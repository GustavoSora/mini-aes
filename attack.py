from s_aes import decrypt

def brute_force(cipher, known_text):
    print("\nIniciando ataque de força bruta...")
    print(f"Texto esperado: '{known_text}'\n")

    tentativas = 0

    for key in range(0, 2**16):
        tentativas += 1

        decrypted = decrypt(cipher, key)

        c1 = (decrypted >> 8) & 0xFF
        c2 = decrypted & 0xFF

        texto = chr(c1) + chr(c2)

        if key < 10 or key % 5000 == 0:
            print(f"[Tentativa {tentativas}] "
                  f"Chave: {bin(key)} "
                  f"→ Resultado: '{texto}'")

        if texto == known_text:
            print("\nCHAVE ENCONTRADA!")
            print(f"Chave correta: {bin(key)}")
            print(f"Tentativas: {tentativas}")
            print(f"Texto obtido: '{texto}'")
            return key

    print("\nChave não encontrada")
    return None