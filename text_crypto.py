from s_aes import encrypt, decrypt

def encrypt_text(text, key):
    if len(text) % 2 != 0:
        text += ' '

    result = []

    for i in range(0, len(text), 2):
        block = (ord(text[i]) << 8) | ord(text[i+1])
        # bloco transforma caractere para ascii
        #ex oi -> 111 105 -> 111 << 8 | 105 
        # move o 8 pra esquerda, transformando em 1 numero de 16 bits
        # resultado -> 0b0110111101101001
        
        result.append(encrypt(block, key))
        # usa a funcao do aes e retorna o numero criptografado
    return result


#recebe uma lista, quebra em 2 caracteres
def decrypt_text(cipher_list, key):
    text = ""

    for c in cipher_list:
        block = decrypt(c, key)
        text += chr((block >> 8) & 0xFF)
        text += chr(block & 0xFF)
                #8 bits da esquerda e da direita
    # remove o espaco adicionado antes
    return text.strip()

    # ex "oi" -> 111 105 -> 0b0110111101101001
    # criptografado -> 0b1010101010111100
    # descriptografado -> 0b0110111101101001 -> 111 105 -> "oi"