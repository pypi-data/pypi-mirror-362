import numpy
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

_graph_cache = {}

def modInverse(a, m):
    a = a % m
    for x in range(1, m):
        if ((a * x) % m == 1): return x
    return 1

# --- توابع ماژول‌ها که اکنون 'backend' را به عنوان آرگومان می‌گیرند ---
def pde_transform(data_arr, a, b, backend):
    return ((data_arr.astype(backend.uint16) * a + b) % 256).astype(backend.uint8)

def knot_transform(data_arr, r, backend):
    r = r % 8
    if r == 0: return data_arr
    return (((data_arr << r) | (data_arr >> (8 - r))) & 0xFF).astype(backend.uint8)

def graph_transform(data_arr, seed, backend):
    length = len(data_arr)
    if length == 0: return data_arr
    
    # کش جایگشت در حافظه CPU ذخیره می‌شود
    if (length, seed) in _graph_cache:
        p_cpu, _ = _graph_cache[(length, seed)]
    else:
        rng = numpy.random.RandomState(seed)
        p_cpu = numpy.arange(length)
        rng.shuffle(p_cpu)
        p_inv_cpu = numpy.empty_like(p_cpu)
        p_inv_cpu[p_cpu] = numpy.arange(length)
        _graph_cache[(length, seed)] = (p_cpu, p_inv_cpu)
    
    # انتقال اندیس‌ها به GPU در صورت نیاز
    p = backend.array(p_cpu)
    return data_arr[p]

def game_transform(data_arr, key_part_arr, backend):
    if len(data_arr) != len(key_part_arr):
        # np.resize در cupy وجود ندارد، از یک معادل استفاده می‌کنیم
        if backend.__name__ == 'cupy':
            repeats = (len(data_arr) + len(key_part_arr) - 1) // len(key_part_arr)
            key_part_arr = backend.tile(key_part_arr, repeats)[:len(data_arr)]
        else: # NumPy
            key_part_arr = backend.resize(key_part_arr, len(data_arr))
            
    return backend.bitwise_xor(data_arr, key_part_arr)

class DynamicNetworkCipher:
    def __init__(self, key: bytes, backend, num_rounds=16, block_size=16):
        if len(key) < 32: raise ValueError("Key must be at least 32 bytes.")
        self.key = key
        self.backend = backend
        self.num_rounds = num_rounds
        self.block_size = block_size
        self.half_size = block_size // 2
        self.round_params = self._key_schedule()

    def _hash(self, data: bytes) -> bytes:
        digest = hashes.Hash(hashes.SHA512(), backend=default_backend())
        digest.update(data)
        return digest.finalize()

    def _derive_kdf(self, salt_base: bytes, out_len: int) -> bytes:
        output = b''; counter = 0
        while len(output) < out_len:
            current_salt = salt_base + counter.to_bytes(4, 'big')
            chunk = self._hash(self.key + current_salt)
            output += chunk
            counter += 1
        return output[:out_len]

    def _key_schedule(self):
        params = []; key_material_len = 80
        for i in range(self.num_rounds):
            round_data = self._derive_kdf(f"round_{i}".encode(), key_material_len)
            offset = 0
            pde_a = (round_data[offset] | 1); offset += 1
            pde_b = round_data[offset]; offset += 1
            graph_seed = int.from_bytes(round_data[offset:offset+4], 'big'); offset += 4
            game_key_bytes = round_data[offset:offset+self.half_size]; offset += self.half_size
            knot_r = round_data[offset] % 8; offset += 1
            order_seed = round_data[offset] % 24; offset += 1
            mask_key = round_data[offset:offset+32]; offset += 32
            params.append({
                'pde_a': pde_a, 'pde_b': pde_b, 'knot_r': knot_r, 'graph_seed': graph_seed,
                'game_key': self.backend.array(numpy.frombuffer(game_key_bytes, dtype=numpy.uint8)),
                'order_seed': order_seed, 'mask_key': mask_key
            })
        return params

    def _F(self, half_block_arr, round_idx: int):
        params = self.round_params[round_idx]
        
        # برای تبدیل به بایت، اگر داده روی GPU است، باید به CPU منتقل شود
        # .get() این کار را برای CuPy انجام می‌دهد
        data_for_hash = half_block_arr.get().tobytes() if self.backend.__name__ == 'cupy' else half_block_arr.tobytes()
        mask_bytes = self._hash(params['mask_key'] + data_for_hash)[:self.half_size]
        mask = self.backend.array(numpy.frombuffer(mask_bytes, dtype=numpy.uint8))
        
        data_arr = self.backend.bitwise_xor(half_block_arr, mask)
        
        order_rng = numpy.random.RandomState(params['order_seed'])
        order = numpy.arange(4)
        order_rng.shuffle(order)
        for op_idx in order:
            if op_idx == 0: data_arr = pde_transform(data_arr, params['pde_a'], params['pde_b'], self.backend)
            elif op_idx == 1: data_arr = knot_transform(data_arr, params['knot_r'], self.backend)
            elif op_idx == 2: data_arr = graph_transform(data_arr, params['graph_seed'], self.backend)
            elif op_idx == 3: data_arr = game_transform(data_arr, params['game_key'], self.backend)
        
        return self.backend.bitwise_xor(data_arr, mask)

    def encrypt_block(self, block_arr):
        L, R = block_arr[:self.half_size], block_arr[self.half_size:]
        for i in range(self.num_rounds):
            F_out = self._F(R, i)
            L, R = R, self.backend.bitwise_xor(L, F_out)
        return self.backend.concatenate((R, L))

    def decrypt_block(self, block_arr):
        L, R = block_arr[:self.half_size], block_arr[self.half_size:]
        R, L = L, R
        for i in range(self.num_rounds - 1, -1, -1):
            F_out = self._F(L, i)
            R, L = L, self.backend.bitwise_xor(R, F_out)
        return self.backend.concatenate((L, R))

