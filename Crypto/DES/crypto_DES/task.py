import os
from My_box import *


def gen_key(key):
    key_64 = ""
    for i in range(16):
        key_64 += '{0:04b}'.format(int(key[i], 16))
    key_56 = gen_56bit(key_64)
    left_key, right_key = key_56[:28], key_56[28:]
    round_keys = list()
    for index in range(2):
        L = circular_shift(left_key, round_shifts[index])
        R = circular_shift(right_key, round_shifts[index])
        round_key = gen_48bit(L + R)
        round_keys.append(round_key)
        left_key = L
        right_key = R
    return round_keys


def circular_shift(key, n):
    temp = ""
    temp = key[n:] + key[:n]
    return temp


def gen_56bit(key):
    key_56 = ""
    for x in KEY_P1:
        key_56 += key[x - 1]
    return key_56


def gen_48bit(key):
    key_48 = ""
    for x in KEY_P2:
        key_48 += key[x - 1]
    return key_48


def encrypt(plain_text, sub_keys):
    plain_textb = ""
    for i in range(16):
        plain_textb += '{0:04b}'.format(int(plain_text[i], 16))

    plain_textp = permutation(plain_textb)
    left, right = plain_textp[:32], plain_textp[32:]
    out = func(right, sub_keys[0])
    temp = int(out, 2) ^ int(left, 2)
    left, right = right, '{0:032b}'.format(temp)
    out = func(right, sub_keys[1])

    temp = int(out, 2) ^ int(left, 2)
    left = '{0:032b}'.format(temp)
    final = inv_permutation(left + right)
    cipher = hex(int(final, 2))[2:]
    return cipher


def permutation(plain_text):
    p = ""
    for x in IP:
        p += plain_text[x - 1]
    return p


def func(text, key):
    exp = expand(text)
    s_input = '{0:048b}'.format(int(exp, 2) ^ int(key, 2))
    s_out = sbox(s_input)
    f_final = per_func(s_out)
    return f_final


def expand(text):
    temp = ""
    for x in E:
        temp += text[x - 1]
    return temp


def inv_permutation(text):
    final = ""
    for x in Inv_IP:
        final += text[x - 1]
    return final


def per_func(s_output):
    s_final = ""
    for x in P:
        s_final += s_output[x - 1]
    return s_final


def sbox(s_input, index=None):
    s_out = ""
    if index != None:
        i = index
        row = int(s_input[0] + s_input[5], 2)
        column = int(s_input[1:5], 2)
        s_out += '{0:04b}'.format(S[i][row][column])
        return s_out
    else:
        for i in range(8):
            row = int(s_input[6 * i] + s_input[6 * i + 5], 2)
            column = int(s_input[6 * i + 1:6 * i + 5], 2)
            s_out += '{0:04b}'.format(S[i][row][column])
        return s_out


def enc(plain_text):
    sub_keys = gen_key(key_64)
    cipher_text = encrypt(plain_text, sub_keys)
    return cipher_text


def pad(plain_text):
    size = (16 - (len(plain_text) % 16)) % 16
    plain_text += size * '0'
    return plain_text


def myenc(plain_text):
    plain_text = pad(plain_text)
    cipher_text = ""
    for i in range(0, len(plain_text), 16):
        block = plain_text[i:i + 16]
        block_enc = enc(block).rjust(16, '0')
        cipher_text += block_enc
    return cipher_text


def enc2(plain_text, key):
    sub_keys = gen_key(key)
    cipher_text = encrypt(plain_text, sub_keys)
    return cipher_text


key_64 = os.urandom(8).hex()

teststring = "testtest"
print(enc2(teststring.encode().hex(), key_64))

with open("flag.txt") as f:
    flag = f.read()

print("flag: ", myenc(flag.encode().hex()))

# 77a35598c47aeea6
# flag:  86721c7c1ebe2d0af8aa8e073073931b4a5ae6dcf03c784e3c70b5f8ce71cf9eb87f9b836eea0118
