// rijndael.h
#ifndef RIJNDAEL_H
#define RIJNDAEL_H

#include <stdint.h>

#define BLOCK_SIZE 16
#define NUM_ROUNDS 10

// Fonctions principales
unsigned char *aes_encrypt_block(const unsigned char *plaintext, const unsigned char *key);
unsigned char *aes_decrypt_block(const unsigned char *ciphertext, const unsigned char *key);

// Fonctions internes
void sub_bytes(unsigned char *block);
void shift_rows(unsigned char *block);
void mix_columns(unsigned char *block);
void add_round_key(unsigned char *block, const unsigned char *key);  // Ajout de 'const'
unsigned char *expand_key(const unsigned char *cipher_key);          // Ajout de 'const'

#endif