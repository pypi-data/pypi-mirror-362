#%% Imports
import numpy as np
import warnings
from collections.abc import Iterable

#%% Define Warnings
warnings.simplefilter("ignore", UserWarning)

#%% Define class
class PXIPreProcessing:
  def __init__(self,
                peakIBoundaryU: float = 0,
                peakIBoundaryL: float = 0,
                frequency: float = 0,
                numPeriods: int = 0,
                sampleFrequency: int = 0,
                numIntervalls: int = 0,
                mainSignal: np.array = np.zeros((1, 1)),
                upSignal: np.array = np.zeros((1, 1)),
                downSignal: np.array = np.zeros((1, 1))):

      self.peakIBoundaryU = peakIBoundaryU
      self.peakIBoundaryL = peakIBoundaryL
      self.F = frequency
      self.numPeriods = numPeriods
      self.sF = sampleFrequency
      self.numIntervalls = numIntervalls
      self.mainSignal= mainSignal
      self.upSignal = upSignal
      self.downSignal = downSignal
      self.outSignal = []
      self.outSignalNew = []
    
      self.createOutputSignal()

  def createOutputSignal(self):
    for i in range(self.numIntervalls):
      temp_list = []
      for upSignal, mainSignal, downSignal in zip(self.upSignal, self.mainSignal, self.downSignal):
          if self.peakIBoundaryL == False and self.numIntervalls == 1:
              signal = np.concatenate((upSignal,mainSignal,downSignal))
              temp_list.append(self.peakIBoundaryU*signal)
          elif self.peakIBoundaryL == False and isinstance(self.peakIBoundaryU,Iterable):
              peakCurrent = self.peakIBoundaryU[i]
              signal = np.concatenate((upSignal,mainSignal,downSignal))
              temp_list.append(peakCurrent*signal)
          else:    
              peakCurrent = self.peakIBoundaryU - (self.peakIBoundaryU - self.peakIBoundaryL)*i / (self.numIntervalls-1)
              signal = np.concatenate((upSignal,mainSignal,downSignal))
              temp_list.append(peakCurrent*signal)

      self.outSignalNew.append(temp_list)
      
  def getTA0(self):
      return np.transpose(np.arange(0, (np.asarray(self.outSignal[0]).size - 1) / self.sF + 1 / self.sF, 1 / self.sF))

  def getNDMM(self):
      return len(self.outSignal[0])

  def getTDMM(self):
      return np.arange(0, (self.getNDMM() - 1) / self.sF + 1 / self.sF, 1 / self.sF)

  def getOutputSignal(self, iteration):
      allSignalsOfIteration = self.outSignalNew[iteration]
      for i in range(len(allSignalsOfIteration)):
          signal = allSignalsOfIteration[i]
          allSignalsOfIteration[i] = signal
      return allSignalsOfIteration
