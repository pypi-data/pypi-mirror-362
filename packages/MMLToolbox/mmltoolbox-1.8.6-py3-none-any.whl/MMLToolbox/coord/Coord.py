import time
import sys
import string
import gclib
import tkinter as tk
import statistics
import numpy as np

from .WASDHandler import WASDHandler

class Coord():
    """This class handles the communication with Feinmess/Galil devices via RS232"""
    def __init__(self, com_port:str, ):
        # Init System
        self.galilTool = gclib.py()
        self.galilTool.GOpen(com_port)
        print(f"Connecting System: {self.galilTool.GInfo()}")

        # Parameter
        self._mum_to_counts = 10

    #############################################################
    # Private Function
    #############################################################       
    def _initPosition(self):
        self._findLimitSwitch("Z")
        self.galilTool.GCommand('SB 1')
        self.galilTool.GCommand("JG ,,5000")
        self.galilTool.GCommand("FI Z")
        self.galilTool.GCommand("BG Z")
        self.galilTool.GMotionComplete("Z")
        print("Index of Z-Axis found!")
        self._findLimitSwitch("X")
        self.galilTool.GCommand("JG 5000")
        self.galilTool.GCommand("FI X")
        self.galilTool.GCommand("BG X")
        self.galilTool.GMotionComplete("X")
        print("Negative Index of X-Axis found!")
        self.relativePos(x=[10000,10000])
        self.galilTool.GCommand("JG 5000")
        self.galilTool.GCommand("FI X")
        self.galilTool.GCommand("BG X")
        self.galilTool.GMotionComplete("X")
        print("Middle Index of X-Axis found!")
        self._findLimitSwitch("Y")
        self.galilTool.GCommand("JG ,5000,")
        self.galilTool.GCommand("FI Y")
        self.galilTool.GCommand("BG Y")
        self.galilTool.GMotionComplete("Y")
        print("Negative Index of Y-Axis found!")
        self.relativePos(y=[10000,10000])
        self.galilTool.GCommand("JG ,5000,")
        self.galilTool.GCommand("FI Y")
        self.galilTool.GCommand("BG Y")
        self.galilTool.GMotionComplete("Y")
        print("Middle Index of Y-Axis found!")
        
    
    def _findLimitSwitch(self, axis):
        self.galilTool.GCommand('AB')
        self.galilTool.GCommand('CB 1')
        self.galilTool.GCommand('MO')   
        self.galilTool.GCommand('SH')
        if axis == 'Z':
            print("Looking for revers limitswitch on Z-axis!")
            reverse_limit_active= int(float(self.galilTool.GCommand("MG _LRZ")))
            print(reverse_limit_active)
            self.galilTool.GCommand('SB 1')
            self.galilTool.GCommand('WT 500')
            if reverse_limit_active == 0:
               
                self.galilTool.GCommand("JG,,5000")
                self.galilTool.GCommand("BG Z")
                while int(float(self.galilTool.GCommand("MG _LRZ"))) == 0:
                    print(".")
                self.galilTool.GCommand("ST Z")
                self.galilTool.GCommand("CB1")
            else:
                print(self.galilTool.GCommand("MG _LRZ"))
                self.galilTool.GCommand("JG,,-50000")
                self.galilTool.GCommand("BG Z")
                self.galilTool.GMotionComplete("Z")
                print("Limit found!")
                self.galilTool.GCommand("JG,,5000")
                self.galilTool.GCommand("BG Z")
                while int(float(self.galilTool.GCommand("MG _LRZ"))) == 0:
                    print(".")
                self.galilTool.GCommand("ST Z")
                print(self.galilTool.GCommand("MG _LRZ"))
                self.galilTool.GCommand("CB1")

        if axis == 'Y':
            print("Looking for revers limitswitch on Y-axis!")
            reverse_limit_active= int(float(self.galilTool.GCommand("MG _LRY")))
            print(reverse_limit_active)
            self.galilTool.GCommand('AB')
            self.galilTool.GCommand('CB 1')
            self.galilTool.GCommand('MO')   
            self.galilTool.GCommand('SH')
            self.galilTool.GCommand('WT 500')
            if reverse_limit_active == 0:
               
                self.galilTool.GCommand("JG ,5000,")
                self.galilTool.GCommand("BG Y")
                while int(float(self.galilTool.GCommand("MG _LRY"))) == 0:
                    print(".")
                self.galilTool.GCommand("ST Y")
                
            else:
                print(self.galilTool.GCommand("MG _LRY"))
                self.galilTool.GCommand("JG ,-50000,")
                self.galilTool.GCommand("BG Y")
                self.galilTool.GMotionComplete("Y")
                print("Limit found!")
                self.galilTool.GCommand("JG ,5000,")
                self.galilTool.GCommand("BG Y")
                while int(float(self.galilTool.GCommand("MG _LRY"))) == 0:
                    print(".")
                self.galilTool.GCommand("ST Y")
                print(self.galilTool.GCommand("MG _LRY"))
        if axis == 'X':
            print("Looking for revers limitswitch on X-axis!")
            reverse_limit_active= int(float(self.galilTool.GCommand("MG _LRX")))
            print(reverse_limit_active)
            self.galilTool.GCommand('AB')
            self.galilTool.GCommand('CB 1')
            self.galilTool.GCommand('MO')   
            self.galilTool.GCommand('SH')
            self.galilTool.GCommand('WT 500')
            if reverse_limit_active == 0:
               
                self.galilTool.GCommand("JG 5000,,")
                self.galilTool.GCommand("BG X")
                while int(float(self.galilTool.GCommand("MG _LRX"))) == 0:
                    print(".")
                self.galilTool.GCommand("ST X")
                
            else:
                print(self.galilTool.GCommand("MG _LRX"))
                self.galilTool.GCommand("JG -50000,,")
                self.galilTool.GCommand("BG X")
                self.galilTool.GMotionComplete("X")
                print("Limit found!")
                self.galilTool.GCommand("JG 5000,,")
                self.galilTool.GCommand("BG X")
                while int(float(self.galilTool.GCommand("MG _LRX"))) == 0:
                    print(".")
                self.galilTool.GCommand("ST X")
                print(self.galilTool.GCommand("MG _LRX"))

    def _pos2counts(self, pos):
        counts = int(pos*self._mum_to_counts)
        return counts
    
    def _counts2pos(self, counts):
        pos = counts / self._mum_to_counts
        return pos

    #############################################################
    # Global Function
    #############################################################
    def initSystem(self,buildInInitAvialable:bool=True):
        if buildInInitAvialable:
          self.galilTool.GCommand("XQ#NEWINIT")
        else:
            self._initPosition()

    def sendCommand(self, command:str):
        """This method allows the user to send specific commands
        :param command: The command the user wants to execute
        :type command: str
        """
        self.galilTool.GCommand(command)

    def relativePos(self,x=None, y=None, z=None):
        """This method moves an axis the specified amount of steps away from its current position.

        :param x: List with two elements. The first element specifies the amount of steps. The second element specifies the movement speed. 
        :type x: list

        :param y: List with two elements. The first element specifies the amount of steps. The second element specifies the movement speed. 
        :type x: list

        :param z: List with two elements. The first element specifies the amount of steps. The second element specifies the movement speed. 
        :type x: list
        """

        self.galilTool.GCommand('AB')
        self.galilTool.GCommand('CB 1')
        self.galilTool.GCommand('MO')   
        self.galilTool.GCommand('SH')
        self.galilTool.GCommand('AC 150000')
        self.galilTool.GCommand('DC 150000')
  
        active_axis = ''

        if type(x) == list:
            self.galilTool.GCommand('SPX = '+ str(self._pos2counts(x[1])))
            self.galilTool.GCommand('PRX = ' + str(-self._pos2counts(x[0])))
            active_axis += 'X'

        if type(y) == list:
            self.galilTool.GCommand('SPY = '+ str(self._pos2counts(y[1])))
            self.galilTool.GCommand('PRY = ' + str(-self._pos2counts(y[0])))
            active_axis += 'Y'

        if type(z) == list:
            self.galilTool.GCommand('SPZ = '+ str(self._pos2counts(z[1])))
            self.galilTool.GCommand('PRZ = ' + str(-self._pos2counts(z[0])))
            self.galilTool.GCommand('SB 1')
            self.galilTool.GCommand('WT 500')
            active_axis += 'Z'

        print("Starting movement!")
        self.galilTool.GCommand('BG ' + active_axis )
        self.galilTool.GMotionComplete(active_axis)
        self.galilTool.GCommand('CB 1')
        print("Movement complete!")
    
    def absolutePos(self,x=None, y=None, z=None):
        """This method moves an axis to an absolute position in the coordinate system of the Feinmess system.

        :param x: List with two elements.The first element specifies the absolute position based on reference coordinate system. The second element specifies the movement speed.
        :type x: list

        :param y: List with two elements.The first element specifies the absolute position based on reference coordinate system. The second element specifies the movement speed.
        :type x: list

        :param z: List with two elements.The first element specifies the absolute position based on reference coordinate system. The second element specifies the movement speed.
        :type x: list
        """

        self.galilTool.GCommand('AB')
        self.galilTool.GCommand('CB 1')
        self.galilTool.GCommand('MO')   
        self.galilTool.GCommand('SH')
        self.galilTool.GCommand('AC 150000')
        self.galilTool.GCommand('DC 150000')
            
        active_axis = ''

        if type(x) == list:
            self.galilTool.GCommand('SPX = '+ str(self._pos2counts(x[1])))
            self.galilTool.GCommand('PAX = ' + str(-self._pos2counts(x[0])))
            active_axis += 'X'
        
        if type(y) == list:
            self.galilTool.GCommand('SPY = '+ str(self._pos2counts(y[1])))
            self.galilTool.GCommand('PAY = ' + str(-self._pos2counts(y[0])))
            active_axis += 'Y'

        if type(z) == list:
            self.galilTool.GCommand('SPZ = '+ str(self._pos2counts(z[1])))
            self.galilTool.GCommand('PAZ = ' + str(-self._pos2counts(z[0])))
            self.galilTool.GCommand('SB 1')
            self.galilTool.GCommand('WT 500')
            active_axis += 'Z'

        print("Starting movement!")
        self.galilTool.GCommand('BG' + active_axis)
        self.galilTool.GMotionComplete(active_axis)
        self.galilTool.GCommand('CB 1')
        print("Movement complete!")


    def getPos(self):
        """    This method returns the current position of all connected axis.

        :return: A list every element holds the current position of an axis in alphabetical order.
        :rtype: list
        """        
        data = self.galilTool.GCommand('TP')
        data = data.split(',')
        
        for i in range(len(data)):
            data[i] = self._counts2pos(int(data[i]))*-1

        return np.array(data) 

    def gridMode(self, rows, column, row_step, col_step, z_retract,rest_period, speed):
        for i in range(rows):
            time.sleep(rest_period)
            self.relativePos(z=[z_retract, speed])
            for j in range(column-1):
                if i % 2 == 0:
                    self.relativePos(x=[row_step, speed])
                else:
                    self.relativePos(x=[-1*row_step, speed])
                self.relativePos(z=[z_retract*-1, speed])
                time.sleep(rest_period)
                self.relativePos(z=[z_retract, speed])
            self.relativePos(y = [col_step, speed],z=[z_retract*-1, speed])
            
    
    def customGridMode(self, steps_per_element, mapping, rest_time):
        steps_to_take = 0
        positions = self.getPos()
        initial_x_position = positions[0]
        initial_y_position = positions[1]
        initial_z_position = positions[2]

        row_counter = 0

        for row in mapping:
            for point in row:
                if point == 1:
                    self.absolutePos(z = [1000, initial_z_position])
                    time.sleep(rest_time)
                    self.relativePos(z = [1000, -50000])
                self.relativePos(y = [1000, steps_per_element])
            
            self.relativePos(x = [1000, steps_per_element])
            self.absolutePos(y = [1000, initial_y_position])

    def wasdMovement(self):
        """This method opens a small GUI that allows the user to move the Feinmess-system with
        the keys "WASD". When pressing enter the current position of the Feinmess-system gets
        written to the global list measurement_positions for later use    
        """
        root = tk.Tk()
        #self.pack(fill = "both", expand=True)
        WASDHandler(root, self).pack(fill="both", expand=True)
        root.mainloop()

    def closeSystem(self):
        self.galilTool.GClose()
        print("Coord Connection closed!")
    
