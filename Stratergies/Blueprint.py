import abc
class Stratergy(metaclass=abc.ABCMeta):
    
   
    def __init__(self,imgRead:'function',imgWrite:'function',logger:'function') -> None:
        self.imgRead = imgRead
        self.imgWrite = imgWrite
        self.logger = logger

    @abc.abstractmethod
    def encrypt(self,**kwargs):
        pass

    @abc.abstractmethod
    def decrypt(self,**kwargs):
        pass
    