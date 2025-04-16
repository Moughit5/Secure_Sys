import ctypes
import os

rijndael = ctypes.CDLL(os.path.abspath("./rijndael.so"))

rijndael.sub_bytes.argtypes = [ctypes.POINTER(ctypes.c_ubyte)]
rijndael.shift_rows.argtypes = [ctypes.POINTER(ctypes.c_ubyte)]
rijndael.mix_columns.argtypes = [ctypes.POINTER(ctypes.c_ubyte)]
rijndael.invert_sub_bytes.argtypes = [ctypes.POINTER(ctypes.c_ubyte)]
rijndael.invert_shift_rows.argtypes = [ctypes.POINTER(ctypes.c_ubyte)]
rijndael.invert_mix_columns.argtypes = [ctypes.POINTER(ctypes.c_ubyte)]


def test_sub_bytes_inverse():
    block = bytes(range(16))
    buf = (ctypes.c_ubyte * 16)(*block)
    rijndael.sub_bytes(buf)
    rijndael.invert_sub_bytes(buf)
    assert bytes(buf) == block, "sub_bytes/invert_sub_bytes failed"


def test_shift_rows_inverse():
    block = bytes(range(16))
    buf = (ctypes.c_ubyte * 16)(*block)
    rijndael.shift_rows(buf)
    rijndael.invert_shift_rows(buf)
    assert bytes(buf) == block, "shift_rows/invert_shift_rows failed"


def test_mix_columns_inverse():
    block = bytes([i for i in range(16)])
    buf = (ctypes.c_ubyte * 16)(*block)
    rijndael.mix_columns(buf)
    rijndael.invert_mix_columns(buf)
    assert bytes(buf) == block, "mix_columns/invert_mix_columns failed"


if __name__ == "__main__":
    test_sub_bytes_inverse()
    test_shift_rows_inverse()
    test_mix_columns_inverse()
    print("All component inverse tests passed.")