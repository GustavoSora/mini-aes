# Explicação do Mini AES (S-AES)

## Introdução

O **Mini AES** (ou S-AES - Simplified AES) é uma versão simplificada do algoritmo AES (Advanced Encryption Standard) desenvolvida para fins educacionais. Ele opera com blocos de **16 bits** (2 bytes) e chaves de **16 bits**, ao contrário do AES real que usa blocos de 128 bits e chaves de 128/192/256 bits. Isso torna o Mini AES muito mais simples de implementar e entender, mas também menos seguro (vulnerável a ataques de força bruta devido ao espaço de chaves pequeno: apenas 65.536 possibilidades).

## Funcionamento Geral da Criptografia e Decriptografia

O Mini AES é um algoritmo de **bloco simétrico**, onde a mesma chave é usada para criptografar e decriptografar. Ele divide o texto em blocos de 2 caracteres (16 bits) e aplica uma série de operações matemáticas em cada bloco. O processo é dividido em **rodadas** (rounds), com 2 rodadas completas mais uma inicial.

### Criptografia (Encrypt)
- **Entrada**: Bloco de 16 bits (plaintext) + Chave de 16 bits.
- **Saída**: Bloco de 16 bits criptografado (ciphertext).
- **Passos principais**:
  1. **Expansão da chave**: Gera 3 subchaves (K0, K1, K2) a partir da chave original.
  2. **Rodada 0**: Adiciona a primeira subchave (AddRoundKey).
  3. **Rodada 1**: Substituição (SubNibbles), Permutação (ShiftRow), Mistura (MixColumns), Adição de chave (AddRoundKey).
  4. **Rodada 2**: Substituição, Permutação, Adição de chave (sem MixColumns na última rodada).

### Decriptografia (Decrypt)
- É o inverso da criptografia, aplicando as operações em ordem reversa.
- Usa as mesmas subchaves, mas na ordem inversa (K2, K1, K0).
- Inclui operações inversas: InvSubNibbles, InvMixColumns, etc.

Para textos maiores, o código divide o texto em blocos de 2 caracteres e criptografa cada um separadamente (modo ECB - Electronic Codebook, que é simples mas não recomendado para textos longos devido a padrões repetitivos).

## O que são Nibbles e S-Box?

Antes de aprofundar no código, vamos explicar dois conceitos fundamentais no Mini AES: **nibbles** e **S-Box**.

### Nibbles
- Um **nibble** (ou nybble) é uma unidade de 4 bits, ou seja, metade de um byte (8 bits).
- No Mini AES, o bloco de dados é de 16 bits (2 bytes), dividido em **4 nibbles** de 4 bits cada.
- Exemplo: O número 16 bits `0b110111101101001` (28425 em decimal) é dividido em nibbles:
  - Bits 15-12: `0b1101` (13 em decimal)
  - Bits 11-8: `0b1110` (14)
  - Bits 7-4: `0b1101` (13)
  - Bits 3-0: `0b1001` (9)
  - Representação como lista: `[13, 14, 13, 9]` (usando `split16`).
- Os nibbles são manipulados individualmente durante as operações do algoritmo.

### S-Box (Substitution Box)
- A **S-Box** é uma tabela de substituição não-linear que mapeia cada valor de entrada (nibble, 0-15) para outro valor (0-15).
- No Mini AES, a S-Box é definida como um dicionário fixo:
  ```python
  SBOX = {
      0x0: 0x9, 0x1: 0x4, 0x2: 0xA, 0x3: 0xB,
      0x4: 0xD, 0x5: 0x1, 0x6: 0x8, 0x7: 0x5,
      0x8: 0x6, 0x9: 0x2, 0xA: 0x0, 0xB: 0x3,
      0xC: 0xC, 0xD: 0xE, 0xE: 0xF, 0xF: 0x7
  }
  ```
- **Propósito**: Introduz "confusão" (não-linearidade) no algoritmo, tornando difícil para um atacante prever a saída a partir da entrada. É uma operação de substituição byte-a-byte no AES real, mas aqui é nibble-a-nibble.
- **Como funciona**: Para cada nibble no estado, substitua pelo valor correspondente na S-Box.
  - Exemplo: Nibble 0x0 → 0x9, 0x1 → 0x4, etc.
- **INV_SBOX**: A S-Box inversa para decriptografia, onde cada valor é mapeado de volta ao original.
- **Uso no código**: `sub_nibbles(s)` aplica a S-Box a cada nibble da lista `s`. `inv_sub_nibbles(s)` usa a inversa.

Esses conceitos são essenciais para entender como o Mini AES transforma os dados de forma segura e reversível.

## Explicação Parte a Parte do Código

Explicação dos arquivos principais, focando em `s_aes.py` (implementação do algoritmo), `text_crypto.py` (criptografia de texto) e `main.py` (interface). Incluí exemplos de valores de variáveis baseados em execuções típicas (usando chave `0b0100101011110101` e texto "oi").

### 1. `s_aes.py` - Implementação do Algoritmo

Este arquivo contém as operações básicas do S-AES.

#### SBOX e INV_SBOX
Tabelas de substituição (S-Boxes). O SBOX substitui cada nibble (4 bits) por outro valor fixo. INV_SBOX é o inverso para decriptografia.

