'''
Acts as a facde between Stratergy and user 
Loads the stratergy required dynamically and executes the request o/p 
Motiviation:
- all encyption method have series of I/O operation that must be  performed eg. reading file 
- I/O ops may be  platform dependant eg, different for CLI, server engine class lets you provide those platform sepcific ops and does the rest
'''
#TODO: prevent against timing attacks
import inspect
from warnings import warn
from Stratergies.Impl import ArnoldCat,OneTimePad,AES,Stegano

class Engine():
    @staticmethod
    def stratergies():
        return {
            'ArnoldCat':ArnoldCat.ArnoldCatStratergy,
            'OneTimePad':OneTimePad.OneTimePadStratergy,
            'AES':AES.AESStratergy,
            'Stegano':Stegano.SteganoStratergy,

        }
    def setImgRead(self,imgRead:'function') -> 'Engine':
        self.imgRead = imgRead
        return self

    def setImgWrite(self,imgWrite:'function') -> 'Engine':
        self.imgWrite = imgWrite
        return self
    def setLogger(self,logger:'function') ->'Engine':
        self.logger = logger
        return self

    def loadStratergy(self,stratergy:str) -> 'Engine':
        if not(all((self.imgRead,self.imgWrite,self.logger))):
            raise  RuntimeError('Please add imgRead imgWrite, logger first')
        if stratergy not in self.stratergies():
            raise RuntimeError('Stratergy not found')
        self.stratergy = self.stratergies()[stratergy](imgRead = self.imgRead,imgWrite=self.imgWrite,logger = self.logger)
        # self.stratergy.setImgRead(self.imgRead)
        # self.stratergy.setImgWrite(self.imgWrite)
        # self.stratergy.setLogger(self.logger)
        return self
    def exe(self,operation:str,**kwargs):
        supportedOps = ('encrypt','decrypt')
        if operation not in supportedOps:
            raise RuntimeError(f'{operation} not support operation must be any one of : {supportedOps}  ')
        if operation == 'encrypt':
            self.encrypt(**kwargs)
        else:
            self.decrypt(**kwargs)

    def __getFunReq(self,fn:'function',**kwargs) -> dict:
        fullArgSpec = inspect.getfullargspec(fn)
        args = fullArgSpec.args
        args += fullArgSpec.kwonlyargs
        args.remove('self')
        reqArgs = {}
        for arg in args:
            if arg not in kwargs:
                raise KeyError(f'key {arg} is required')
            reqArgs[arg] =  kwargs[arg]
        if len(reqArgs) < len(kwargs):
            usedArgs = list(reqArgs.keys())
            warn(f'Extra parameters were supplied they are ignored arguments consider are {usedArgs}')
        return reqArgs

    def decrypt(self,**kwargs):
        reqArgs = self.__getFunReq(self.stratergy.decrypt,**kwargs)
        self.stratergy.decrypt(**reqArgs)

    def encrypt(self,**kwargs):
        reqArgs = self.__getFunReq(self.stratergy.encrypt,**kwargs)
        self.stratergy.encrypt(**reqArgs)
    

