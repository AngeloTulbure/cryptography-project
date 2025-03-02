#  ElGamal Software implementation with ECB ciphering mode

## Overview

This project implements the **ElGamal cryptosystem** for encryption and decryption, using the **Electronic Code Book (ECB)** mode for ciphering. The implementation also explores the **Cipher Block Chaining (CBC)** mode, though the decryption for CBC is not fully operational in this version.

## Features

- Implementation of the ElGamal cryptosystem for secure communication.
- Encryption and decryption using **ECB mode**.
- Key generation, encryption, and decryption functions.
- Partial implementation of **CBC mode** (encryption works, decryption is incomplete).

## How It Works

### ElGamal Cryptosystem

1. **Key Generation**:
   - Generates a public-private key pair.
   - Public key: `(p, g, y)`, where `p` is a prime number, `g` is a generator, and `y = g^x mod p`.
   - Private key: `x`, a random integer.

2. **Encryption**:
   - The sender uses the receiver's public key to encrypt the message into ciphertext.

3. **Decryption**:
   - The receiver uses their private key to decrypt the ciphertext back to plaintext.

### Ciphering Modes

- **ECB Mode**: 
  - Each block of plaintext is encrypted independently, making it simple and efficient.
- **CBC Mode**:
  - Uses an initialization vector (IV) and XORs it with the plaintext before encryption. Decryption involves reversing this process.