class ChainedEncryptor:
    def __init__(self, master_key: bytes, backend, num_chains=8, block_size=16):
        self.master_key = master_key
        self.backend = backend
        self.num_chains = num_chains
        self.block_size = block_size
        
    def _hash(self, data):
        digest = hashes.Hash(hashes.SHA512(), backend=default_backend()); digest.update(data); return digest.finalize()

    def _derive_key(self, salt: bytes) -> bytes:
        return self._hash(self.master_key + salt)[:len(self.master_key)]

    def _process_data(self, data: bytes, decrypt_mode: bool):
        is_gpu_mode = self.backend.__name__ == 'cupy'
        
        if decrypt_mode and len(data) % self.block_size != 0:
            raise ValueError("Ciphertext length must be a multiple of block size.")
            
        padding_len = self.block_size - (len(data) % self.block_size) if not decrypt_mode else 0
        padded_data = data + bytes([padding_len] * padding_len) if not decrypt_mode else data
        
        chain_keys = [self._derive_key(f"chain_{i}".encode()) for i in range(self.num_chains)]
        
        device_data_arr = self.backend.array(numpy.frombuffer(padded_data, dtype=numpy.uint8))
        
        num_blocks = len(device_data_arr) // self.block_size
        block_view = device_data_arr.reshape(num_blocks, self.block_size)

        loop_range = range(self.num_chains) if not decrypt_mode else range(self.num_chains - 1, -1, -1)

        for i in loop_range:
            engine = DynamicNetworkCipher(chain_keys[i], backend=self.backend, block_size=self.block_size)
            processed_blocks_list = []
            for j in range(num_blocks):
                block_arr = block_view[j]
                if not decrypt_mode:
                    processed_block = engine.encrypt_block(block_arr)
                else:
                    processed_block = engine.decrypt_block(block_arr)
                processed_blocks_list.append(processed_block)
            
            if not processed_blocks_list:
                # Handle empty input case
                block_view = self.backend.array([], dtype=numpy.uint8).reshape(0, self.block_size)
            else:
                block_view = self.backend.stack(processed_blocks_list)

        final_data_arr = block_view.flatten()
        final_data_bytes = final_data_arr.get().tobytes() if is_gpu_mode else final_data_arr.tobytes()

        if decrypt_mode:
            if not final_data_bytes:
                # Handle empty decryption result
                return b''
            padding_len_val = final_data_bytes[-1]
            if padding_len_val > self.block_size or padding_len_val == 0: raise ValueError("Invalid padding value.")
            if not all(b == padding_len_val for b in final_data_bytes[-padding_len_val:]): raise ValueError("Invalid padding bytes.")
            return final_data_bytes[:-padding_len_val]
        else:
            return final_data_bytes

    def encrypt(self, plaintext: bytes) -> bytes:
        return self._process_data(plaintext, decrypt_mode=False)

    def decrypt(self, ciphertext: bytes) -> bytes:
        return self._process_data(ciphertext, decrypt_mode=True)