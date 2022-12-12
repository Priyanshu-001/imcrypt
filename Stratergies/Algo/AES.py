from Crypto.Cipher import AES
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import numpy as np


def encrypt(img,key):
	'''
	a standard implementation of aes 
	array is flattened and each byte is encoded in CFB mode
	'''
	#TODO
	#make iv and salt random for each image
	img_shape=img.shape
	salt=b'000000'
	iv='four'*4
	iv =bytes(iv,'utf-8')
	#key derivation from password
	kdf=PBKDF2HMAC(algorithm=hashes.SHA256(),
		iterations=100,
		salt=salt,
		length=24,
		backend=default_backend()
		)
	key= bytes(key, 'utf-8')
	key=kdf.derive(key)
	cipher = AES.new(key, AES.MODE_CFB,IV=iv)
	img = cipher.encrypt(img.tobytes())
	img = np.frombuffer(img,np.uint8)
	print(len(img))
	img=img.reshape(img_shape)
	return img

def decrypt(img,key):
	'''
	a standard implimentation of aes decryption
	'''
	img_shape=img.shape
	salt=b'000000'
	iv='four'*4
	iv =bytes(iv,'utf-8')

	kdf=PBKDF2HMAC(algorithm=hashes.SHA256(),
		iterations=100,
		salt=salt,
		length=24,
		backend=default_backend()
		)
	key= bytes(key, 'utf-8')
	key=kdf.derive(key)
	cipher = AES.new(key, AES.MODE_CFB,IV=iv)
	img = cipher.decrypt(img.tobytes())
	img = np.frombuffer(img,np.uint8)
	img=img.reshape(img_shape)
	return img

