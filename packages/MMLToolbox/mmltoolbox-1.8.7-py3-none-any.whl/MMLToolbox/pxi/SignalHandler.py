import numpy as np
import sys
import MMLToolbox.pxi.PXIPostProcessing as PXIPostProcessing

from . import StoreSetup
from MMLToolbox.util.types import *

class SignalHandler:
    def __init__(self, storeSetup:StoreSetup,meas_type=str,do_demag=False):
        self.ss = storeSetup
        self.meas_type = meas_type
        
        # Signal Parameter
        self.frequency = storeSetup.readInfoValue('frequency')
        self.sample_frequency_factor = storeSetup.readInfoValue('sampleFrequencyFactor')
        self.sample_frequency_factor_daq = storeSetup.readInfoValue('sampleFrequencyFactorDAQ')
        self.sample_frequency = self.frequency*self.sample_frequency_factor
        self.zero_periods = storeSetup.readInfoValue('zeroPeriods')
        self.up_periods = storeSetup.readInfoValue('upPeriods')
        self.main_periods = storeSetup.readInfoValue('mainPeriods')
        self.pp_periods = storeSetup.readInfoValue('ppPeriods')
        self.down_periods = storeSetup.readInfoValue('downPeriods')
        self.phi = storeSetup.readInfoValue('phi')


        # Additional Parameters
        self.wavepoints= None
        self.time = None
        self.len_up_signal = None
        self.len_down_signal = None
        self.len_main_signal = None
        self.len_zeros = None
        self.base_out_signal = None
        self.base_ref_signal = None
        self.base_demag_signal = None
        self.len_up_signal_DAQ = None
        self.len_down_signal_DAQ = None

        # Base Signal
        self.up_signal = None
        self.down_signal = None
        
        # Init Function
        self.__init_base_signal()

        # Demag Function
        if do_demag:
            self.zero_periods_demag = storeSetup.readInfoValue('zeroPeriodsDemag')
            self.up_periods_demag = storeSetup.readInfoValue('upPeriodsDemag')
            self.main_periods_demag = storeSetup.readInfoValue('mainPeriodsDemag')
            self.pp_periods_demag = storeSetup.readInfoValue('ppPeriodsDemag')
            self.down_periods_demag = storeSetup.readInfoValue('downPeriodsDemag')
            self.base_demag_signal = self.__init_demag_signal()
            

    ################################################
    # User Functions
    ################################################
    def getBaseOutSignal(self):
        return self.base_out_signal
    
    def getBaseRefSignal(self):
        return self.base_ref_signal
    
    def getDemagSignal(self):
        return self.base_demag_signal

    ################################################
    # Helper Functions
    ################################################
    def __init_base_signal(self):
        if self.meas_type == UNIAXIAL:
            self.__func_base_out_signal = self.__uniaxial_base_out_signal
            self.__func_base_ref_signal = self.__uniaxial_base_ref_signal
        elif self.meas_type == ROTATIONAL_CW:
            self.rot_dir = 1
            self.__func_base_out_signal = self.__rotational_base_out_signal
            self.__func_base_ref_signal = self.__rotational_base_out_signal
        elif self.meas_type == ROTATIONAL_CCW:
            self.rot_dir = -1
            self.__func_base_out_signal = self.__rotational_base_out_signal
            self.__func_base_ref_signal = self.__rotational_base_out_signal
        elif self.meas_type == NELDERMEAD:
            self.__func_base_out_signal = self.__uniaxial_base_nelder_mead
            self.__func_base_ref_signal = self.__uniaxial_base_nelder_mead
        else:
            sys.exit(f"meas_type must be {UNIAXIAL},{ROTATIONAL_CW},{ROTATIONAL_CCW} or {NELDERMEAD}")

        self.base_out_signal = self.__func_base_out_signal()
        self.base_ref_signal = self.__func_base_ref_signal()

    def __add_dmm_signal_parameter_2_storeSetup(self,zeroSteps,upSteps,ppSteps,mainSteps,downSteps):
        self.wavepoints = len(zeroSteps)+len(upSteps)+len(ppSteps)+len(mainSteps)+len(ppSteps)+len(downSteps)+len(zeroSteps)
        total_periods = 2*self.zero_periods+2*self.pp_periods+self.up_periods+self.down_periods+self.main_periods
        #self.time = np.arange(0,total_periods/self.frequency,1/self.sample_frequency)
        self.time = np.arange(0,self.main_periods/self.frequency,1/self.sample_frequency)
        self.len_up_signal = len(zeroSteps)+len(upSteps)+len(ppSteps)
        self.len_main_signal = len(mainSteps)
        self.len_down_signal = len(downSteps)+len(zeroSteps)+len(ppSteps)
        self.len_zeros = len(zeroSteps)
        temp_dict = {"lenZeroSteps": (len(zeroSteps), "-"),
                     "lenUpSteps": (len(upSteps), "-"),
                     "lenPPSteps": (len(ppSteps), "-"),
                     "lenMainSteps": (len(mainSteps), "-"),
                     "lenDownSteps": (len(downSteps), "-"),
                     "lenUpSignal": (self.len_up_signal, "-"),
                     "lenMainSignal": (self.len_main_signal, "-"),
                     "lenDownSignal": (self.len_down_signal, "-"),
                     "wavepoints": (self.wavepoints, ("-")),
                     "time": (self.time,"s"),
                     "sampleFrequency": (self.frequency*self.sample_frequency_factor,"Hz")}
        self.ss.writeInfo(temp_dict)

    def __add_daq_signal_parameter_2_storeSetup(self):
        sampleFrequency = self.frequency*self.sample_frequency_factor_daq
        zeroSteps = np.arange(0,self.zero_periods/self.frequency,1/sampleFrequency)
        upSteps = np.arange(0,self.up_periods/self.frequency,1/sampleFrequency)
        ppSteps = np.arange(0,self.pp_periods/self.frequency,1/sampleFrequency)
        mainSteps = np.arange(0,self.main_periods/self.frequency,1/sampleFrequency)
        downSteps = np.arange(0,self.down_periods/self.frequency,1/sampleFrequency)
        wavepoints = len(zeroSteps)+len(upSteps)+len(ppSteps)+len(mainSteps)+len(ppSteps)+len(downSteps)+len(zeroSteps)
        time = np.arange(0,self.main_periods/self.frequency,1/sampleFrequency)
        self.len_up_signal_DAQ = len(zeroSteps)+len(upSteps)+len(ppSteps)
        self.len_down_signal_DAQ = len(downSteps)+len(zeroSteps)+len(ppSteps)
        temp_dict = {"lenZeroStepsDAQ": (len(zeroSteps), "-"),
                     "lenUpStepsDAQ": (len(upSteps), "-"),
                     "lenPPStepsDAQ": (len(ppSteps), "-"),
                     "lenMainStepsDAQ": (len(mainSteps), "-"),
                     "lenDownStepsDAQ": (len(downSteps), "-"),
                     "lenUpSignalDAQ": (len(zeroSteps)+len(upSteps)+len(ppSteps), "-"),
                     "lenMainSignalDAQ": (len(mainSteps), "-"),
                     "lenDownSignalDAQ": (len(downSteps)+len(zeroSteps)+len(ppSteps), "-"),
                     "wavepointsDAQ": (wavepoints, ("-")),
                     "timeDAQ": (time,"s"),
                     "sampleFrequencyDAQ": (self.frequency*self.sample_frequency_factor_daq,"Hz")}
        self.ss.writeInfo(temp_dict)

    def __add_demag_signal_parameter_2_storeSetup(self,zeroSteps,upSteps,ppSteps,mainSteps,downSteps):
        wavepoints = len(zeroSteps)+len(upSteps)+len(ppSteps)+len(mainSteps)+len(ppSteps)+len(downSteps)+len(zeroSteps)
        all_periods = 2*self.zero_periods_demag+self.up_periods_demag+self.main_periods_demag+2*self.pp_periods_demag+self.down_periods_demag
        time = np.arange(0,all_periods/self.frequency,1/self.sample_frequency)[-1]
        temp_dict = {"wavepointsDemag": (wavepoints, ("-")),
                     "timeDemag": (time,("s"))}
        self.ss.writeInfo(temp_dict)

    ################################################
    # Base Output Signal
    ################################################
    def __uniaxial_base_out_signal(self):
        frequency = self.frequency
        sampleFrequency = self.sample_frequency
        phi = self.phi

        zeroSteps = np.arange(0,self.zero_periods/frequency,1/sampleFrequency)
        upSteps = np.arange(0,self.up_periods/frequency,1/sampleFrequency)
        ppSteps = np.arange(0,self.pp_periods/frequency,1/sampleFrequency)
        mainSteps = np.arange(0,self.main_periods/frequency,1/sampleFrequency)
        downSteps = np.arange(0,self.down_periods/frequency,1/sampleFrequency)

        zeroSignal_x = zeroSteps*0
        upSignal_x = upSteps/max(upSteps)*np.sin(2*np.pi*frequency*upSteps)
        ppSignal_x = np.sin(2*np.pi*frequency*ppSteps)
        mainSignal_x = np.sin(2*np.pi*frequency*mainSteps)
        downSignal_x = np.flip(downSteps)/max(downSteps)*np.sin(2*np.pi*frequency*downSteps)

        tempSignal_x = np.concatenate((zeroSignal_x,upSignal_x,ppSignal_x,mainSignal_x,ppSignal_x,downSignal_x,zeroSignal_x))
        tempSignal_y = np.zeros(tempSignal_x.shape)
        signal_xy = np.array([tempSignal_x,tempSignal_y])
        R = np.array([[np.cos(np.pi/180*phi), -np.sin(np.pi/180*phi)],
                      [np.sin(np.pi/180*phi), np.cos(np.pi/180*phi)]])
        signal = R @ signal_xy

        self.__add_dmm_signal_parameter_2_storeSetup(zeroSteps,upSteps,ppSteps,mainSteps,downSteps)
        self.__add_daq_signal_parameter_2_storeSetup()
        self.up_signal = signal[:,:(len(zeroSteps)+len(upSteps))]
        self.down_signal = signal[:,-(len(downSteps)+len(zeroSteps)):]
        return signal.reshape(2,-1)
    
    def __uniaxial_base_nelder_mead(self):
        frequency = self.frequency
        sampleFrequency = self.sample_frequency

        zeroSteps = np.arange(0,self.zero_periods/frequency,1/sampleFrequency)
        upSteps = np.arange(0,self.up_periods/frequency,1/sampleFrequency)
        ppSteps = np.arange(0,self.pp_periods/frequency,1/sampleFrequency)
        mainSteps = np.arange(0,self.main_periods/frequency,1/sampleFrequency)
        downSteps = np.arange(0,self.down_periods/frequency,1/sampleFrequency)

        zeroSignal_x = zeroSteps*0
        upSignal_x = upSteps/max(upSteps)*np.sin(2*np.pi*frequency*upSteps)
        ppSignal_x = np.sin(2*np.pi*frequency*ppSteps)
        mainSignal_x = np.sin(2*np.pi*frequency*mainSteps)
        downSignal_x = np.flip(downSteps)/max(downSteps)*np.sin(2*np.pi*frequency*downSteps)

        tempSignal_x = np.concatenate((zeroSignal_x,upSignal_x,ppSignal_x,mainSignal_x,ppSignal_x,downSignal_x,zeroSignal_x))
        signal = np.array([tempSignal_x,tempSignal_x])

        self.__add_dmm_signal_parameter_2_storeSetup(zeroSteps,upSteps,ppSteps,mainSteps,downSteps)
        self.__add_daq_signal_parameter_2_storeSetup()
        self.up_signal = signal[:,:(len(zeroSteps)+len(upSteps))]
        self.down_signal = signal[:,-(len(downSteps)+len(zeroSteps)):]
        return signal.reshape(2,-1)
    
    def __rotational_base_out_signal(self):
        frequency = self.frequency
        sampleFrequency = self.sample_frequency

        zeroSteps = np.arange(0,self.zero_periods/frequency,1/sampleFrequency)
        upSteps = np.arange(0,self.up_periods/frequency,1/sampleFrequency)
        ppSteps = np.arange(0,self.pp_periods/frequency,1/sampleFrequency)
        mainSteps = np.arange(0,self.main_periods/frequency,1/sampleFrequency)
        downSteps = np.arange(0,self.down_periods/frequency,1/sampleFrequency)

        zeroSignal = zeroSteps*0
        upSignal = upSteps/max(upSteps)*np.sin(2*np.pi*frequency*upSteps)
        ppSignal = np.sin(2*np.pi*frequency*ppSteps)
        mainSignal = np.sin(2*np.pi*frequency*mainSteps)
        downSignal = np.flip(downSteps)/max(downSteps)*np.sin(2*np.pi*frequency*downSteps)
        tempSignal_x = np.concatenate((zeroSignal,upSignal,ppSignal,mainSignal,ppSignal,downSignal,zeroSignal))
    
        upSignal = self.rot_dir*upSteps/max(upSteps)*np.cos(2*np.pi*frequency*upSteps)
        ppSignal = self.rot_dir*np.cos(2*np.pi*frequency*ppSteps)
        mainSignal = self.rot_dir*np.cos(2*np.pi*frequency*mainSteps)
        downSignal = self.rot_dir*np.flip(downSteps)/max(downSteps)*np.cos(2*np.pi*frequency*downSteps)
        tempSignal_y = np.concatenate((zeroSignal,upSignal,ppSignal,mainSignal,ppSignal,downSignal,zeroSignal))

        self.__add_dmm_signal_parameter_2_storeSetup(zeroSteps,upSteps,ppSteps,mainSteps,downSteps)
        self.__add_daq_signal_parameter_2_storeSetup()
        up = len(zeroSteps)+len(upSteps)
        down = len(downSteps)+len(upSteps)
        self.up_signal = np.array([tempSignal_x[:up],tempSignal_y[:up]]).reshape(2,-1)  
        self.down_signal = np.array([tempSignal_x[-down:],tempSignal_y[-down:]]).reshape(2,-1)  
        return np.array([tempSignal_x,tempSignal_y]).reshape(2,-1)  
    
    def __init_demag_signal(self):
        frequency = self.frequency
        sampleFrequency = self.sample_frequency

        zeroSteps = np.arange(0,self.zero_periods_demag/frequency,1/sampleFrequency)
        upSteps = np.arange(0,self.up_periods_demag/frequency,1/sampleFrequency)
        ppSteps = np.arange(0,self.pp_periods_demag/frequency,1/sampleFrequency)
        mainSteps = np.arange(0,self.main_periods_demag/frequency,1/sampleFrequency)
        downSteps = np.arange(0,self.down_periods_demag/frequency,1/sampleFrequency)

        zeroSignal = zeroSteps*0
        upSignal = upSteps/max(upSteps)*np.sin(2*np.pi*frequency*upSteps)
        ppSignal = np.sin(2*np.pi*frequency*ppSteps)
        mainSignal = np.sin(2*np.pi*frequency*mainSteps)
        downSignal = np.flip(downSteps)/max(downSteps)*np.sin(2*np.pi*frequency*downSteps)
        tempSignal_x = np.concatenate((zeroSignal,upSignal,ppSignal,mainSignal,ppSignal,downSignal,zeroSignal))
    
        upSignal = upSteps/max(upSteps)*np.cos(2*np.pi*frequency*upSteps)
        ppSignal = np.cos(2*np.pi*frequency*ppSteps)
        mainSignal = np.cos(2*np.pi*frequency*mainSteps)
        downSignal = np.flip(downSteps)/max(downSteps)*np.cos(2*np.pi*frequency*downSteps)
        tempSignal_y = np.concatenate((zeroSignal,upSignal,ppSignal,mainSignal,ppSignal,downSignal,zeroSignal))

        self.__add_demag_signal_parameter_2_storeSetup(zeroSteps,upSteps,ppSteps,mainSteps,downSteps)
        return np.array([tempSignal_x,tempSignal_y]).reshape(2,-1)  
    ################################################
    # Base Ref Signal
    ################################################
    def __uniaxial_base_ref_signal(self):
        frequency = self.frequency
        sampleFrequency = self.sample_frequency
        phi = self.phi

        zeroSteps = np.arange(0,self.zero_periods/frequency,1/sampleFrequency)
        upSteps = np.arange(0,self.up_periods/frequency,1/sampleFrequency)
        ppSteps = np.arange(0,self.pp_periods/frequency,1/sampleFrequency)
        mainSteps = np.arange(0,self.main_periods/frequency,1/sampleFrequency)
        downSteps = np.arange(0,self.down_periods/frequency,1/sampleFrequency)

        zeroSignal_x = zeroSteps*0
        upSignal_x = upSteps/max(upSteps)*np.sin(2*np.pi*frequency*upSteps)
        ppSignal_x = np.sin(2*np.pi*frequency*ppSteps)
        mainSignal_x = np.sin(2*np.pi*frequency*mainSteps)
        downSignal_x = np.flip(downSteps)/max(downSteps)*np.sin(2*np.pi*frequency*downSteps)

        tempSignal_x = np.concatenate((zeroSignal_x,upSignal_x,ppSignal_x,mainSignal_x,ppSignal_x,downSignal_x,zeroSignal_x))
        tempSignal_y = np.zeros(tempSignal_x.shape)
        signal_xy = np.array([tempSignal_x,tempSignal_y])
        R = np.array([[np.cos(np.pi/180*phi), -np.sin(np.pi/180*phi)],
                      [np.sin(np.pi/180*phi), np.cos(np.pi/180*phi)]])
        signal = R @ signal_xy
        return signal.reshape(2,-1)

    ################################################
    # Output Signal
    ################################################
    def get_complite_output_signal_old(self,signal):
        frequency = self.frequency
        sampleFrequency = self.sample_frequency
        signal_one_periode_x = PXIPostProcessing.calc_average(signal[0,:],sampleFrequency,frequency,1)
        signal_one_periode_y = PXIPostProcessing.calc_average(signal[1,:],sampleFrequency,frequency,1) 

        zeroSteps = np.arange(0,self.zero_periods/frequency,1/sampleFrequency)
        upSteps = np.arange(0,self.up_periods/frequency,1/sampleFrequency)
        downSteps = np.arange(0,self.down_periods/frequency,1/sampleFrequency)

        zeroSignal = zeroSteps*0
        upSignal = upSteps/max(upSteps)*np.tile(signal_one_periode_x,self.up_periods)
        ppSignal = np.tile(signal_one_periode_x,self.pp_periods)
        downSignal = np.flip(downSteps)/max(downSteps)*np.tile(signal_one_periode_x,self.down_periods)
        tempSignal_x = np.concatenate((zeroSignal,upSignal,ppSignal,signal[0,:],ppSignal,downSignal,zeroSignal))

        zeroSignal = zeroSteps*0
        upSignal = upSteps/max(upSteps)*np.tile(signal_one_periode_y,self.up_periods)
        ppSignal = np.tile(signal_one_periode_y,self.pp_periods)
        downSignal = np.flip(downSteps)/max(downSteps)*np.tile(signal_one_periode_y,self.down_periods)
        tempSignal_y = np.concatenate((zeroSignal,upSignal,ppSignal,signal[1,:],ppSignal,downSignal,zeroSignal))

        return np.array([tempSignal_x,tempSignal_y]).reshape(2,-1)
    
    def get_complite_output_signal(self,signal):
        frequency = self.frequency
        sampleFrequency = self.sample_frequency

        zeroSteps = np.arange(0,self.zero_periods/frequency,1/sampleFrequency)
        upSteps = np.arange(0,self.up_periods/frequency,1/sampleFrequency)
        downSteps = np.arange(0,self.down_periods/frequency,1/sampleFrequency)

        signal[:,:zeroSteps] = 0
        signal[:,-zeroSteps:] = 0
        signal[:,zeroSteps:(zeroSteps+upSteps)] = upSteps/max(upSteps)*signal[:,zeroSteps:(zeroSteps+upSteps)]
        signal[:,-(downSteps+zeroSteps):zeroSteps] = np.flip(downSteps)/max(downSteps)*signal[:,-(downSteps+zeroSteps):zeroSteps]

        return signal

    
        

