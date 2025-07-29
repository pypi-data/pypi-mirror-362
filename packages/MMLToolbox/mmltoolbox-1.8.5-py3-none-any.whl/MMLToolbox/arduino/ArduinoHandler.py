import serial
import time
import numpy as np

class ArduinoHandler:



    def __init__(self, port:str, baudrate:int):
        """The constructor builds the initial connectin to the arduino
           after the connection is established the constructor blocks 
           for 3 seconds giving the arduino time to reset.
        :param port: Port the arduino is connected to
        :type port: str
        
        :param baudrate: Port the arduino is connected to
        :type baudrate: str
        """
        self.serialHandler = serial.Serial(port, baudrate)
        time.sleep(3)
    


    def sendCommand(self, command:str):
        """This method lets the user to send a custom command string 
           to the connected arduino
        :param command: Command string
        :type command: str
        """
        self.serialHandler.write(bytes(command,"utf-8"))
        
    
    def startMeasurement(self):
        """Sends a  signal to the arduino to start the measurement"""
        self.serialHandler.write(b's')

    def stopMeasurement(self):
        """Sends a signal to the arduino to stop the measurement"""
        self.serialHandler.write(b'o')
        
    def reciveData(self, numSensors):
        """Reicives the acquired measurement data from the arduino
        :param numSensors: number of sensors that where used during the measurement
        :type numSensors: int   
        """
        sensor_data = []

        for i in range(numSensors):
            sensor_data.append([])


        time.sleep(3)
        self.serialHandler.write(b'd')

        #ata = b""
        print("waiting for data...")

        
        data_count =self.serialHandler.readline()
        data_count = str(data_count, "utf-8")
        data_count = data_count.strip('\r\n')
      
        data_count = int(data_count)
        

        for i in range(data_count):
            data =self.serialHandler.readline()
            data = str(data, "utf-8")
         
            data = data.split(',')
            data.pop()
            
            # if i%numSensors == 1:
            #     print(data)

            for j in range(len(data)):
                data[j] = float(data[j])
                data[j] = (data[j] / (30.8*1000))
                

            sensor_data[i%numSensors].append(np.array(data))


        for i in range(len(sensor_data)):
            sensor_data[i] = np.array(sensor_data[i])
        


                    
        return sensor_data
    

        





