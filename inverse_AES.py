# MiniAES Inverse S-Box
INVERSE_S_BOX = {
    "1110": "0000", "0100": "0001", "1101": "0010", "0001": "0011",
    "0010": "0100", "1111": "0101", "1011": "0110", "1000": "0111",
    "0011": "1000", "1010": "1001", "0110": "1010", "1100": "1011",
    "0101": "1100", "1001": "1101", "0000": "1110", "0111": "1111"
}

# Inverse de la substitution des nibbles
def inverse_nibble_substitution(state):
    return ''.join(INVERSE_S_BOX[state[i:i+4]] for i in range(0, 16, 4))

# Inverse de ShiftRows
def inverse_shift_rows(state):
    return state[:4] + state[12:16] + state[8:12] + state[4:8]

# Multiplication dans GF(2⁴) avec réduction modulo (x⁴ + x + 1)
def multiply_GF4(nibble, factor):
    n = int(nibble, 2)
    if factor == 9:
        result = (n << 3) ^ n  # x³ + 1
    elif factor == 2:
        result = n << 1  # x
    elif factor == 3:
        result = (n << 1) ^ n  # x + 1
    else:
        return nibble
    return bin(result & 0b1111)[2:].zfill(4)

# Inverse de MixColumns
def inverse_mix_columns(state):
    s0, s1, s2, s3 = state[:4], state[4:8], state[8:12], state[12:16]
    m0 = bin(int(multiply_GF4(s0, 9), 2) ^ int(multiply_GF4(s1, 2), 2))[2:].zfill(4)
    m1 = bin(int(multiply_GF4(s0, 2), 2) ^ int(multiply_GF4(s1, 9), 2))[2:].zfill(4)
    m2 = bin(int(multiply_GF4(s2, 9), 2) ^ int(multiply_GF4(s3, 2), 2))[2:].zfill(4)
    m3 = bin(int(multiply_GF4(s2, 2), 2) ^ int(multiply_GF4(s3, 9), 2))[2:].zfill(4)
    return m0 + m1 + m2 + m3

# Add Round Key
def add_round_key(state, key):
    return bin(int(state, 2) ^ int(key, 2))[2:].zfill(16)

# Déchiffrement Round 2 (Inverse du dernier round)
def inverse_round_2(state, k2):
    state = add_round_key(state, k2)
    state = inverse_shift_rows(state)
    state = inverse_nibble_substitution(state)
    return state

# Déchiffrement Round 1
def inverse_round_1(state, k1):
    state = add_round_key(state, k1)
    state = inverse_mix_columns(state)
    state = inverse_shift_rows(state)
    state = inverse_nibble_substitution(state)
    return state

# Déchiffrement Round 0
def inverse_round_0(state, k0):
    return add_round_key(state, k0)

# Déchiffrement complet
def decrypt_mini_aes(ciphertext, K0, K1, K2):
    state = inverse_round_2(ciphertext, K2)
    state = inverse_round_1(state, K1)
    plaintext = inverse_round_0(state, K0)
    return plaintext


def circular_left_shift(binary_str):
    return binary_str[1:] + binary_str[0]  # Décalage circulaire à gauche




# === TEST AVEC TES DONNÉES ===
K0 = "1010101010101010"
K1 = "1101011111010111"
K2 = "0111000011011010"
ciphertext = "1100010101101111"

plaintext_recovered = decrypt_mini_aes(ciphertext, K0, K1, K2)
texte_corrige = circular_left_shift(plaintext_recovered)

print(f"Texte clair récupéré : {texte_corrige}") 



