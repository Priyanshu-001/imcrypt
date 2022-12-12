# imcrypt

image encryption cli tool, supports the following operations

AES encrytion/decryption 


Encryption/decryption using Arnold's cat map


Encryption/decryption using one time pad


LSB steganography
## Installation
Recommended to set up a venv first

    pip install -r requirements.txt

## USAGE



usage: python imcrypt.py [-h] --image IMAGE [--message MESSAGE] [--key KEY]
                  [--password PASSWORD] MODE
                  
                  
MODE can be any one of these {1time_pad_en,1time_pad_de,arnold_cat,arnold_cat_de,aes_en,aes_de,stegsno_write,stegano_read}


-- image. -i image to encrypted


-- messsage, -m message to be hidden in image(for steganography mode)


-- key, -k address of key image for one time pad or number of iterations for Arnold's cat map


-- password, -p password for aes mode




## CLI MODES


**1time_pad_en,1time_pad_de** - Generates a randomly generated key and performs xor with the orginal image to create encrypted image, the key and the encrypted image both are required for decryption


**arnold_cat,arnold_cat_de** - a chaotic map that maps a pixel at (x,y) to (2x+y,x+y)mod n the current implementation work only for square images, any rectangular image will be padded as a square.


**stegsno_write,stegano_read** - Implementation of LSB-steganography.



**aes_en,aes_de** - standard AES implementation 

## Examples
### arnold_cat
#### Orignal
![Arnold_cat - Copy](https://user-images.githubusercontent.com/26710303/184945901-c5cdc47f-afc7-4d52-bc95-08ae79becb13.png)

#### Encrypted with k= 37
```
python imcrypt.py arnold_cat --image Arnold_cat.png -k 37
```
![Arnold_cat](https://user-images.githubusercontent.com/26710303/184945747-a45bc762-bcd1-4f11-9236-d124a5f65a69.png)

#### Decrypted back
```
python imcrypt.py arnold_cat_de --image Arnold_cat.png -k 37
```
![Arnold_cat](https://user-images.githubusercontent.com/26710303/184946479-6595db0c-af19-457a-be02-7dc1ecfbfe98.png)

### One time Pad
#### Orignal
```
python imcrypt.py 1time_pad_en --image amg.png
```
![amg](https://user-images.githubusercontent.com/26710303/184948449-89ab8513-478d-4a66-81f5-6ce563eb69b5.png)
#### Encrypted key & image(doesn't matter what is consider image or key as xor is communatative op)
![amg](https://user-images.githubusercontent.com/26710303/184949359-674ff2f7-04d2-4493-bd3c-d705be3fedcd.png)
![key-amg](https://user-images.githubusercontent.com/26710303/184949522-3677e8ea-767c-4da6-bba0-8ef059ffff33.png)

#### Decryted
```
python imcrypt.py 1time_pad_de -i amg.png -k key-amg.png
```
![amg](https://user-images.githubusercontent.com/26710303/184950002-b9441829-cadd-4f51-a44d-39a093867ccb.png)

### AES
#### Orignal
![lab](https://user-images.githubusercontent.com/26710303/184951940-94cf3847-2c4e-4723-8d5c-f6aec7e3ec69.png)
#### Encrypted
```
python imcrypt.py aes_en -i lab.png -p "woof woof"
```
![lab](https://user-images.githubusercontent.com/26710303/184952210-edfae96f-d7cd-40e1-b14c-83ff4aff347d.png)

#### Decrypted
```
python imcrypt.py aes_de -i lab.png -p "woof woof"
```
![lab](https://user-images.githubusercontent.com/26710303/184952557-f68bb064-a6fc-4f84-8d38-e209060bfc1f.png)

## LSB Stegano with delimiter
### Write
![car.png](https://user-images.githubusercontent.com/26710303/184948449-89ab8513-478d-4a66-81f5-6ce563eb69b5.png)

```
python imcrypt.py stegano_write -i car.png -m "Hello everyone !!"
```
### Read 
![car](https://user-images.githubusercontent.com/26710303/206098737-123ad5b4-3166-4ef8-8323-9eaeeb7529ce.png)

*Image with message encoded.*
```

python imcrypt.py stegano_read -i car.png
> Hello everyone !!
```

* Download any image and try decrypted them to see the result *


## Using the engine class
for other apps that may use image encryption but don't want to use CLI the engine class provides an easy interface to do so. Where methods of i/o may be different. Eg flask backend, tkinter GUI
### Example use
```
engine = Engine()
engine.setImgRead(read_image).setImgWrite(save_img).setLogger(loggingFun)
engine.loadStratergy(stratergy).exe(operation,**kwargs)
```
Here stratergy can be
1. ArnoldCat,
2. OneTimePad,
3. AES
4. Stegano

operation can be 
1. encrypt
2. decrypt
