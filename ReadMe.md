# AES-128 Implementation in C with Python Tests

![AES Encryption](https://img.shields.io/badge/Algorithm-AES-2ea44f) ![C](https://img.shields.io/badge/Language-C-blue) ![Python](https://img.shields.io/badge/Test%20Suite-Python-yellow)

This project provides a complete implementation of the AES-128 encryption algorithm in C, with comprehensive Python-based testing.

## Features

- Pure C implementation of AES-128 (Rijndael algorithm)
- ECB mode encryption/decryption
- Complete key expansion implementation
- Python tests suite with:
  - Known answer tests (NIST FIPS-197 vectors)
  - Random data roundtrip tests
  - Cross-validation with PyCryptodome


## Prerequisites

- GCC or compatible C compiler
- Python 3.6+
- PyCryptodome (for test comparisons)
- pytest (for running tests)
- Sometimes the dll runs in 32bits so we need to make it in 64bits we should use 

```bash
x86_64-w64-mingw32-gcc -shared -o rijndael.dll rijndael.c
```

## Installation


Running Tests
Install Python dependencies:

```bash
pip install pycryptodome pytest
```
Run all the tests:

```bash
python -m pytest -v
```
Run the test_components:

```bash
python test_components.py 
```

Run the test_ae:

```bash
python test_ae.py    
```
Run the test:

```bash
python test.py    
```
## Documentation

Full code documentation is available in:

Header file (rijndael.c)

Test script (test_ae.py)

Inline comments throughout implementation

#### Thank YOU For Reading ME <3
