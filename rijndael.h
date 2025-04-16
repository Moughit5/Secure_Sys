/*
 * AES-128 Header
 * Author: [Your Name] - [Student Number]
 * Description: Interface declarations for AES 128-bit encryption and decryption.
 */

 #ifndef RIJNDAEL_H
 #define RIJNDAEL_H
 
 #define BLOCK_SIZE 16
 #define BLOCK_ACCESS(block, row, col) (block[(row * 4) + col])
 
 unsigned char *aes_encrypt_block(unsigned char *plaintext, unsigned char *key);
 unsigned char *aes_decrypt_block(unsigned char *ciphertext, unsigned char *key);
 
 void sub_bytes(unsigned char *block);
 void shift_rows(unsigned char *block);
 void mix_columns(unsigned char *block);
 
 void invert_sub_bytes(unsigned char *block);
 void invert_shift_rows(unsigned char *block);
 void invert_mix_columns(unsigned char *block);
 
 void add_round_key(unsigned char *block, unsigned char *round_key);
 unsigned char *expand_key(unsigned char *cipher_key);
 
 #endif
 