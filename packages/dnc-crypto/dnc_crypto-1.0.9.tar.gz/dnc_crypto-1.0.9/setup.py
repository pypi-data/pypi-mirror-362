import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dnc_crypto",
    version="1.0.9",
    author="Mohammadmoein Pisoude",
    author_email="mmoeinp3@gmail.com",
    description="A high-performance, industrial-grade cipher with optional GPU acceleration.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #url="https://github.com/your_username/dnc_crypto",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
        'cryptography',
        'networkx',
        'pynacl',
    ],
    extras_require={
        'gpu': ["cupy-cuda12x"], # کاربر با pip install dnc-crypto[gpu] می‌تواند نصب کند
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security :: Cryptography",
    ],
    python_requires='>=3.7',
)