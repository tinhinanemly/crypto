# Définition des tables de permutation
IP = [2, 6, 3, 1, 4, 8, 5, 7]       
IP_inv = [4, 1, 3, 5, 7, 2, 8, 6]    

EP = [4, 1, 2, 3, 2, 3, 4, 1]        
P4 = [2, 4, 3, 1]                    

# Définition des S-Boxes (binaire)
S0 = [["01", "00", "11", "10"], 
      ["11", "10", "01", "00"], 
      ["00", "10", "01", "11"], 
      ["11", "01", "11", "10"]]

S1 = [["00", "01", "10", "11"],  
      ["10", "00", "01", "11"],  
      ["11", "00", "01", "00"],  
      ["10", "01", "00", "11"]]

# Fonction de permutation
def permutation(bits, table):
    return ''.join(bits[i - 1] for i in table)

# Fonction de décalage circulaire à gauche
def left_shift(bits, n):
    return bits[n:] + bits[:n]

# Génération des clés K1 et K2
def generate_keys(key):
    print("---Génération des sous-clés K1 et K2 avec affichage des étapes---")

    P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
    P8 = [6, 3, 7, 4, 8, 5, 10, 9]

    key = permutation(key, P10)
    print(f"Clé après P10 : {key}")

    left, right = key[:5], key[5:]
    print(f"Gauche (L0)    : {left}")
    print(f"Droite (R0)    : {right}")

    left, right = left_shift(left, 1), left_shift(right, 1)
    print(f"Après LS-1 (L1): {left}")
    print(f"Après LS-1 (R1): {right}")

    K1 = permutation(left + right, P8)
    print(f"Clé K1         : {K1}")

    left, right = left_shift(left, 2), left_shift(right, 2)
    print(f"Après LS-2 (L2): {left}")
    print(f"Après LS-2 (R2): {right}")

    K2 = permutation(left + right, P8)
    print(f"Clé K2         : {K2}")

    return K1, K2

# Substitution S-Box
def sbox_substitution(bits, sbox):
    row = int(bits[0] + bits[3], 2)
    col = int(bits[1] + bits[2], 2)
    return sbox[row][col]

# Fonction de Feistel
def feistel_function(bit_string, round_key):

    left, right = bit_string[:4], bit_string[4:]
    print(f"Entrée Feistel : L = {left}, R = {right}")

    # Étape 1 : Expansion/Permutation sur R
    expanded_right = permutation(right, EP)
    print(f"Expansion/Permutation E/P : {expanded_right}")


    # Étape 2 : XOR avec la clé de round
    xor_result = format(int(expanded_right, 2) ^ int(round_key, 2), '08b')
    print(f"XOR avec la clé de round : {xor_result}")

    # Étape 3 : Substitution avec S-Boxes
    left_sbox_out = sbox_substitution(xor_result[:4], S0)
    right_sbox_out = sbox_substitution(xor_result[4:], S1)
    sbox_output = left_sbox_out + right_sbox_out
    print(f"Substitution S-Boxes : S0 = {left_sbox_out}, S1 = {right_sbox_out}, Résultat = {sbox_output}")

     # Étape 4 : Permutation P4
    p4_result = permutation(sbox_output, P4)
    print(f"Permutation P4 : {p4_result}")

    # Étape 5 : XOR avec L
    new_right = ''.join(str(int(left[i]) ^ int(p4_result[i])) for i in range(4))
    print(f"XOR avec L : {new_right}")

    print(f"Résultat round Feistel : L = {right}, R = {new_right}")
    
    return new_right ,  right

# Fonction de chiffrement MiniDES
def miniDES_encrypt(plaintext, key):
    print("---Le chiffrement DES de text : " , plaintext)

    print("---La génération des clés---")
    K1, K2 = generate_keys(key)
    print("la clé K1 : " , K1)
    print("la clé K2 :  " , K2)

    # 2. Permutation Initiale (IP)
    permuted_text = permutation(plaintext, IP) 
    print(f"Permutation Initiale (IP) : {permuted_text}")

    # 3. Premier round de Feistel avec K1
    L1, R1 = feistel_function(permuted_text, K1)
    swiched = R1 + L1 
    print(f"Après Round 1 (switch) : {swiched}") 

    # 4. Deuxième round de Feistel avec K2 
    L2, R2 = feistel_function(swiched, K2)

    # 5. Permutation Inverse (IP⁻¹)
    final_ciphertext = permutation(L2 + R2, IP_inv)
    print(f"Texte chiffré après IP⁻¹ : {final_ciphertext}")

    return final_ciphertext 

# Fonction de déchiffrement MiniDES
def miniDES_decrypt(ciphertext, key):
    print(f"\nDéchiffrement du texte : {ciphertext}")

    K1, K2 = generate_keys(key)

    # Étape 1 : Appliquer IP
    permuted = permutation(ciphertext, IP)
    print(f"Après IP       : {permuted}")    

     
    print("---Premier Round DE Fiestel") 
    L2, R2 = feistel_function(permuted, K2) 
    
    
    swapped = R2 + L2                

    print("---Deuxième Round De Feistel") 
    L0, R0 = feistel_function(swapped, K1)

    perm = permutation(L0 + R0, IP_inv) 
    print("Le résultat de la permutation inverse (text déchiffré) : " , perm)

    return perm  


# Exemple d'utilisation
plaintext = "01110010"
key = "1010000010"

ciphertext = miniDES_encrypt(plaintext, key)
decrypted_text = miniDES_decrypt(ciphertext, key)


print(f"Texte en clair   : {plaintext}")
print(f"Texte chiffré    : {ciphertext}")
print(f"Texte déchiffré  : {decrypted_text}") 


