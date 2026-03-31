from text_crypto import encrypt_text, decrypt_text
from debug import debug_encrypt_text
from attack import brute_force

def main():
    key = 0b0100101011110101
    cifrado = []
    texto_original = ""

    while True:
        print("\n=== MINI AES ===")
        print("1 - Criptografar texto")
        print("2 - Mostrar criptografado")
        print("3 - Descriptografar")
        print("4 - Mostrar descriptografado")
        print("5 - Mostrar tudo")
        print("6 - Mostrar funcionamento (debug)")
        print("7 - Quebrar chave (força bruta)")
        print("0 - Sair")

        opcao = input("Escolha: ")

        match opcao:
            case "1":
                texto_original = input("Digite o texto: ")
                cifrado = encrypt_text(texto_original, key)
                print("✅ Criptografado!")

            case "2":
                print("Cifrado:", cifrado if cifrado else "Nada ainda")

            case "3":
                if cifrado:
                    texto_decifrado = decrypt_text(cifrado, key)
                    print("✅ Descriptografado!")
                else:
                    print("Nada para descriptografar")

            case "4":
                if cifrado:
                    print("Texto:", decrypt_text(cifrado, key))
                else:
                    print("Nada ainda")

            case "5":
                if cifrado:
                    print("Original:", texto_original)
                    print("Cifrado:", cifrado)
                    print("Decifrado:", decrypt_text(cifrado, key))
                else:
                    print("Nada ainda")

            case "6":
                if texto_original:
                    debug_encrypt_text(texto_original, key)
                else:
                    print("Digite um texto primeiro!")

            case "7":
                if cifrado:
                    known = input("Digite o texto original (ex: oi): ")
                    brute_force(cifrado[0], known)
                else:
                    print("Nada criptografado ainda")

            case "0":
                print("Saindo...")
                break

            case _:
                print("Opção inválida!")

if __name__ == "__main__":
    main()