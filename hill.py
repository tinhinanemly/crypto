import numpy as np

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Fonction pour transformer une lettre en un indice
def lettre_to_num(lettre):
    return alphabet.index(lettre.upper())

# Fonction pour transformer un indice en une lettre
def num_to_lettre(num):
    return alphabet[num]


# Fonction pour vérifier si une matrice est inversible (determinant != 0 mod 26)
def est_inversible(matrice):
    determinant = int(np.linalg.det(matrice)) % 26
    return determinant != 0 

# Fonction de chiffrement de Hill
def chiffrement_hill(texte_clair, matrice_cle):
    if not est_inversible(matrice_cle):
        raise ValueError("La matrice de chiffrement n'est pas inversible (déterminant nul).")
    
    # Convertir le texte clair en indices numériques
    texte_clair = [lettre_to_num(c) for c in texte_clair if c.isalpha()] 

    # Si le nombre de lettres est impair, ajouter un 'X'
    if len(texte_clair) % 2 != 0:
        texte_clair.append(lettre_to_num('X'))
    
    texte_chiffre = []

    # Chiffrement du texte
    for i in range(0, len(texte_clair), 2):
        bloc = np.array(texte_clair[i:i+2]).reshape(2, 1)
        chiffre_bloc = np.dot(matrice_cle, bloc) % 26
        texte_chiffre.extend(chiffre_bloc.flatten().astype(int)) # matrice col => matrice ligne
        print(bloc )
    # Convertir les résultats en lettres
    texte_chiffre = ''.join(num_to_lettre(num) for num in texte_chiffre)
    return texte_chiffre

# Exemple d'utilisation
texte_clair = "l! ettre"
matrice_cle = np.array([[5, 8], [17, 3]])

# Chiffrement du texte
try:
    texte_chiffre = chiffrement_hill(texte_clair, matrice_cle)
    print(f"Texte chiffré : {texte_chiffre}")
except ValueError as e:
    print(e)


def mod_inverse(a):
    
    for x in range(1, 26):
        if (a * x) % 26 == 1:  
            return x
    return None

def inverse_matrix(A):
    
    # Calcul du déterminant de la matrice A mod 26
    det = int(np.linalg.det(A)) % 26
   

    
    if det == 0:
        raise ValueError("La matrice n'est pas inversible car le déterminant est nul mod 26.")

    # Calcul de l'inverse du déterminant mod 26
    det_inv = mod_inverse(det)
    
    
    # Calcul de la matrice la matrice des cofacteurs transposée
    adj = np.array([[A[1][1], -A[0][1]], [-A[1][0], A[0][0]]])
    adj = adj % 26

    # Multiplication de l'adjointe par l'inverse du déterminant modulo 26
    inv_A = (det_inv * adj) % 26
    return inv_A


def dechiffrement_hill(ciphertext, key_matrix):
    try:
        
        key_inv = inverse_matrix(key_matrix)
    except ValueError as e:
        print(e)  
        return ""  

    
    ciphertext_nums = [lettre_to_num(c) for c in ciphertext]
    cipher_blocks = np.array(ciphertext_nums).reshape(-1, 2).T

    plaintext_nums = []

    for i in range(0, len(ciphertext_nums), 2):
        block = np.array(ciphertext_nums[i:i+2]).reshape(2, 1)
        decrypted_block = np.dot(inverse_matrix(key_matrix), block) % 26
        plaintext_nums.extend(decrypted_block.flatten().astype(int))
    
    texte_déchiffré = ''.join(num_to_lettre(num) for num in plaintext_nums)
    return texte_déchiffré 

     


key = np.array([[5, 8], [17, 3]])
ciphertext = "JRNQNP"  
plaintext = dechiffrement_hill(ciphertext, key)
print("Texte déchiffré :", plaintext)
