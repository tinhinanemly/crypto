import numpy as np
import string

def crypttranspo(message: str, key: str) -> str:
    key_sorted = sorted(list(key))    # trier la klé selon l'ordre alphabétique                       
    print("sorted key : " , key_sorted)
    perm = [key.index(k) for k in key_sorted]  
    print("ordre de coloone " , perm)
    num_cols = len(key)
    num_rows = int(np.ceil(len(message) / num_cols))

    
    grid = [[' ' for _ in range(num_cols)] for _ in range(num_rows)]

    
    index = 0
    for i in range(num_rows):

        for j in range(num_cols):
            if index < len(message):
                if message[index].isalpha() :    CODE
                    grid[i][j] = message[index]     
                    index += 1 
    print("grid" ,grid)
    
    cipher_text = ""
    for col in perm: # ordre de colonnes
        for row in range(num_rows):
            cipher_text += grid[row][col] 

    return cipher_text.replace(' ', '')  


# Exemple d'utilisation
message = "MESSAGE"
key = "CODE"  
chiffre = crypttranspo(message, key)
print("Message chiffré :", chiffre)




