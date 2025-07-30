import os
from time import time
import tgcrypto
import tgcrypto_optimized


def test_encrypt_ctr():
    data = os.urandom(10 * 1024 * 1024)
    key = os.urandom(32)  # Random Key
    iv = bytearray(16)  # Reserve 16 bytes for the IV
    iv_copy = bytearray(16)  # Reserve 16 more bytes for the copy
    iv[:] = os.urandom(16)  # Random IV
    iv_copy[:] = iv  # Copy IV

    start_time = time()
    first_result, first_state, first_iv = tgcrypto_optimized.ctr256_encrypt(
        bytes(data),
        bytes(key),
        bytes(iv),
        0
    )
    #print('first', round((time() - start_time) * 1000, 5))
    second_state = bytearray(1)
    start_time = time()
    second_result = tgcrypto.ctr256_encrypt(
        data,
        key,
        iv_copy,
        second_state
    )
    #print('second', round((time() - start_time) * 1000, 5))
    assert first_result == second_result
    assert first_state == second_state[0]
    assert first_iv == iv_copy


def test_encrypt_ctr_state():
    data = os.urandom(10 * 1024 * 1024)
    key = os.urandom(32)  # Random Key
    iv = bytearray(16)  # Reserve 16 bytes for the IV
    iv_copy = bytearray(16)  # Reserve 16 more bytes for the copy
    iv[:] = os.urandom(16)  # Random IV
    iv_copy[:] = iv  # Copy IV

    start_time = time()
    first_result, first_state, first_iv = tgcrypto_optimized.ctr256_encrypt(
        bytes(data),
        bytes(key),
        bytes(iv),
        5
    )
    #print('first', round((time() - start_time) * 1000, 5))
    second_state = bytearray(1)
    second_state[0] = 5
    start_time = time()
    second_result = tgcrypto.ctr256_encrypt(
        data,
        key,
        iv_copy,
        second_state
    )
    #print('second', round((time() - start_time) * 1000, 5))
    assert first_result == second_result
    assert first_state == second_state[0]
    assert first_iv == iv_copy


def test_encrypt_ige():
    data = os.urandom(10 * 1024 * 1024)
    key = os.urandom(32)  # Random Key
    iv = os.urandom(32)  # Random IV

    start_time = time()
    first_result = tgcrypto_optimized.ige256_encrypt(data, key, iv)
    #print('first', round((time() - start_time) * 1000, 5))
    start_time = time()
    second_result = tgcrypto.ige256_encrypt(data, key, iv)
    #print('second', round((time() - start_time) * 1000, 5))
    assert first_result == second_result
