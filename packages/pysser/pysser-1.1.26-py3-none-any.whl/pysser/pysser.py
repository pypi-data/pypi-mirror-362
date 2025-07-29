import sys

class Pysser():
    def __init__(self,interval=0.1):
        self.sser = None
        if sys.platform.startswith('linux'):
            from .ssermainlinux import SserMain
            self.sser = SserMain(interval=interval)
        else:
            from .ssermainwin import SserMain
            self.sser = SserMain(interval=interval)

    def init(self,port,baudrate,timeout,closeL,closeG) -> None:
        self.sser.init(port=port,baudrate=baudrate,timeout=timeout,closeL=closeL,closeG=closeG)

        
    def flush(self):
        self.sser.flush()

    def close(self) -> None:
        self.sser.close()

    def open(self):
        self.sser.open()

    def is_open(self):
        return self.sser.is_open()
    
    def docommand(self, command, no_response=False, timeout=3, size=1,gtypePoll=False):
        return self.sser.docommand(command=command,no_response=no_response,timeout=timeout,size=size,gtypePoll=gtypePoll)
    
    def read(self,size=1):
        return self.sser.read(size=size)
    
    def write(self,data):
        self.sser.write(data=data)

    def set_interval(self, interval):
        self.sser.set_interval(interval=interval)
        
    def set_address(self, address):
        self.sser.set_address(address=address)