import numpy as np
import secrets	
import cv2


def encrypt(img1):
	'''
	generates an key image containning composed of random noise

	'''
	if type(img1) !=np.ndarray or img1.shape[2]!=3:
		raise Exception("image in incorrect format or is invalid")

	h,w,_=img1.shape
	key=np.zeros((h,w,3),np.uint8)
	key = [[[secrets.randbelow(256) for i in range(3)]for j in range(w)]for k in range(h) ]
	key=np.asarray(key,np.uint8)
	
	try:
		encrypted_image = cv2.bitwise_xor(img1,key)
	except Exception as e:
		raise e
		
	else:
		return (encrypted_image,key) 


	
	

def decrypt(img=None,key=None):
	if type(img) !=np.ndarray or img.shape[2]!=3:
		raise Exception("image in incorrect format or is invalid")
	elif type(key) !=np.ndarray or key.shape[2]!=3:
		raise Exception("the key in incorrect format or is invalid")
	elif img.shape != key.shape:
		raise Exception("This is not a valid image - key pair or the img/key has been cropped")


	try:
		decrypted_img = cv2.bitwise_xor(img,key)
	except Exception as e:
		raise e
	else:
		return decrypted_img

