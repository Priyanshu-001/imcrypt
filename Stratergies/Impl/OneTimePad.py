from Stratergies.Blueprint import Stratergy
from Stratergies.Algo import OneTimePad
class OneTimePadStratergy(Stratergy):
    def encrypt(self, imgname):
        image=self.imgRead(imgname)
        image,key=OneTimePad.encrypt(image)
        name=self.imgWrite(image,imgname) 
        self.logger(f'saved image as {name}')
        name=self.imgWrite(key,'key-'+imgname) 
        self.logger(f'saved key as {name}')
    def decrypt(self, imgname,key):
        image=self.imgRead(imgname) 
        keyImage = self.imgRead(key)
        image=OneTimePad.decrypt(image,keyImage)
        name = self.imgWrite(image,imgname)
        self.logger(f'saved image as {name}')

