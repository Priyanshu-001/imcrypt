import cv2
import numpy as np
import secrets
import os
import sys
import argparse
from Crypto.Cipher import AES
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
'''
contains implementation of arnold_cat/aes/1time_pad/lsb steganography 
NOTE: destroys meta data during any operation
'''
def stegano_write(img,msg):
	'''
	An implementation of lsb steganography the last 1 bit is altered '\0' is used as a delimeter here 
	stores 1 bit of msg per byte of image
	works with ascii charaters only 

	'''
	#flattens the array and chages the last bit of each element to the msg
	msg=msg+"\0"#the delimter charater
	img_shape = img.shape
	nPixels= img_shape[0]*img_shape[1]*img_shape[2]
	if len(msg)*8>nPixels:
		raise Exception(f'image is not big enough to store this msg this image can store atmost {nPixels//8 -1} chars')
	
	ctr=0
	img=img.reshape(nPixels)
	msg=[ord(x) for x in msg]#text to ascii conversion 

	for a in msg:
		i=8#for every char in msg 
		while i: #for each bit in the data 
			i-=1
			b=a>>i#starts from MSB of the MSG 
			if b&1:#a|1 will change only the last bit to 1
				img[ctr] = img[ctr] | 1
			else:
				#254 = 11111110  
				img[ctr] = img[ctr] & 254 # only last bit is set to 0 other bits remains the same
			ctr+=1
	return img.reshape(img_shape)

def stegano_read(img):
	'''
	searches for delimter '\0' extracts 1 bit of msg per 8 bytes of image assembles them as ascii codes and convert them back to char 
	'''
	img_shape = img.shape
	nPixels= img_shape[0]*img_shape[1]*img_shape[2]
	img = img.reshape(nPixels)
	nPixels=nPixels -nPixels%8
	wordList=[]
	b=''
	msg_found = 0
	for a in range(1,nPixels+1):

		if a%8 == 0:
			wordList.append(b)
			if int(b,2) == 0:
				msg_found = 1
				break
			b=''
		b+=str(img[a]%2)
	msg = [chr(int(x,2)) for x in wordList]
	msg = ''.join(msg)
	if msg_found == 0:
		msg= "no message found!!"
	return msg

		


	
def aes_en(img,key):
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

def aes_de(img,key):
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

def arnold_cat_en(img):
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

def arnold_cat_de(img):
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



def decompose(path):
	'''
	decompose imagename as path+imagename+format
	'''
	path=os.path.abspath(path)
	upper=''
	if "\\" not in path:
		upper=''
		exe = str(path.split('.')[-1])
		img_name = path.split('.')[0:-1]
		
	else:
		upper=(path.split("\\")[0:-1])
		upper ="\\".join(upper)
		img_name = path.split('\\')[-1]
		exe = str(img_name.split('.')[-1])
		img_name = img_name.split('.')[0:-1]
	img_name = '.'.join(img_name)
	exe=exe.lower()
	return (upper,img_name, exe)

	
def safeSave(img,I,override='ask',delete_jpg=False,end=''):
	'''
	attempts to save img with given name imgname
	jpg or jpeg are not allowed to be saved 
	'''
	
	path,imgname,exe=decompose(I)
	if (exe.lower() == 'jpg') | (exe.lower() == 'jpeg'):
		
		
		I = path+'\\'+imgname+'.'+'webp'
		safeSave(img,I,override,True,exe)

	
	if override=='yes':
		try:
			cv2.imwrite(I,img)
			if delete_jpg:
				os.remove(path+'\\'+imgname+'.'+end)

			return I
		except Exception as e:
			raise e
		

	elif os.path.isfile(I) & (override=='ask'):
		arg2=str(input(f'{name} already exsists in {path} override? [Y/n]')).lower()

		if(not(arg2=="y" or arg2=="n")):#invalid case
			print('Please choose from given opts only')
			return safeSave(img,I,override)
		elif arg2=='n':#override
			return safeSave(img,I,'no')
		else:#dont override
			return safeSave(img,I,'yes')

	elif(override=='no'):#dont override
		
		while(os.path.isfile(I)):
			imgname=input(f"Enter new name ({I} already exists)")
			I=path+'\\'+imgname+'.'+exe
		return safeSave(img, I,'yes')
	elif override=='ask':#and imgname doesn't exists
		return safeSave(img, I,'yes')
	else:
		return (0,"Invalid state",'')


def read_image(path):
	'''
	read image and catch any execeptions
	'''
	if os.path.isfile(path)==False:
		raise Exception("File not found or the program doesn't have required permissions")

	try:
		img = cv2.imread(path)
	except Exception as e:
		raise e
	else:
		return img


def encry(img1):
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
	
	
	

def decry(img=None,key=None):
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

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description="IMCrypt v-0.0.1")
	parser.add_argument('mode',help="1time_pad_en/1time_pad_de for encryption/decryption through one time pad",choices=['1time_pad_en','1time_pad_de','arnold_cat','arnold_cat_de','aes_en','aes_de','stegsno_write','stegano_read'])
	parser.add_argument('--image','-i',required=True,help='Image address ')
	parser.add_argument('--message','-m',required='stegano_write' in sys.argv, help = 'message to be hidden in image')
	parser.add_argument('--key', '-k' ,help='Name of the existing key in 1time_pad_de/no of iterations in arnold_cat ', required = bool('arnold_cat' in sys.argv) |bool('arnold_cat_de' in sys.argv )| bool('1time_pad_de' in sys.argv)  )
	parser.add_argument('--password','-p',help='password in aes encryption', required=bool('aes_en' in sys.argv) | bool('aes_de' in sys.argv))

	args = parser.parse_args()
	if args.mode=='1time_pad_en':
		imgname = args.image
		image=read_image(imgname)
		image,key=encry(image)
		name=safeSave(image,imgname,'yes')#override 
		print(f'saved image as {name}')
		path,keyname,formatt=decompose(imgname)#format is a keyword
		name=safeSave(key,path+'\\'+'key-'+keyname+'.'+formatt) 
		print(f'saved key as {name}')
		
	elif args.mode=='1time_pad_de':
		imgname = args.image
		keyname = args.key
		image=read_image(imgname) 
		key = read_image(keyname)
		image=decry(image,key)
		name = safeSave(image,imgname,'yes')
		print(f'saved image as {name}')

	elif args.mode == 'arnold_cat':
		imgname = args.image
		key = int(args.key)
		image=read_image(imgname)
		
		for k in range(key): 
			image=arnold_cat_en(image)
		name = safeSave(image,imgname,'yes')
		print(f'saved image as {name}')

	elif args.mode == 'arnold_cat_de':
		imgname = args.image
		key = int(args.key)
		image=read_image(imgname)
		for k in range(key):
			image=arnold_cat_de(image)
		name = safeSave(image,imgname,'yes')
		print(f'saved image as {name}')

	elif args.mode == 'aes_en':
		image=read_image(args.image)
		encrypted_image = aes_en(image,args.password)
		name = safeSave(encrypted_image, args.image,'yes')
		print(f'saved image as {name}')

	elif args.mode == 'aes_de':
		image = read_image(args.image)
		decrypted_image = aes_de(image,args.password)
		name = safeSave(decrypted_image,args.image,'yes')
		print(f'saved image as {name}')

	elif args.mode == 'stegano_write':
		image = read_image(args.image)
		image = stegano_write(image,args.message)

		name = safeSave(image,args.image,'yes')
		print(f'saved image as {name}')

	elif args.mode == 'stegano_read':
		image = read_image(args.image)
		msg = stegano_read(image)
		print(msg)

	
