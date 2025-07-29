import numpy as np
import sys
import math
import time

from MMLToolbox.pxi.StoreSetup import StoreSetup 
from MMLToolbox.pxi.PXIControl import PXIControl
from MMLToolbox.util.types import *


class PXIHandler:
    def __init__(self, storeSetup:StoreSetup):
        self.ss = storeSetup
        self.handler = PXIControl()

        # PXI Parameter
        self.frequency = storeSetup.readInfoValue("frequency")
        self.sampleFrequencyFactor = storeSetup.readInfoValue("sampleFrequencyFactor")
        self.sampleFrequencyFactorDAQ = storeSetup.readInfoValue("sampleFrequencyFactorDAQ")
        self.niOutput = storeSetup.readInfo("niOutput")
        self.niInput = storeSetup.readInfo("niInput")
        self.niDMM = storeSetup.readInfo("niDMM")
        storeSetup.readInfo("niDMM")

        self.__define_niOutput()
        self.__define_niInput()
        self.__define_niDMM()

    def __define_niOutput(self):
        for key,item in self.niOutput.items():
            item["rate"] = self.sampleFrequencyFactor*self.frequency
            self.niOutput[key] = item

    def __define_niInput(self):
        for key,item in self.niInput.items():
            self.__daq_sample_frequency_feasible()
            item["rate"] = self.sampleFrequencyFactorDAQ*self.frequency
            item["wavepoints"] = self.ss.readInfoValue("wavepointsDAQ")
            self.niInput[key] = item

    def __define_niDMM(self):
        for key,item in self.niDMM.items():
            self.__dmm_sample_frequency_feasible()
            item["sampleFreq"] = self.sampleFrequencyFactor*self.frequency
            item["wavepoints"] = self.ss.readInfoValue("wavepoints")
            self.niDMM[key] = item

    def __define_niDMM_Demag(self):
        niDMM = self.ss.readInfo("niDMM")
        for key,item in niDMM.items():
            item["sampleFreq"] = self.sampleFrequencyFactor*self.frequency
            item["wavepoints"] = self.ss.readInfoValue("wavepointsDemag")
            niDMM[key] = item
        return niDMM
        

    def __dmm_sample_frequency_feasible(self):
        samplefreq = self.frequency*self.sampleFrequencyFactor
        factor_base = 1.8*10**6
        param = factor_base/samplefreq

        if not param.is_integer():
            param_min = math.floor(param)
            param_max = math.ceil(param)

            while factor_base % (param_min*self.frequency) != 0 and param_min > 0:
              param_min -= 1

            while factor_base % (param_max*self.frequency) != 0:
              param_max += 1

            sample_freq_factor_min = factor_base/(param_min*self.frequency)
            sample_freq_factor_max = factor_base/(param_max*self.frequency)

            sys.exit(f"##########################\nSampleFrquencyFactor not feasible.\nPlease change sampleFrequencyFactor to {sample_freq_factor_min:.1f} or {sample_freq_factor_max:.1f} \n##########################")

    def __daq_sample_frequency_feasible(self):
        samplefreq = self.frequency*self.sampleFrequencyFactorDAQ
        factor_base = 100*10**6 
        param = factor_base/samplefreq
        max_sample_freq_factor = 2*10**6/(len(self.niInput)*2*self.frequency)

        if not param.is_integer():
            param_min = math.floor(param)
            param_max = math.ceil(param)

            while factor_base % (param_min*self.frequency) != 0 and param_min > 0:
              param_min -= 1

            while factor_base % (param_max*self.frequency) != 0:
              param_max += 1

            sample_freq_factor_min = factor_base/(param_min*self.frequency)
            sample_freq_factor_max = factor_base/(param_max*self.frequency)

            if sample_freq_factor_max > max_sample_freq_factor or sample_freq_factor_min > max_sample_freq_factor:
                sys.exit(f"##########################\nSampleFrequencyFactorDAQ must be smaller as {max_sample_freq_factor}\n##########################")
            else: 
                sys.exit(f"##########################\nSampleFrequencyFactorDAQ not feasible.\nPlease change sampleFrequencyFactorDAQ to {sample_freq_factor_min:.1f} or {sample_freq_factor_max:.1f} \n##########################")

    def doMeasurement(self,signal,iteration):
        self.handler.connectHardware(dmmDict=self.niDMM,analogOutDict=self.niOutput,anlaogInDict=self.niInput,switchSlotName="PXI1Slot13")
        self.ss.writeOutputSignal(iteration,self.niOutput.keys(),[signal[0,:],signal[1,:]])

        self.handler.triggerDevices(signal)
        dmm_results = self.handler.getMeasResults()
        daq_results = self.handler.analogInResults
        self.handler.closeAnalogOutputTask()
        self.ss.writeData(iteration,self.niDMM.keys(),dmm_results)
        self.ss.writeData(iteration,self.niInput.keys(), daq_results)

    def doDemag(self,signal):
        print("Do Demag")
        niDMM = self.__define_niDMM_Demag()
        self.handler.connectHardware(analogOutDict=self.niOutput,switchSlotName="PXI1Slot13")        
        self.handler.triggerDevices(signal)
        time.sleep(self.ss.readInfoValue("timeDemag"))
        self.handler.closeAnalogOutputTask()
        time.sleep(1)
        print("Demag finished")
