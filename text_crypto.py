from s_aes import encrypt, decrypt

def encrypt_text(text, key):
    if len(text) % 2 != 0:
        text += ' '

    result = []

    for i in range(0, len(text), 2):
        block = (ord(text[i]) << 8) | ord(text[i+1])
        result.append(encrypt(block, key))

    return result

def decrypt_text(cipher_list, key):
    text = ""

    for c in cipher_list:
        block = decrypt(c, key)
        text += chr((block >> 8) & 0xFF)
        text += chr(block & 0xFF)

    return text.strip()