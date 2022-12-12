import numpy as np

def encrypt(img):
	'''
	arnold_cat maps a pixel with cordinates at position (x1,y1) to  another position (x2,y2) 
	below implementation works only with square images
	any rectangular image is padded to become square
	'''
	h,w,_=img.shape
	n=max(h,w)
	encrypted_image = np.zeros([n,n,3])
	padding = ((0,n-h),(0,n-w),(0,0))
	img=np.pad(img,padding,mode='constant', constant_values=255)
	
	for x in range(n):
		for y in range(n):
			encrypted_image[x][y]=img[(2*x+y)%n][(y+x)%n]

		
	return encrypted_image

def decrypt(img):
	'''
	inverse of arnold_cat_en function 
	'''
	h,w,_=img.shape
	decrypted_image = np.zeros([h,w,3])
	#rectangular images are not allowed 
	if h!=w:
		raise Exception("Expected a square image")

	for x in range(h):
		for y in range(h):
			decrypted_image[x][y]=img[(x-y)%h][((2*y)-x)%h]

	img=decrypted_image
	return decrypted_image

