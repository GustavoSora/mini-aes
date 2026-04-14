from a.s_aes_key import *

def debug_encrypt_text(text):
    if len(text) % 2 != 0:
        text += ' '

    for i in range(0, len(text), 2):
        block = (ord(text[i]) << 8) | ord(text[i+1])

        print("\n=== DEBUG BLOCO ===")
        print("Texto:", text[i:i+2])
        print("Bloco:", bin(block))

        debug_encrypt(block)

def debug_encrypt(p):
    keys = key_schedule(KEY)
    s = split16(p)

    print("Estado inicial:", s)
    print("K0:", split16(keys[0]))

    s = add_round_key(s, key_to_state(keys[0]))
    print("AddRoundKey:", s)

    s = sub_nibbles(s)
    print("SubNibble:", s)

    s = shift_row(s)
    print("ShiftRow:", s)

    s = mix_columns(s)
    print("MixColumns:", s)

    print("K1:", split16(keys[1]))
    s = add_round_key(s, key_to_state(keys[1]))
    print("AddRoundKey:", s)

    s = sub_nibbles(s)
    print("SubNibble:", s)

    s = shift_row(s)
    print("ShiftRow:", s)

    print("K2:", split16(keys[2]))
    s = add_round_key(s, key_to_state(keys[2]))

    print("Resultado final:", s)