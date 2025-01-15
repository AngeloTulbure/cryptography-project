#!/usr/bin/env python3
import random
from math import pow

def power(a, b, c):
    x = 1
    y = a
 
    while b > 0:
        if b % 2 != 0:
            x = (x * y) % c;
        y = (y * y) % c
        b = int(b / 2)
 
    return x % c

def encrypted_elgamal(message, g_power_ab): 
    return (g_power_ab * message)

def decrypted_elgamal(en_msg, g_power_ab):
    return int(en_msg / g_power_ab)

def encrypt_ECB(message, g_power_ab):
    c = []

    for i in range(0, len(message)):
        c.append(message[i])
    
    for i in range(0, len(c)):
        c[i] = encrypted_elgamal(ord(c[i]), g_power_ab)
       
    return c

def decrypt_ECB(en_msg, h):
    dr_msg = []

    for i in range(0, len(en_msg)):
        dr_msg.append(0)

    for i in range(0, len(en_msg)):
        dr_msg[i] = chr(decrypted_elgamal(en_msg[i], h)) 
    
    return dr_msg


def encrypt_CBC(plain_text, key, iv):
    c = []

    for i in range(0, len(plain_text)):
        c.append(1)
        c[i] = ord(plain_text[i]) #from char to int

    c[0] = c[0] ^ iv  #scrable it

    for i in range(0, (len(c) - 1)):
        c[i] = encrypted_elgamal(c[i], key)
        c[i+1] = c[i+1] ^ c[i]

    c[len(c) - 1] = encrypted_elgamal(c[len(c) - 1], key)

    return c

def decrypt_CBC(cipher_text, key, iv, p):
    de_msg = []
    plain_text = []

    for i in range(0, len(cipher_text)):
        de_msg.append(0)
        plain_text.append('a')
        de_msg[i] = decrypted_elgamal(cipher_text[i], key)

    print("key = ", key, "ciphertext[2] = ", cipher_text[2])

    plain_text[0] = chr(iv ^ de_msg[0]) 
    print(0, plain_text[0])

    for i in range(1, len(cipher_text)):
        print(i, cipher_text[i-1], de_msg[i], cipher_text[i-1] ^ de_msg[i])
        plain_text[i] = chr(cipher_text[i-1] ^ de_msg[i]) 

    return plain_text

def gcd(a, b):
    if a < b:
        return gcd(b, a)
    elif a % b == 0:
        return b;
    else:
        return gcd(b, a % b)
 
# Generating large random numbers
def gen_key(p):
 
    key = random.randint(pow(10, 20), p)
    while gcd(p, key) != 1:
        key = random.randint(pow(10, 20), p)
 
    return key

def main():
    print("Please enter a string to be encrypted: ")
    message = input()
    
    p = random.randint(pow(10, 20), pow(10, 50))
    g = random.randint(2, p - 1)
 
    print("\nIn the field: ", p, "\nwe found a the generator: ", g)
    rec_key = gen_key(p) # Private key for receiver # a
    g_power_a = power(g, rec_key, p) 
    print("the public key: ", rec_key)
    print("g to the power of a: ", g_power_a)

    send_key = gen_key(p)# Private key for sender # b
    g_power_b = power(g, send_key, p)
    print("the private key: ", send_key)
    print("g to the power b: ", g_power_b)

    g_power_ab = power(g_power_a, send_key, p)
    print("g to the power of ab:", g_power_ab, "\n")

    #print("Please choose a ciphering mode:\n1 ECB\n2 CBC")
    #cipher_mode = input()

    #if cipher_mode == "1":
    
    # ECB
    cipher_text = encrypt_ECB(message, g_power_ab)
    print("We used ECB cipher mode to break up the message, into smaller parts, and encrypt every part individually")
    print("This is our encrypted message: ", cipher_text, "\n")
    plain_text = decrypt_ECB(cipher_text, g_power_ab)
    dmsg = ''.join(plain_text)
    print("This is our decrypted message: ", dmsg)
    
    # else:
    #     # CBC
    #     iv = random.randint(1, 2000000)
    #     cipher_text = encrypt_CBC(message, g_power_ab, iv)     

    #     plain_text = decrypt_CBC(cipher_text, g_power_ab, iv, p)
    #     dmsg = ''.join(plain_text)
    #     print(dmsg)

if __name__ == "__main__":
    main()
