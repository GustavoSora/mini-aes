SBOX = {
    0x0: 0x9, 0x1: 0x4, 0x2: 0xA, 0x3: 0xB,
    0x4: 0xD, 0x5: 0x1, 0x6: 0x8, 0x7: 0x5,
    0x8: 0x6, 0x9: 0x2, 0xA: 0x0, 0xB: 0x3,
    0xC: 0xC, 0xD: 0xE, 0xE: 0xF, 0xF: 0x7
}

INV_SBOX = {v: k for k, v in SBOX.items()}

def sub_nibbles(s):
    return [SBOX[x] for x in s]

def inv_sub_nibbles(s):
    return [INV_SBOX[x] for x in s]

def shift_row(s):
    return [s[0], s[1], s[3], s[2]]

def gf_mult(a, b):
    p = 0
    for _ in range(4):
        if b & 1:
            p ^= a
        carry = a & 0x8
        a <<= 1
        if carry:
            a ^= 0b10011
        b >>= 1
    return p & 0xF

def mix_columns(s):
    return [
        s[0] ^ gf_mult(4, s[2]),
        s[1] ^ gf_mult(4, s[3]),
        s[2] ^ gf_mult(4, s[0]),
        s[3] ^ gf_mult(4, s[1])
    ]

def inv_mix_columns(s):
    return [
        gf_mult(9, s[0]) ^ gf_mult(2, s[2]),
        gf_mult(9, s[1]) ^ gf_mult(2, s[3]),
        gf_mult(9, s[2]) ^ gf_mult(2, s[0]),
        gf_mult(9, s[3]) ^ gf_mult(2, s[1])
    ]

def add_round_key(s, k):
    return [x ^ y for x, y in zip(s, k)]

RCON1 = 0b10000000
RCON2 = 0b00110000

def key_schedule(key):
    w0 = key >> 8
    w1 = key & 0xFF

    def g(w, r):
        return ((SBOX[w & 0xF] << 4) | SBOX[w >> 4]) ^ r

    w2 = w0 ^ g(w1, RCON1)
    w3 = w2 ^ w1
    w4 = w2 ^ g(w3, RCON2)
    w5 = w4 ^ w3

    return [(w0 << 8) | w1,
            (w2 << 8) | w3,
            (w4 << 8) | w5]

def split16(x):
    return [(x >> 12) & 0xF,
            (x >> 8) & 0xF,
            (x >> 4) & 0xF,
            x & 0xF]

def join16(s):
    return (s[0]<<12)|(s[1]<<8)|(s[2]<<4)|s[3]

def key_to_state(k):
    return split16(k)

def encrypt(p, key):
    keys = key_schedule(key)
    s = split16(p)

    s = add_round_key(s, key_to_state(keys[0]))

    s = sub_nibbles(s)
    s = shift_row(s)
    s = mix_columns(s)
    s = add_round_key(s, key_to_state(keys[1]))

    s = sub_nibbles(s)
    s = shift_row(s)
    s = add_round_key(s, key_to_state(keys[2]))

    return join16(s)

def decrypt(c, key):
    keys = key_schedule(key)
    s = split16(c)

    s = add_round_key(s, key_to_state(keys[2]))
    s = shift_row(s)
    s = inv_sub_nibbles(s)

    s = add_round_key(s, key_to_state(keys[1]))
    s = inv_mix_columns(s)
    s = shift_row(s)
    s = inv_sub_nibbles(s)

    s = add_round_key(s, key_to_state(keys[0]))

    return join16(s)