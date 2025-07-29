import matplotlib.pyplot as plt
import numpy as np
import sys

from . import StoreSetup
from . import PXIPostProcessing

MU_0 = 4*np.pi*1e-7


class ILController:
    def __init__(self, storeSetup:StoreSetup, cutfrequency:int=30, Imax=45, Umax=450,maxIterations=10,n_mean=1):
        self.ss = storeSetup
        
        # Info Parameter
        self.sampleFrequency = storeSetup.readInfoValue['sampleFrequency']
        self.frequency = storeSetup.readInfoValue['frequency']
        self.wavepoints = storeSetup.readInfoValue['wavepoints']
        self.mainSteps = storeSetup.readInfoValue['lenMainSignalDMM']
        self.upSteps = storeSetup.readInfoValue['lenUpSignalDMM']
        self.downSteps = storeSetup.readInfoValue['lenDownSignalDMM']
        self.zeroSteps = storeSetup.readInfoValue['lenZeroSignalDMM']
        self.Rohrer_voltage_factor = storeSetup.readInfoValue['Rohrer_voltage_factor']
        self.Rohrer_current_factor= storeSetup.readInfoValue['Rohrer_current_factor']
        self.B_turns = storeSetup.readInfoValue['B_turns']
        self.B_area = storeSetup.readInfoValue['B_area']
        self.H_turns = storeSetup.readInfoValue['H_turns']
        self.l_eff = storeSetup.readInfoValue['l_eff']

        # ILC Parameter
        self.cutfrequency = cutfrequency
        self.maxIterations = maxIterations
        self.S = []
        self.FF = []
        self.amp_e_up = np.linspace(0,1,len(self.upSteps))
        self.amp_e_down = np.linspace(1,0,len(self.downSteps))
        self.Imax = Imax
        self.Umax = Umax        
        self.U2_ref = None
        self.B_ref = None
        self.first_iteration = None
        self.U_out = []
        self.n_mean = n_mean
        self.k_p = None
        self.err = None

        # Additional Parameter
        self.J_corr = None
        self.I1_temp = None
        self.M_corr = None
        self.B_corr = None
        self.B_corr_temp = None
        self.U2_temp = None

    def initRefSignal(self,B_ref,U_ref):
        self.first_iteration = True
        self.B_ref = B_ref
        self.U2_ref = U_ref
        self.U_out = None

    def computeVariablesFromMeasurements(self):
        self.U2_temp = self.ss.readData(0,"U2")[self.upSteps:-self.downSteps]
        J_corr = PXIPostProcessing.calc_BCoil(self.U2_temp,self.sampleFrequency,self.frequency,self.n_mean,self.mainSteps,1,self.B_turns,self.B_area)
        self.J_corr = np.concatenate((J_corr, [J_corr[len(J_corr)-1]], [J_corr[len(J_corr)-1]]))  # TODO: Warum müssen wir das so machen

        self.I1_temp = self.ss.readData(0,"I")[self.upSteps:-self.downSteps]*self.Rohrer_current_factor
        self.H_corr = PXIPostProcessing.calc_average(self.I1_temp,self.sampleFrequency,self.frequency,1)*self.H_turns/self.l_eff

        self.M_corr = self.J_corr/MU_0
        self.B_corr = MU_0*(self.H_corr + self.M_corr) 

        B_corr_temp = PXIPostProcessing.calc_BCoil(self.U2_temp,self.sampleFrequency,self.frequency,self.n_mean,self.mainSteps,1,self.B_turns,self.B_area)
        self.B_corr_temp =np.concatenate([B_corr_temp, [B_corr_temp[len(B_corr_temp)-1]]])

    def checkCriteria(self):
        self.__checkCurrentInLimit()
        self.__checkFFandRMS()

    def __getILCFactor(self):
        if self.first_iteration:
            U_peak = np.max(self.U2_ref)
            B_peak = np.max(self.B_ref)
            k_sys_U = np.max(self.U2_temp)/U_peak
            k_sys_B = np.max(self.B_corr)/B_peak

            if self.frequency > self.cutfrequency: self.k_p = 0.25/k_sys_U
            else: self.k_p = 0.1/k_sys_B 

    def __checkCurrentInLimit(self):
        if max(self.I1_temp) > max(self.Imax):
          sys.exit("calculated value of I is to high --> reduce B")


    def __checkFFandRMS(self):
        if self.frequency > self.cutfrequency:
            e = self.U2_ref - self.U2_temp
            tol = max(self.U2_ref)*0.02
            FF_tol = 0.01111
        else:
            e = self.B_ref - self.B_corr
            tol = max(self.B_ref)*0.02
            FF_tol = 0.01111

        e[0:len(self.zeroSteps)] = 0 
        e[-len(self.zeroSteps):] = 0 
        e[len(self.zeroSteps):len(self.zeroSteps)+len(self.upSteps)] = self.amp_e_up*e[len(self.zeroSteps):len(self.zeroSteps)+len(self.upSteps)]
        e[-len(self.zeroSteps)-len(self.upSteps):-len(self.zeroSteps)] = self.amp_e_down*e[-len(self.zeroSteps)-len(self.upSteps):-len(self.zeroSteps)]
        self.err = e

        # FF and RMS condition
        self.S.append(np.sqrt(np.sum(e**2)/len(e)))

        U2_eff = np.sqrt(1/len(self.U2_temp)*np.sum(self.U2_temp**2))
        U2_glr = 1/len(self.U2_temp)*np.sum(abs(self.U2_temp))
        B_eff = np.sqrt(1/len(self.B_corr)*np.sum(self.B_corr**2))
        B_glr = 1/len(self.B_corr)*np.sum(abs(self.B_corr))

        if self.frequency > self.cutfrequency:
            self.FF.append(U2_eff/U2_glr)
        else:
            self.FF.append(B_eff/B_glr)

        if self.S[-1] < tol and abs(self.FF[-1]-1.111) < FF_tol:
            sys.exit("FF and Tol are met")
        else:
            return False
    
        
    def createNewSignal(self):
        self.__getILCFactor()

        self.U_out = self.U_out + self.k_p*self.err 
        # TODO: Das muss ich mir im Labor anschauen, was Franz genau in seinem Code so macht.
        U_new_fft = np.fft.rfft(self.U_out)
        U_new_fft_abs = np.abs(U_new_fft)
        freq = np.fft.rfftfreq(self.wavepoints, d=1/self.sampleFrequency)

        U_new_fft_filter = U_new_fft.copy()
        U_new_fft_filter[freq > 10*self.frequency] = 0
        U_new_fft_filter_abs = np.abs(U_new_fft_filter)
        U_new_filtered = np.fft.irfft(U_new_fft_filter)

        if self.frequency > self.cutfrequency:
            upSignal_x = self.U_out[0:self.upSteps]/self.Rohrer_voltage_factor
            mainSignal_x = self.U_out[self.upSteps:-self.downSteps]/self.Rohrer_voltage_factor
            downSignal_x =self.U_out[-self.downSteps:]/self.Rohrer_voltage_factor
        else:
            upSignal_x = U_new_filtered[0:self.upSteps]/self.Rohrer_voltage_factor
            mainSignal_x = U_new_filtered[self.upSteps:-self.downSteps]/self.Rohrer_voltage_factor
            downSignal_x = U_new_filtered[-self.downSteps:]/self.Rohrer_voltage_factor

        mainSignal = [mainSignal_x]
        upSignal = [upSignal_x]
        downSignal = [downSignal_x]

        return upSignal,mainSignal,downSignal