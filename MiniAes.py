
#  MiniAES S-Box
S_BOX = {
    "0000": "1110", "0001": "0100", "0010": "1101", "0011": "0001",
    "0100": "0010", "0101": "1111", "0110": "1011", "0111": "1000",
    "1008": "0011", "1001": "1010", "1010": "0110", "1011": "1100",
    "1100": "0101", "1101": "1001", "1110": "0000", "1111": "0111"
}

# Substitution des Nibbles (S-Box)
def nibble(nibble):
    return S_BOX[nibble]

#  Génération des Clés MiniAES
def generate_mini_aes_keys(initial_key):
    if len(initial_key) != 16:
        raise ValueError(f"Clé invalide : {initial_key} (longueur {len(initial_key)})")

    w0, w1, w2, w3 = initial_key[:4], initial_key[4:8], initial_key[8:12], initial_key[12:]

    recon1, recon2 = "0001", "0010"

    # Génération de K1 (w4 à w7)
    sub_w3 = nibble(w3)
    w4 = bin(int(w0, 2) ^ int(sub_w3, 2) ^ int(recon1, 2))[2:].zfill(4)
    w5 = bin(int(w1, 2) ^ int(w4, 2))[2:].zfill(4)
    w6 = bin(int(w2, 2) ^ int(w5, 2))[2:].zfill(4)
    w7 = bin(int(w3, 2) ^ int(w6, 2))[2:].zfill(4)
    K1 = w4 + w5 + w6 + w7

    # Génération de K2 (w8 à w11)
    sub_w7 = nibble(w7)
    w8 = bin(int(w4, 2) ^ int(sub_w7, 2) ^ int(recon2, 2))[2:].zfill(4)
    w9 = bin(int(w5, 2) ^ int(w8, 2))[2:].zfill(4)
    w10 = bin(int(w6, 2) ^ int(w9, 2))[2:].zfill(4)
    w11 = bin(int(w7, 2) ^ int(w10, 2))[2:].zfill(4)
    K2 = w8 + w9 + w10 + w11

    return initial_key, K1, K2

# Round 0 (Add Round Key)
def round_0(plaintext, k0):
    result = bin(int(plaintext, 2) ^ int(k0, 2))[2:].zfill(16)
    return result

def nibble_substitution(state):
    return ''.join(S_BOX[state[i:i+4]] for i in range(0, 16, 4))

# ShiftRows (Permutation des nibbles)
def shift_rows(state):
    return state[:4] + state[12:16] + state[8:12] + state[4:8]

# Multiplications dans GF(2⁴) modulo x⁴ + x + 1
def multiply_by_2(nibble):
    n = int(nibble, 2)
    result = (n << 1) & 0b1111  # Décalage à gauche et masque sur 4 bits
    if n & 0b1000:  # Vérifie si le MSB était 1 avant le décalage
        result ^= 0b0011  # Réduction modulo x⁴ + x + 1
    return bin(result)[2:].zfill(4)

def multiply_by_3(nibble):
    return bin(int(nibble, 2) ^ int(multiply_by_2(nibble), 2))[2:].zfill(4)
# MixColumns (Matricielle)
def mix_columns(state):
    s0, s1, s2, s3 = state[:4], state[4:8], state[8:12], state[12:16]
    m0 = bin(int(multiply_by_3(s0), 2) ^ int(multiply_by_2(s1), 2))[2:].zfill(4)
    m1 = bin(int(multiply_by_2(s0), 2) ^ int(multiply_by_3(s1), 2))[2:].zfill(4)
    m2 = bin(int(multiply_by_3(s2), 2) ^ int(multiply_by_2(s3), 2))[2:].zfill(4)
    m3 = bin(int(multiply_by_2(s2), 2) ^ int(multiply_by_3(s3), 2))[2:].zfill(4)
    return m0 + m1 + m2 + m3

#  Add Round Key (XOR avec la clé de round)
def add_round_key(state, key):
    return bin(int(state, 2) ^ int(key, 2))[2:].zfill(16)

#  Round 1 (Nibble Sub, ShiftRows, MixColumns, AddRoundKey)
def round_1(state, k1):
    state = nibble_substitution(state)
    state = shift_rows(state)
    state = mix_columns(state)
    state = add_round_key(state, k1)
    return state

# Round 2 (Nibble Sub, ShiftRows, AddRoundKey)
def round_2(state, k2):
    state = nibble_substitution(state)
    state = shift_rows(state)
    state = add_round_key(state, k2)
    return state

# Test
initial_key = "1010101010101010"
plaintext = "1100110011001100"

print ("plaintext : " , plaintext)
#  Génération des clés
K0, K1, K2 = generate_mini_aes_keys(initial_key)
print(f"K0: {K0}")
print(f"K1: {K1}")
print(f"K2: {K2}")

# Round 0
ciphertext_round0 = round_0(plaintext, K0)
print(f"Résultat du Round 0 : {ciphertext_round0}")

# Round 1
ciphertext_round1 = round_1(ciphertext_round0, K1)
print(f"Résultat du Round 1 : {ciphertext_round1}")

# Round 2 (Texte chiffré final)
ciphertext_final = round_2(ciphertext_round1, K2)
print(f"Résultat du Round 2 (Texte chiffré final) : {ciphertext_final}")

# Test supplémentaire pour MixColumns
test_state = "1100110011001100"
print(f"Test MixColumns : {mix_columns(test_state)}")



