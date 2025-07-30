class DNCCryptoError(Exception):
    pass

class DecryptionError(DNCCryptoError):
    pass

class KeyManagementError(DNCCryptoError):
    pass