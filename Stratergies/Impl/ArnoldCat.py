from Stratergies.Blueprint import Stratergy
from Stratergies.Algo import ArnoldCat
class ArnoldCatStratergy(Stratergy):
   
    def encrypt(self,key:int,imgname:str):
        key = int(key)
        image=self.imgRead(imgname)
        for k in range(key): 
            image=ArnoldCat.encrypt(image)
        name = self.imgWrite(image,imgname)
        self.logger(f'img saved as {name}')
       

    def decrypt(self,key:int,imgname:str):
        key = int(key)
        image=self.imgRead(imgname)
        for k in range(key):
            image=ArnoldCat.decrypt(image)
        name = self.imgWrite(image,imgname,'yes')
        self.logger(f'img saved as {name}')


