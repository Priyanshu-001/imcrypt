from Stratergies.Blueprint import Stratergy
from Stratergies.Algo import Stegano

class SteganoStratergy(Stratergy):
    def encrypt(self, imgname,message):
        image = self.imgRead(imgname)
        image = Stegano.encrypt(image,message)
        name = self.imgWrite(image,imgname,'yes')
        self.logger(f'saved image as {name}')

    def decrypt(self, imgname):
        image = self.imgRead(imgname)
        msg = Stegano.decrypt(image)
        self.logger(msg)
        return {msg:msg}