```python
SBOX = {
    0x0: 0x9, 0x1: 0x4, 0x2: 0xA, 0x3: 0xB,
    0x4: 0xD, 0x5: 0x1, 0x6: 0x8, 0x7: 0x5,
    0x8: 0x6, 0x9: 0x2, 0xA: 0x0, 0xB: 0x3,
    0xC: 0xC, 0xD: 0xE, 0xE: 0xF, 0xF: 0x7
}
```

- `sub_nibbles(s)`: Aplica SBOX a cada nibble do estado (lista de 4 nibbles).
- `inv_sub_nibbles(s)`: Aplica INV_SBOX.

#### shift_row(s)
Permutação simples: troca os dois últimos nibbles.

```python
def shift_row(s):
    return [s[0], s[1], s[3], s[2]]
```

Exemplo: Se s = [0, 1, 2, 3], shift_row(s) = [0, 1, 3, 2].

#### gf_mult(a, b)
Multiplicação no campo finito GF(2^4), usado para MixColumns.

```python
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
```

Exemplo: gf_mult(4, 2) = 8 (em decimal).

#### mix_columns(s) e inv_mix_columns(s)
Mistura os nibbles usando multiplicação no campo finito.

```python
def mix_columns(s):
    return [
        s[0] ^ gf_mult(4, s[2]),
        s[1] ^ gf_mult(4, s[3]),
        s[2] ^ gf_mult(4, s[0]),
        s[3] ^ gf_mult(4, s[1])
    ]
```

Exemplo: Se s = [0, 1, 2, 3], mix_columns(s) ≈ [8, 9, 10, 11] (dependendo dos cálculos GF).

#### add_round_key(s, k)
XOR entre o estado e a subchave.

```python
def add_round_key(s, k):
    return [x ^ y for x, y in zip(s, k)]
```

Exemplo: s = [0, 1, 2, 3], k = [4, 5, 6, 7] → [4, 4, 4, 4].

#### key_schedule(key)
Expande a chave de 16 bits em 3 subchaves.

```python
def key_schedule(key):
    w0 = key >> 8
    w1 = key & 0xFF
    # ... cálculos para w2, w3, w4, w5
    return [(w0 << 8) | w1, (w2 << 8) | w3, (w4 << 8) | w5]
```

Para chave 0b0100101011110101 (19781 em decimal):
- w0 = 0b01001010 (74), w1 = 0b11110101 (245)
- K0 = 0b0100101011110101 -> [4, 10, 15, 5]
- K1 = 0b1101110100101000 -> [13, 13, 2, 8]
- K2 = 0b1000011110101111 -> [8, 7, 10, 15]

#### encrypt(p, key)
Função de criptografia.

Exemplo com p = "oi" (ord('o')=111, ord('i')=105 → bloco = 111<<8 | 105 = 28425 em decimal, 0b110111101101001 em binário):
- Estado inicial: [6, 15, 6, 9] (split16(28425))
- K0: [4, 10, 15, 5]
- Após AddRoundKey com K0: [2, 5, 9, 12]
- Após SubNibbles: [10, 1, 2, 12]
- Após ShiftRow: [10, 1, 12, 2]
- Após MixColumns: [15, 9, 2, 6]
- K1: [13, 13, 2, 8]
- Após AddRoundKey com K1: [2, 4, 0, 14]
- Após SubNibbles: [10, 13, 9, 15] (não mostrado no debug, mas calculado)
- Após ShiftRow: [10, 13, 15, 9]
- K2: [8, 7, 10, 15]
- Após AddRoundKey com K2: [2, 10, 5, 6] (resultado final, ciphertext)

#### decrypt(c, key)
Inverso, aplicando operações reversas.

Exemplo com ciphertext [2, 10, 5, 6] (join16 = 10838, 0b10101001010110):
- Estado inicial: [2, 10, 5, 6]
- Após AddRoundKey com K2: [exemplo: [10, 13, 15, 9]] (inverso)
- Após ShiftRow: [10, 13, 9, 15]
- Após InvSubNibbles: [exemplo: [2, 4, 0, 14]]
- Após AddRoundKey com K1: [15, 9, 2, 6]
- Após InvMixColumns: [10, 1, 12, 2]
- Após ShiftRow: [10, 1, 2, 12]
- Após InvSubNibbles: [2, 5, 9, 12]
- Após AddRoundKey com K0: [6, 15, 6, 9] (plaintext "oi")

### 2. `text_crypto.py` - Criptografia de Texto
- **encrypt_text(text, key)**: Divide em blocos de 2 chars, converte para 16 bits, criptografa.
- **decrypt_text(cipher_list, key)**: Decriptografa e converte de volta para string.

Exemplo: Texto "oi" → bloco 28425 → criptografado → lista [cipher] → decriptografado → "oi".

### 3. `main.py` - Interface Principal
Menu interativo. Chave fixa: 0b0100101011110101.

### 4. `debug.py` - Depuração
Mostra estados intermediários. Execute `debug_encrypt_text("oi", key)` para ver valores reais.

### 5. `attack.py` - Ataque de Força Bruta
Testa todas as chaves até encontrar a que decriptografa para o texto conhecido.

## Como Usar
- Execute `python main.py` para o menu.
- Digite um texto, criptografe, veja o resultado.
- Use debug para entender os passos.
- O ataque de força bruta demonstra a fraqueza da chave curta.

