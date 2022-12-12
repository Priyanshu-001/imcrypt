import cv2
import os
import sys
import argparse
from Engine import Engine

'''
contains implementation of arnold_cat/aes/1time_pad/lsb steganography 
NOTE: destroys meta data during any operation
'''
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

	
def safeSave(img,I,override='yes',delete_jpg=False,end=''):
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
		arg2=str(input(f'{imgname} already exsists in {path} override? [Y/n]')).lower()

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

if __name__ == '__main__':
	
	parser = argparse.ArgumentParser(description="IMCrypt v-0.0.1")
	parser.add_argument('mode',help="1time_pad_en/1time_pad_de for encryption/decryption through one time pad",choices=['1time_pad_en','1time_pad_de','arnold_cat','arnold_cat_de','aes_en','aes_de','stegano_write','stegano_read'])
	parser.add_argument('--imgname','--image','-i',required=True,help='Image address ')
	parser.add_argument('--message','-m',required='stegano_write' in sys.argv, help = 'message to be hidden in image')
	parser.add_argument('--key', '-k' ,help='Name of the existing key in 1time_pad_de/no of iterations in arnold_cat ', required = bool('arnold_cat' in sys.argv) |bool('arnold_cat_de' in sys.argv )| bool('1time_pad_de' in sys.argv)  )
	parser.add_argument('--password','-p',help='password in aes encryption', required=bool('aes_en' in sys.argv) | bool('aes_de' in sys.argv))

	args = parser.parse_args()
	argsDict = vars(args)
	
	engine = Engine()
	engine.setImgRead(read_image).setImgWrite(safeSave).setLogger(print)
	actionMap = {
		'1time_pad_en':('OneTimePad','encrypt'),
		'1time_pad_de': ('OneTimePad','decrypt'),
		'arnold_cat': ( 'ArnoldCat','encrypt'),
		'arnold_cat_de':('ArnoldCat','decrypt'),
		'aes_en':('AES','encrypt'),
		'aes_de':('AES','decrypt'),
		'stegano_write':('Stegano','encrypt'),
		'stegano_read':('Stegano','decrypt'),
	}
	mode,op = actionMap[args.mode]
	engine.loadStratergy(mode).exe(op,**argsDict)