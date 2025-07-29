import chrpy
import time

from chrpy.chr_cmd_id import *
from chrpy.chr_connection import *
from chrpy.chr_utils import Data

class Optic:
    def __init__(self,IPAdress:str='192.168.170.2',IDSens:int=1, nSamples:int=10):
        self.IPAdresse = IPAdress
        self.nSamples = nSamples
        self.IDSens = IDSens
        self.conn = None
        
    def initSystem(self):
        config = ConnectionConfig()
        config.address = self.IPAdresse    
        output_format = OutputDataMode.DOUBLE
        conn = connection_from_config(config=config)
        conn.open()
        conn.set_output_data_format_mode(output_format)
        conn.exec('SODX', 83, 256, 2304)
        conn.exec('SEN', self.IDSens)
        conn.exec('AVD', self.nSamples)
        self.conn = conn
    
    def getDistance(self):
        _ = self.conn.activate_auto_buffer_mode(self.nSamples, flush_buffer=True)
        data = self.conn.get_auto_buffer_new_samples()
        status = self.conn.get_auto_buffer_status()
        if status == AutoBuffer.ERROR:
            raise Exception("Bla")
        elif status != AutoBuffer.FINISHED:
            time.sleep(0.01)
        self.conn.deactivate_auto_buffer_mode()
        value = data.get_signal_values_all(256)[0]
        std_deviation = data.get_signal_values_all(2304)[0]
        print("Get Distance done")
        return (value, std_deviation)
    
    def close_connection(self):
        self.conn.close()
        
