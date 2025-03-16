import random
import hashlib
import math
from sympy import isprime, mod_inverse

def generate_prime(bits=16):
    """Génère un nombre premier aléatoire de la taille spécifiée en bits."""
    while True:
        num = random.getrandbits(bits)
        if isprime(num):
            return num

def generate_keys(bits=16):
    """Génère les clés publique et privée pour RSA."""
    p = generate_prime(bits)
    q = generate_prime(bits)
    while p == q:
        q = generate_prime(bits)
    
    n = p * q
    phi = (p - 1) * (q - 1)
    
    e = random.randint(2, phi - 1)
    while math.gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)
    
    d = mod_inverse(e, phi)
    
    return (n, e), (n, d)

def modular_exponentiation(base, exponent, modulus):
    """Calcule (base^exponent) % modulus efficacement."""
    result = 1
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent //= 2
    return result

def encrypt(message, public_key):
    """Chiffre une chaîne de caractères avec la clé publique."""
    n, e = public_key
    return [modular_exponentiation(ord(char), e, n) for char in message]

def decrypt(ciphertext, private_key):
    """Déchiffre une liste de nombres en une chaîne de caractères avec la clé privée."""
    n, d = private_key
    return "".join(chr(modular_exponentiation(char, d, n)) for char in ciphertext)

def sign(message, private_key):
    """Génère une signature RSA pour un message donné."""
    n, d = private_key
    hashed = int(hashlib.sha256(message.encode()).hexdigest(), 16) % n  # Hash modulo n
    return modular_exponentiation(hashed, d, n)

def verify(message, signature, public_key):
    """Vérifie une signature RSA."""
    n, e = public_key
    hashed = int(hashlib.sha256(message.encode()).hexdigest(), 16) % n
    decrypted_hash = modular_exponentiation(signature, e, n)
    return hashed == decrypted_hash

# Exemple d'utilisation
public_key, private_key = generate_keys(bits=16)
message = "Hello RSA"

# Chiffrement & déchiffrement
ciphertext = encrypt(message, public_key)
decrypted_message = decrypt(ciphertext, private_key)

# Signature & vérification
signature = sign(message, private_key)
verification = verify(message, signature, public_key)

print(f"Clé publique: {public_key}")
print(f"Clé privée: {private_key}")
print(f"Message original: {message}")
print(f"Message chiffré: {ciphertext}")
print(f"Message déchiffré: {decrypted_message}")
print(f"Signature: {signature}")
print(f"Vérification de la signature: {verification}")
