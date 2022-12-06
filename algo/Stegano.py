def encrypt(img,msg):
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

def decrypt(img):
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
