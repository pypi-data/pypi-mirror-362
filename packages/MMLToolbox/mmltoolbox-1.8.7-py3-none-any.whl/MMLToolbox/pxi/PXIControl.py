import numpy as np
import nidmm
import nidaqmx
import nidaqmx.system
import niswitch
from nidmm.enums import AutoZero
import  nidaqmx.stream_writers
from nidaqmx.stream_readers import AnalogMultiChannelReader
from nidaqmx.constants import AcquisitionType
import nidaqmx.constants

import time
from enum import Enum
 

class PXIControl:
    """This class enables the user to interact with three different devices connected to a PXI-System."""
    dmmRequirements = ["slotName", "range", "sampleFreq", "wavepoints"]
    aoRequirements = ["slotName", "channel", "minVal", "maxVal", "rate", "digitalSignal","switchTrigger"]
    aiRequirements = ["slotName", "channel", "minVal", "maxVal", "rate", "wavepoints", "switchTrigger"]
    hardwareType_ = Enum('hardwareType', ['DMM', 'AI', 'AO'])
    
    def __init__(self):
        self.dmmList = []
        self.dmmSession = []
        self.main_dmmSession = 0
        self.__analogOutTask = 0
        self.__analogInTask = 0
        self.__digitalOutTask = 0
        self.__samples_to_read_Analog_In = []
        self.__daqmxReader = 0
        self.__switchSession = 0
        self.analogInResults = []
        self.__analogInDict= {}
        self.__analogOutDict = {}
        print("PXI Controll called!")
       
    def copy2dDict(self, dictionary:dict):
        """This method creates a shallow copy of the provided 2D dictionary

        :param dictionary: The 2D dictionary you want to copy 
        :type dictionary: dict

        :return: Returns a shallow copy of the provided dict
        :rtype: dict
        """
        copiedDict = {}

        for key in dictionary:
            copiedDict[key] = {}
            for inner_key in dictionary[key]:
                copiedDict[key][inner_key] = dictionary[key][inner_key]
            
        return copiedDict
    
    def createZeroArray(self, num_of_elements):
        """This method creates numpy array with the specified number of elements.
        The elements will be 0.

        :param num_elements: The 2D dictionary you want to copy 
        :type num_elements: int

        :return: Returns a numpy array with the specified number of elements
        :rtype: numpy array
        """
        array = []

        for i in range(num_of_elements):
            array.append(0.0)
        return array

    def printConnectedPXIDevs(self):
        system = nidaqmx.system.System.local()

        print("Connected PXI devices:")
        try:
            for device in system.devices:
                print(device)
        except:
            return
    
    def checkDictionaryRequirements(self, to_check:dict, hardwareType):
        """This method checks if a provided hardware dictionary has all required elements

        :param dictionary: The 2D dictionary you want to check
        :type dictionary: dict

        :param hardwareType: The type of hardware this dictionary is supposed to configure
        :type hardwareType: hardwareType_

        :return: Returns a shallow copy of the provided dict
        :rtype: dict
        """
        
        valid_key_found = False
        requirements = {}
        if hardwareType == self.hardwareType_.DMM:
            for requirement in self.dmmRequirements:
                valid_key_found = False
                for key in to_check:
                    if key == requirement:
                        valid_key_found = True
                        break
                if valid_key_found == False:
                    return False
                
        if hardwareType == self.hardwareType_.AI:
           for requirement in self.aiRequirements:
                valid_key_found = False
                for key in to_check:
                    if key == requirement:
                        valid_key_found = True
                        break
                if valid_key_found == False:
                    return False ,
        if hardwareType == self.hardwareType_.AO:
           for requirement in self.aoRequirements:
                valid_key_found = False
                for key in to_check:
                    if key == requirement:
                        valid_key_found = True
                        break

                if valid_key_found == False:
                    return False
            

        return True

    def connectHardware(self, dmmDict = 0, analogOutDict = 0, anlaogInDict = 0, switchSlotName = 0):
        """This method is used to connect to PXI devices. This method also makes sure that the provided dictionaries have the correct keys. 

        :param dmmDict: Containins all Digital multi meters that need to be configured. When using the PXIe-4081 putting its specifications on the first place inside the dictionary is recommended.
        :type dmmDict: 2D dictionary[str] or None

         :param analogOutDict: Contains all the output channels that need to be configured.
        :type analogOutDict: 2D dictionary[str] or None

         :param analogInDict: Contains all the input channels that need to be configured.
        :type analogInDict: 2D dictionary[str] or None

         :param switchSlotName: The switch is used to start all devices synchronously.The string clarifys on which slot the Switch is connected.
        :type switchSlotName: str or None
        """

        if dmmDict != 0:
            for key in dmmDict:
                if self.checkDictionaryRequirements(dmmDict[key], self.hardwareType_.DMM) == False:
                    print("Your DMM dictionary does not include required keys!")
                    print("Required keys are:")
                    print(self.dmmRequirements)
                    return False
            self.createdmmSession(dmmDict)
        if analogOutDict != 0:
            for key in analogOutDict:
                if self.checkDictionaryRequirements(analogOutDict[key], self.hardwareType_.AO) == False:
                    print("Your anlaog-out dictionary does not include required keys!")
                    print("Required keys are:")
                    print(self.aoRequirements)
                    return False
            self.createAnalogOutputTask(analogOutDict)
        if anlaogInDict != 0:
            for key in anlaogInDict:
                if self.checkDictionaryRequirements(anlaogInDict[key], self.hardwareType_.AI) == False:
                    print("Your analog-in dictionary does not include required keys!")
                    print("Required keys are:")
                    print(self.aiRequirements)
                    return False
            self.createAnalogInputTask(anlaogInDict) 
        if switchSlotName != 0:
            self.configureSwitch(switchSlotName)
        
        


    def createdmmSession(self, dmmDict):
        """This method will configure the DMM's according to the provided values and adds the Dictionary to a global list.

        :param dmmDict: Containins all Digital multi meters that need to be configured. 
        :type dmmDict: 2D dictionary[str]
        """
        for key in dmmDict:
            self.dmmList.append(dmmDict[key])        
            self.dmmSession.append(self.configureDMM(dmmDict[key]["slotName"], dmmDict[key]["range"], dmmDict[key]["sampleFreq"],dmmDict[key]["wavepoints"]))
        
     

    def configureDMM(self,slotName,range,sF,wavePoints):
        """This method is used internally by createdmmSession to connect to the specified DMM  with the provided parameters.

        :param slotName: The slot to which the DMM is connected to.
        :type slotName: str
    
        :param range: The expected measurement range of the DMM.
        :type range: float
    
        :param sF: The sample frequency the DMM should measure at.
        :type sF: int 
    
        :param wavePoints: How many wavepoints the DMM should measure.
        :type wavePoints: int
        """
        try:
                nidmm.Session(slotName).reset()
                session = nidmm.Session(slotName) 
                print("Connected: " + slotName + " | " + session.instrument_model)
                
                if session.instrument_model == "NI PXIe-4081":
                    session.configure_waveform_acquisition(nidmm.Function.WAVEFORM_VOLTAGE, range, sF, 0)
                else:
                    session.configure_waveform_acquisition(nidmm.Function.WAVEFORM_VOLTAGE, range, sF, wavePoints)
    
                session.configure_trigger(trigger_source= nidmm.TriggerSource.PXI_TRIG3, trigger_delay=0)
                session.powerline_freq = 50
                session.auto_zero = AutoZero.OFF
                session.adc_calibration = nidmm.ADCCalibration.OFF
                session.settle_time = 0

                session.initiate()
                return session
                
        except Exception as e:
                print("Problem trying to configure DMM on '" + slotName +"'!")        
                print(e)      
                return -1
                

    def createAnalogOutputTask(self, analogOutDict):
        """This method will configure the AO according to the provided values and adds the Dictionary to a global list.

        :param analogOutDict: Contains all the channels that need to be configured.
        :type analogOutDict: 2D dictionary[str]

        """
        for key, value in analogOutDict.items():
            first_key_out = key
            break
        
        self.__analogOutDict = self.copy2dDict(analogOutDict)

        try:
            self.__analogOutTask = nidaqmx.Task("outputTask")
            
 
            for key in analogOutDict:
                self.addAnalogOutputChannel(analogOutDict[key]["slotName"], analogOutDict[key]["channel"], analogOutDict[key]["minVal"], analogOutDict[key]["maxVal"])

            if analogOutDict[first_key_out]["digitalSignal"] == True:
                self.__digitalOutTask = nidaqmx.Task("digitalTask")
                self.__digitalOutTask._do_channels.add_do_chan(analogOutDict[key]["slotName"] + "/port0/line0")

            self.__analogOutTask.timing.cfg_samp_clk_timing(rate = analogOutDict[first_key_out]["rate"],sample_mode= AcquisitionType.CONTINUOUS)      
            self.__analogOutTask.timing.samp_timing_type = nidaqmx.constants.SampleTimingType.SAMPLE_CLOCK
            if analogOutDict[first_key_out]["switchTrigger"] == True:
                self.__analogOutTask.triggers.start_trigger.cfg_dig_edge_start_trig("/PXI1Slot14/PXI_Trig3", trigger_edge=nidaqmx.constants.Edge.RISING)

            print("Connected: "+ analogOutDict[first_key_out]["slotName"] + " | AnalogOutput")
         
        except Exception as e:
            print("Problem trying to configure '"+ analogOutDict[first_key_out]["slotName"] + "'!")
            return -1
            


    def createAnalogInputTask(self, analogInDict):
        """This method will configure the AI's according to the provided values and adds the Dictionary to a global list.

        :param analogInDict: Containins all the channels that need to be configured.
        :type analogInDict: 2D dictionary[str]
        """
        for key, value in analogInDict.items():
            first_key_in = key
            break
        try:
            self.__analogInTask = nidaqmx.Task("inputTask")
            self.__daqmxReader = AnalogMultiChannelReader(self.__analogInTask.in_stream)
        
            self.__analogInDict = analogInDict
       
            for key in analogInDict:    
                self.addAnalogInputChannel(analogInDict[key]["slotName"], analogInDict[key]["channel"], analogInDict[key]["minVal"], analogInDict[key]["maxVal"])
                self.__samples_to_read_Analog_In.append(analogInDict[key]["wavepoints"])
        
            self.__analogInTask.timing.cfg_samp_clk_timing(rate = analogInDict[first_key_in]["rate"],sample_mode= AcquisitionType.CONTINUOUS, samps_per_chan=3*analogInDict[first_key_in]["wavepoints"]) 
            #self.__analogInTask.input_buf_size = analogInDict[first_key_in]["wavepoints"]   
            if analogInDict[first_key_in]["switchTrigger"] == True:
                self.__analogInTask.register_every_n_samples_acquired_into_buffer_event(analogInDict[first_key_in]["wavepoints"], self.callBackStartAnalogInputTask)
                self.__analogInTask.triggers.start_trigger.cfg_dig_edge_start_trig("/PXI1Slot14/PXI_Trig3", trigger_edge=nidaqmx.constants.Edge.RISING)
            print("Connected: "+ analogInDict[first_key_in]["slotName"] + " | AnalogInput")

        except Exception as e:
            print("Problem trying to configure '"+ analogInDict[first_key_in]["slotName"] + "'!")
            
    def addAnalogOutputChannel(self, slotName, channel, minVal, maxVal):
        """This Method is used internally by createAnalogOutputTask to add the channels specified by the user to the analog output task
        
           :param slotName: The slot to which the DAQMX-card is connected to.
           :type slotName: str
        """
        try:
            self.__analogOutTask._ao_channels.add_ao_voltage_chan(slotName+"/"+ channel, min_val=minVal, max_val=maxVal) 
        except Exception as e:
      
            print("Problem trying to add Analog output channel '"+ slotName +"/"+ channel + "'!")
            return -1

    def addAnalogInputChannel(self , slotName, channel, minVal, maxVal):
        """    This Method is used internally by createAnalogInputTask to add the channels specified by the user to the analog input task. 

        :param slotName: The slot to which the DAQMX-card is connected to.
        :type slotName: str
    
        :param channel: Which channel of the DAQMX-card should be used.
        :type channel: str
    
        :param minVal: Less than the minimum value the channel should output. 
        :type minVal: int
    
        :param maxVal: More than the maximum value the channel should output
        :type maxVal: int
        """
        try:
            self.__analogInTask._ai_channels.add_ai_voltage_chan(slotName + "/" + channel, min_val=minVal, max_val= maxVal)
        except Exception as e:
            print(e)
            print("Problem trying to add Analog input channel '"+ slotName +"/"+ channel + "'!")
            return -1
     

    def configureSwitch(self, slotName):
        """    This method is used to connect to the switch on the specified slot and configure it in a way that it sends a trigger signal on trggerline 5.

        :param slotName: The slot to which the Switch is connected to.
        :type slotName: str
        """
        try:
            self.__switchSession = niswitch.Session(slotName)
            print("Connected: Switch |" + self.__switchSession.instrument_model)
        
            self.__switchSession.scan_advanced_output = niswitch.ScanAdvancedOutput.TTL3
            self.__switchSession.trigger_input = niswitch.TriggerInput.SOFTWARE_TRIG
            self.__switchSession.scan_list = "com0->ch0;"
            
        except Exception as e:
            print("Problem trying to configure Switch on '"+ slotName + "'!")
       
            return -1

    


    def startAnalogOutputTask(self, outputSignal):
        """    This method should only be called after connecting to the DAQMX card via connectHardware. It will start the analog output task and write the given outputsignals to the specified channels.

        :param outputSignal: Every row contains the signal of a channel.
        :type outputSignal: 2D numpy-array
        """
        try:

            if self.__analogOutTask == 0:
                print("No Tasks for Analogoutput have been created yet! Please create Tasks with 'connectHardware' before calling this Method!")
                return -1
            if len(self.__analogInDict) != 0:
                for key, value in self.__analogInDict.items():
                    first_key_in = key
                    break
                
            if self.__digitalOutTask != 0:            
                self.__digitalOutTask.write(np.asarray([True]))
                self.__digitalOutTask.start()

            print("Start analog output!")
            self.__analogOutTask.write(outputSignal)
            self.__analogOutTask.start()
            if self.__digitalOutTask != 0:
                time.sleep(1)
                self.__digitalOutTask.stop()
                self.__digitalOutTask.write(np.asarray([False]))
                self.__digitalOutTask.start
                self.__digitalOutTask.close()
        
        except KeyboardInterrupt as e:
            print("Measurement interrupted closing analog output task!")
            self.closeAnalogOutputTask()
        
        except Exception as e:
            print("Could not start analog output task! Please create Tasks with 'connectHardware' before calling this Method!")
            self.closeAnalogOutputTask()
        

 
        

    def startAnalogInputTask(self):
        """    This method should only be called after connecting to the DAQMX card via connectHardware. It will start the analog input task and will start the data acquisition on the specified channels. If switchTrigger was set to true this method does not need to be called the values can simply get retrieved from the public variable analogInResults.

        :return: Contains the obtained data each row contains all acquired data of one channel.
        :rtype: 2D numpy-array
        """
        if self.__analogInTask == 0:
            print("No Tasks for AnalogInput have been created yet! Please create Tasks with 'connectHardware' before calling this Method!")
            return -1
        results = []
        for num_of_samples in self.__samples_to_read_Analog_In:
            results.append(self.createZeroArray(self.__samples_to_read_Analog_In[0]))
        results = np.asarray(results)        

        

        self.__analogInTask.start()

        print("Analog input started!")
        
        self.__daqmxReader.read_many_sample(results , self.__samples_to_read_Analog_In[0],nidaqmx.constants.WAIT_INFINITELY)

        self.closeAnalogInputTask()
        
        return results
  
    
    def callBackStartAnalogInputTask(self,task_idx, event_type, num_samples, callback_data=None):
        try:
            if self.__analogInTask == 0:
                print("No Tasks for AnalogInput have been created yet! Please create Tasks with 'connectHardware' before calling this Method!")
                return -1
            results = []
            for num_of_samples in self.__samples_to_read_Analog_In:
                results.append(self.createZeroArray(self.__samples_to_read_Analog_In[0]))
            results = np.asarray(results)

            
            print("Fetching data from analog input!")
            self.__daqmxReader.read_many_sample(results , self.__samples_to_read_Analog_In[0],nidaqmx.constants.WAIT_INFINITELY)
        

            self.analogInResults = results

            self.closeAnalogInputTask()

        except Exception as e:
            print("Error callBack")
            print(e)           
      
        return 0
        
        
        
    def closeAnalogOutputTask(self):   
        """Closes all analog output tasks."""
        try:   
            
            self.__analogOutTask.close()
            zero_dict = self.copy2dDict(self.__analogOutDict)
            cnt = 0
            for key in zero_dict:
                zero_dict[key]['minVal'] = -1
                zero_dict[key]['maxVal'] = 1
                zero_dict[key]['switchTrigger'] = False
                zero_dict[key]['rate'] = 100
                cnt += 1
            
            signal = []
            if cnt == 1:
                signal = np.asarray(self.createZeroArray(100))
            else:
                for i in range(cnt):
                    signal.append(self.createZeroArray(100))
                signal = np.asarray(signal)

            self.createAnalogOutputTask(zero_dict)

            self.__analogOutTask.write(signal)
            self.__analogOutTask.start()
            

            self.__analogOutTask.stop()
            self.__analogOutTask.close()

            self.__analogOutTask = 0
            print("Set analog output to zero and closed task!")
            
        except Exception as e:
            print("Could not close Analog output task!")

    def closeAnalogInputTask(self):
        """Closes all analog input tasks."""
        try:
            self.__analogInTask.close()
            self.__analogInTask = 0
            self.__daqmxReader = 0
            print("Set analog input to zero and closed task!")

            self.__samples_to_read_Analog_In.clear()
        except Exception as e:
            print("Could not close Analog input task!")

    def closeDMMTask(self):
        
        """This method fetches all the data acquired by all the connected DMMs and closes all DMM sessions

        :return: Every row contains all measured data of one DMM.
        :rtype: 2D numpy-array
        """
        for i, session in enumerate(self.dmmSession):
                session.close()
        self.dmmSession.clear()
    
    def triggerDevices(self, output_signal = 0):        
        """This method should only be called after connecting DMMs and/or analog out/input channels and the switch via connectHardware.
        This method will start the data acquisition of all connected DMMs at the same time. Also if switchTrigger is set to true for the 
        analog channels of the DAQMX-card, they will also be triggered synchronously. When switchTrigger is set to true for an analog output channel 
        the method expects you to pass an output signal as a parameter in the same format as for the startAnalogOutputTask.

        :param outputSignal: Every row contains the signal of a channel.
        :type outputSignal: 2D numpy-array
        """
        if self.__switchSession == 0:
             print("No Switch session has been created yet! Please create Sessions with 'connectHardware' before calling this Method!")
             return -1

        if self.__analogOutTask != 0:
            try:    
                self.__analogOutTask.write(output_signal)
                self.__analogOutTask.start()
            except Exception as e:
                print("Could not start Analog output task!")
           
        if self.__analogInTask != 0:
            try:    
                self.__analogInTask.start()
            except Exception as e:
                print("Could not start Analog input task!")
    


        try:
            self.__switchSession.initiate()
            self.__switchSession.send_software_trigger()
            print("Measurement in Progress")
        except Exception as e:
            print("Could not send trigger to start devieces")
            
       
      
  
   
    def getMeasResults(self):
        
        """This method fetches all the data acquired by all the connected DMMs and closes all DMM sessions

        :return: Every row contains all measured data of one DMM.
        :rtype: 2D numpy-array
        """
        allInputs = []

        try:
        
            for i, session in enumerate(self.dmmSession):
                    
                allInputs.append(session.fetch_waveform(self.dmmList[i]["wavepoints"]))
                
                session.close()
           
        except Exception as e:
            print("Error getMeasResults")
            # print("Could not fetch results!")
            print(e)
          
      
        self.allInputs = allInputs
        self.dmmSession.clear()
    
        return allInputs


    
