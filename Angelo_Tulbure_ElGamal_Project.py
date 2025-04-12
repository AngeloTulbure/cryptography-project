#!/usr/bin/env python3
import random
from math import pow

# Modular exponentiation function (a^b mod c)
def power(a, b, c):
    x = 1
    y = a
 
    while b > 0:
        if b % 2 != 0:  # If b is odd, multiply x by y
            x = (x * y) % c
        y = (y * y) % c  # Square y
        b = int(b / 2)    # Integer division by 2
 
    return x % c

# Basic ElGamal encryption (multiplicative)
def encrypted_elgamal(message, g_power_ab): 
    return (g_power_ab * message)

# Basic ElGamal decryption (division)
def decrypted_elgamal(en_msg, g_power_ab):
    return int(en_msg / g_power_ab)

# Electronic Codebook (ECB) mode encryption
def encrypt_ECB(message, g_power_ab):
    c = []  # Initialize ciphertext list

    # Convert each character to its ASCII value
    for i in range(0, len(message)):
        c.append(message[i])
    
    # Encrypt each ASCII value using ElGamal
    for i in range(0, len(c)):
        c[i] = encrypted_elgamal(ord(c[i]), g_power_ab)
       
    return c

# ECB mode decryption
def decrypt_ECB(en_msg, h):
    dr_msg = []  # Initialize decrypted message list

    # Prepare list with zeros
    for i in range(0, len(en_msg)):
        dr_msg.append(0)

    # Decrypt each value and convert back to character
    for i in range(0, len(en_msg)):
        dr_msg[i] = chr(decrypted_elgamal(en_msg[i], h)) 
    
    return dr_msg

# Cipher Block Chaining (CBC) mode encryption
def encrypt_CBC(plain_text, key, iv):
    c = []  # Initialize ciphertext list

    # Convert each character to ASCII value
    for i in range(0, len(plain_text)):
        c.append(1)
        c[i] = ord(plain_text[i])  # from char to int

    # XOR first block with initialization vector (IV)
    c[0] = c[0] ^ iv  # scramble it

    # Chain encryption: each block depends on previous ciphertext
    for i in range(0, (len(c) - 1)):
        c[i] = encrypted_elgamal(c[i], key)
        c[i+1] = c[i+1] ^ c[i]  # XOR next plaintext with current ciphertext

    # Encrypt last block
    c[len(c) - 1] = encrypted_elgamal(c[len(c) - 1], key)

    return c

# CBC mode decryption
def decrypt_CBC(cipher_text, key, iv, p):
    de_msg = []       # Intermediate decrypted values
    plain_text = []    # Final plaintext characters

    # Initialize lists
    for i in range(0, len(cipher_text)):
        de_msg.append(0)
        plain_text.append('a')
        de_msg[i] = decrypted_elgamal(cipher_text[i], key)

    print("key = ", key, "ciphertext[2] = ", cipher_text[2])

    # First block uses IV for XOR
    plain_text[0] = chr(iv ^ de_msg[0]) 
    print(0, plain_text[0])

    # Subsequent blocks use previous ciphertext for XOR
    for i in range(1, len(cipher_text)):
        print(i, cipher_text[i-1], de_msg[i], cipher_text[i-1] ^ de_msg[i])
        plain_text[i] = chr(cipher_text[i-1] ^ de_msg[i]) 

    return plain_text

# Greatest Common Divisor (Euclidean algorithm)
def gcd(a, b):
    if a < b:
        return gcd(b, a)
    elif a % b == 0:
        return b
    else:
        return gcd(b, a % b)
 
# Generate a random key coprime with p
def gen_key(p):
    key = random.randint(pow(10, 20), p)
    while gcd(p, key) != 1:  # Ensure key is coprime with p
        key = random.randint(pow(10, 20), p)
    return key

def main():
    print("Please enter a string to be encrypted: ")
    message = input()
    
    # Generate large prime p and generator g
    p = random.randint(pow(10, 20), pow(10, 50))
    g = random.randint(2, p - 1)
 
    print("\nIn the field: ", p, "\nwe found a the generator: ", g)
    
    # Receiver's key pair (private key a, public key g^a mod p)
    rec_key = gen_key(p)  # Private key for receiver (a)
    g_power_a = power(g, rec_key, p) 
    print("the public key: ", rec_key)
    print("g to the power of a: ", g_power_a)

    # Sender's key pair (private key b, public key g^b mod p)
    send_key = gen_key(p)  # Private key for sender (b)
    g_power_b = power(g, send_key, p)
    print("the private key: ", send_key)
    print("g to the power b: ", g_power_b)

    # Shared secret (g^(ab) mod p)
    g_power_ab = power(g_power_a, send_key, p)
    print("g to the power of ab:", g_power_ab, "\n")

    # Currently only ECB mode is implemented and used
    # ECB mode encryption and decryption
    cipher_text = encrypt_ECB(message, g_power_ab)
    print("We used ECB cipher mode to break up the message, into smaller parts, and encrypt every part individually")
    print("This is our encrypted message: ", cipher_text, "\n")
    plain_text = decrypt_ECB(cipher_text, g_power_ab)
    dmsg = ''.join(plain_text)
    print("This is our decrypted message: ", dmsg)
    
    # The CBC mode code is commented out but would work similarly
    # else:
    #     # CBC
    #     iv = random.randint(1, 2000000)
    #     cipher_text = encrypt_CBC(message, g_power_ab, iv)     
    #     plain_text = decrypt_CBC(cipher_text, g_power_ab, iv, p)
    #     dmsg = ''.join(plain_text)
    #     print(dmsg)

if __name__ == "__main__":
    main()
