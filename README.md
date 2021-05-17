# imcrypt
image encryption cli tool, supports the following operations

AES encrytion/decryption 


Encryption/decryption using Arnold's cat map


Encryption/decryption using one time pad


LSB steganography


# USAGE



usage: python imcrypt.py [-h] --image IMAGE [--message MESSAGE] [--key KEY]
                  [--password PASSWORD] MODE
                  
                  
MODE can be any one of these {1time_pad_en,1time_pad_de,arnold_cat,arnold_cat_de,aes_en,aes_de,stegsno_write,stegano_read}


-- image. -i image to encrypted


-- messsage, -m message to be hidden in image(for steganography mode)


-- key, -k address of key image for one time pad or number of iterations for Arnold's cat map


-- password, -p password for aes mode




# MODES


**1time_pad_en,1time_pad_de** - Generates a randomly generated key and performs xor with the orginal image to create encrypted image, the key and the encrypted image both are required for decryption


**arnold_cat,arnold_cat_de** - a chaotic map that maps a pixel at (x,y) to (2x+y,x+y)mod n the current implementation work only for square images, any rectangular image will be padded as a square.


**stegsno_write,stegano_read** - Implementation of LSB-steganography.



**aes_en,aes_de** - standard AES implementation 

