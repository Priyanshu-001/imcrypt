from Stratergies.Blueprint import Stratergy
from Stratergies.Algo import AES


class AESStratergy(Stratergy):
    def encrypt(self, imgname,password):
        image=self.imgRead(imgname)
        encrypted_image = AES.encrypt(image,password)
        name = self.imgWrite(encrypted_image, imgname)
        self.logger(f'saved image as {name}')
    def decrypt(self,imgname,password ):
        image = self.imgRead(imgname)
        decrypted_image = AES.decrypt(image,password)
        name = self.imgWrite(decrypted_image,imgname)
        self.logger(f'saved image as {name}')