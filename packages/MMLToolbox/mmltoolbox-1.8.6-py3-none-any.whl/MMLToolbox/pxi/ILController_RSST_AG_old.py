import matplotlib.pyplot as plt
import numpy as np
import sys
import scipy.integrate
from scipy.fft import fft, ifft, fftfreq

import MMLToolbox.pxi.PXIPostProcessing as PXIPostProcessing
from MMLToolbox.pxi.StoreSetup import StoreSetup
from MMLToolbox.pxi.SignalHandler import SignalHandler
from MMLToolbox.pxi.PXIHandler import PXIHandler
from MMLToolbox.util.types import *

MU_0 = 4*np.pi*1e-7


class ILController_RSST_AG:
    def __init__(self, storeSetup:StoreSetup, meas_type=str, cutfrequency:int=1000, I_limit=30, U_limit=450,maxIterations=10,n_mean=1):
        self.ss = storeSetup
        self.meas_type = meas_type
        self.signal_handler = SignalHandler(storeSetup,meas_type)
        self.pxi_handler = PXIHandler(storeSetup)

        # Measurement Parameter
        self.U_init = storeSetup.readInfoValue("U_init")
        self.B_values = storeSetup.readInfoValue("B_values")
        self.steps_iteration = 0
        self.U_B_meas = None
        self.B_meas = None
        self.U_meas = None
        self.I_meas = None

        # Signal
        self.B_ref = None
        self.U_B_ref = None
        self.ref_signal = None
        self.U_output = None
        self.phase_shift = None
        self.B_shift = None

        # ILC Parameter
        self.cutfrequency = cutfrequency
        self.frequency = self.ss.readInfoValue("frequency")
        self.sample_freq = self.ss.readInfoValue("sampleFrequency")
        self.k_p = None
        self.max_iterations = maxIterations
        self.err = None
        self.ilc_iter = None
        self.FF_tol = 0
        self.S_tol = 0
        self.B_tol = 0
        self.FF = None
        self.S = None
        self.B_amp = None
        self.I_limit = I_limit
        self.U_limit = U_limit
        self.rohrer_voltage_factor = self.ss.readInfoValue("Rohrer_voltage_factor")

        # ILC Storage
        self.__Bx_iter = None
        self.__By_iter = None
        self.__Ux_output = None
        self.__Uy_output = None
        self.__errx = None
        self.__erry = None
        self.__FF = None
        self.__S = None
        self.__B_amp = None
        self.__U_init = []
    
    ################################################
    # User Function
    ################################################
    def startILCAlgorithm(self):
       
        for steps_iter,B_value in enumerate(self.B_values):
            self.steps_iteration = steps_iter
            self.__U_init.append(self.U_init)
            self.__reset_storage_for_ilc_algorithm()
            self.__do_init_measurement()
            self.__define_ref_signal(B_value)

            for ilc_iter in range(self.max_iterations):
                self.ilc_iter = ilc_iter
                self.__handle_signal_for_uniaxial()
                self.__shift_signal()
                self.__compute_error()
                if self.__is_stopping_criteria_fullfilled():
                    break
                signal = self.__get_new_excitation_signal()
                self.__check_voltage_and_current_limit_reached()
                self.pxi_handler.doMeasurement(signal=signal,iteration=steps_iter)
                self.__postprocessing_measurement_data()
            self.__get_new_U_init()
            self.__write_ilc_values_to_store_setup()



    ################################################
    # ILC Function
    ################################################
    def __do_init_measurement(self):
        signal = self.signal_handler.getBaseOutSignal()*self.U_init
        self.pxi_handler.doMeasurement(signal=signal,iteration=self.steps_iteration)
        self.U_output = signal[:,self.signal_handler.len_up_signal:-self.signal_handler.len_down_signal]
        self.__postprocessing_measurement_data()
        #self.__check_correlation_init_and_meas()
        main_signal = signal[:,self.signal_handler.len_up_signal:-self.signal_handler.len_down_signal]
        self.phase_shift = self.__get_phase_shift(ref_signals=main_signal,shift_signals=self.B_meas)
        self.k_p = self.__getILCFactor()

    def __compute_error(self):
        if self.frequency > self.cutfrequency:
            err = self.U_B_ref-self.U_B_meas
            self.tol = np.max(self.U_B_ref)*0.03
            self.FF_tol = 1.3
        else:
            self.err = self.B_ref-self.B_shift
            self.S_tol = np.max(self.B_ref,axis=1)*0.1
            B_tol_max = np.max(self.B_ref,axis=1)
            self.B_tol = np.array([B_tol_max*1.05,B_tol_max*0.95])
            self.FF_tol = 1.3
    
    def __getILCFactor(self):
        U_meas_peak = np.max(self.U_output,axis=1)
        U_B_peak = np.max(self.U_B_meas,axis=1)
        B_peak = np.max(self.B_meas,axis=1)

        k_sys_U = U_B_peak/U_meas_peak
        k_sys_B = B_peak/U_meas_peak

        if self.frequency > self.cutfrequency:
            k_p = 1/k_sys_U
        else:
            k_p = 1/k_sys_B 

        return k_p.reshape(2,-1)

    def __is_stopping_criteria_fullfilled(self):
        S = np.sqrt(np.mean(self.err**2,axis=1))
        U_B_eff = np.sqrt(np.mean(self.U_B_meas**2, axis=1))
        U_B_glr = np.mean(np.abs(self.U_B_meas), axis=1)

        B_eff = np.sqrt(np.mean(self.B_shift**2, axis=1))
        B_glr = np.mean(np.abs(self.B_shift), axis=1) 

        if self.frequency > self.cutfrequency:
            FF = U_B_eff/U_B_glr
        else:
            FF = B_eff/B_glr 

        FF = np.nan_to_num(FF, nan=0)
        B_amp = np.max(self.B_shift,axis=1)
        self.S = S
        self.FF = FF
        self.B_amp = B_amp
        self.__store_ilc_values()

        if np.all(S<self.S_tol) and np.all(FF<self.FF_tol) and np.all(B_amp<self.B_tol[0,:]) and np.all(B_amp>self.B_tol[1,:]):
            print(f"Criteria are for B_values={self.B_values[self.steps_iteration]}T fullfilled!")
            return True
        else:
            return False    
        
    def __get_new_U_init(self):
        U_max = np.max(self.U_output,axis=1)
        U_amp = np.sqrt(U_max[0]**2+U_max[1]**2)
        self.U_init = U_amp            


    ################################################
    # Signal Function
    ################################################
    def __get_new_excitation_signal(self):
        U_new = self.U_output + self.k_p*self.err
        self.U_output = U_new
        U_output = self.signal_handler.get_complite_output_signal(U_new)
        return U_output
        
    def __postprocessing_measurement_data(self):
        len_up = self.signal_handler.len_up_signal
        len_down = self.signal_handler.len_down_signal
        U_B_meas_x = self.ss.readData(self.steps_iteration,"Bx")[len_up:-len_down]
        U_B_meas_y = self.ss.readData(self.steps_iteration,"By")[len_up:-len_down]
        self.U_B_meas = np.array([U_B_meas_x,U_B_meas_y])

        B_meas_x = self.__U_B_to_B("Bx",U_B_meas_x)
        B_meas_y = self.__U_B_to_B("By",U_B_meas_y)
        self.B_meas = np.array([B_meas_x,B_meas_y])

        U_meas_x = self.ss.readData(self.steps_iteration,"Ux")[len_up:-len_down]*self.ss.readInfoValue("Rohrer_voltage_factor")
        U_meas_y = self.ss.readData(self.steps_iteration,"Uy")[len_up:-len_down]*self.ss.readInfoValue("Rohrer_voltage_factor")
        self.U_meas = np.array([U_meas_x,U_meas_y])

        I_meas_x = self.ss.readData(self.steps_iteration,"Ix")[len_up:-len_down]*self.ss.readInfoValue("Rohrer_current_factor")
        I_meas_y = self.ss.readData(self.steps_iteration,"Iy")[len_up:-len_down]*self.ss.readInfoValue("Rohrer_current_factor")
        self.I_meas = np.array([I_meas_x,I_meas_y])
    
    def __U_B_to_B(self,name,data):
        area = self.ss.readInfoValue(f"{name}_mat_area")
        amp = self.ss.readInfoValue(f"B_amp")
        turns = self.ss.readInfoValue(f"B_turns")
        t = self.ss.readInfoValue("time")
        
        mean_data = data - np.mean(data)
        int_data = scipy.integrate.cumtrapz(mean_data,t,initial=0)/(amp*turns*area)
        int_data = int_data - (max(int_data)+min(int_data))/2
        return int_data
    
    def __B_to_U_B(self,name,data):
        sample_frequency = self.ss.readInfoValue("sampleFrequency") 
        area = self.ss.readInfoValue(f"{name}_mat_area")
        amp = self.ss.readInfoValue(f"B_amp")
        turns = self.ss.readInfoValue(f"B_turns")
        dB_grad = np.gradient(data)
        U_B = (turns*area*amp*sample_frequency)*dB_grad
        return U_B
    
    def __check_correlation_init_and_meas(self):
        if (max_B_meas:=np.max(np.abs(self.B_meas))) > self.B_values[0]*1.3:
              sys.exit(f"Please decrease U_init!\n max_B_meas={max_B_meas:.2f}\n B_wanted={self.B_values[0]:.2f}")
        elif (max_B_meas:=np.max(np.abs(self.B_meas))) < self.B_values[0]*0.7:
              sys.exit(f"Please increase U_init! \n max_B_meas={max_B_meas:.2f}\n B_wanted={self.B_values[0]:.2f}") 

    def __get_phase_shift(self,ref_signals,shift_signals):
        phase_shift = []
        for ref_signal, shift_signal in zip(ref_signals,shift_signals):
          #signal_A = ref_signal[self.signal_handler.len_up_signal:-self.signal_handler.len_down_signal]
          #signal_B = shift_signal[self.signal_handler.len_up_signal:-self.signal_handler.len_down_signal]
          temp_A = PXIPostProcessing.calc_average(ref_signal,self.sample_freq,self.frequency,1)
          temp_B = PXIPostProcessing.calc_average(shift_signal,self.sample_freq,self.frequency,1)

          spectrum_A = fft(temp_A)
          spectrum_B = fft(temp_B)
          n = len(temp_B)

          positive_magnitudes = np.abs(spectrum_A[:n // 2])
          dominant_idx = np.argmax(positive_magnitudes[1:]) + 1  

          phase_A = np.angle(spectrum_A[dominant_idx])
          phase_B = np.angle(spectrum_B[dominant_idx])
          phase_difference = phase_B - phase_A

          temp_phase_shift = int(np.round((phase_difference / (2 * np.pi)) * n))
          phase_shift.append(temp_phase_shift)
        return np.array(phase_shift).reshape(2,-1)
    
    def __shift_signal(self):
        shift_signals = []
        for signal,shift in zip(self.B_meas,self.phase_shift):
            temp = np.roll(signal,shift)
            shift_signals.append(temp)
        self.B_shift = np.array(shift_signals).reshape(2,-1)

    def __define_ref_signal(self,B_amp):
        self.B_ref = self.signal_handler.getBaseOutSignal()[:,self.signal_handler.len_up_signal:-self.signal_handler.len_down_signal]*B_amp
        U_B_x = self.__B_to_U_B("Bx",self.B_ref[0,:])
        U_B_y = self.__B_to_U_B("By",self.B_ref[1,:])
        self.U_B_ref = np.array([U_B_x, U_B_y])

    def __check_voltage_and_current_limit_reached(self):
        if np.max(self.U_output) > self.U_limit or np.max(self.I_meas) > self.I_limit:
            sys.exit(f"U > {self.U_limit:.2f} or I > {self.I_limit:.2f}")

    def __handle_signal_for_uniaxial(self):
        phi = int(self.ss.readInfoValue("phi"))
        if self.meas_type == UNIAXIAL and phi == 0:
            self.U_B_meas[1,:] = 0
            self.B_meas[1,:] = 0
            self.I_meas[1,:] = 0
            self.U_meas[1,:] = 0
        elif self.meas_type == UNIAXIAL and phi == 90:
            self.U_B_meas[0,:] = 0
            self.B_meas[0,:] = 0
            self.I_meas[0,:] = 0
            self.U_meas[0,:] = 0

    ################################################
    # Storage Function
    ################################################
    def __reset_storage_for_ilc_algorithm(self):
        self.__Bx_iter = []
        self.__By_iter = []
        self.__Ux_output = []
        self.__Uy_output = []
        self.__errx = []
        self.__erry = []
        self.__FF = []
        self.__S = []
        self.__B_amp = []

    def __store_ilc_values(self):
        self.__Bx_iter.append(self.B_meas[0,:].flatten())
        self.__By_iter.append(self.B_meas[1,:].flatten())
        self.__Ux_output.append(self.U_output[0,:].flatten())
        self.__Uy_output.append(self.U_output[1,:].flatten())
        self.__errx.append(self.err[0,:])
        self.__erry.append(self.err[1,:])
        self.__FF.append(self.FF)
        self.__S.append(self.S)
        self.__B_amp.append(self.B_amp)

    def __write_ilc_values_to_store_setup(self):
        self.__write_ilc_value_to_store_setup("Bx",self.__Bx_iter)
        self.__write_ilc_value_to_store_setup("By",self.__By_iter)
        self.__write_ilc_value_to_store_setup("Ux",self.__Ux_output)
        self.__write_ilc_value_to_store_setup("Uy",self.__Uy_output)
        self.__write_ilc_value_to_store_setup("errx",self.__errx)
        self.__write_ilc_value_to_store_setup("erry",self.__erry)

        self.__write_ilc_value_to_store_setup("FF",self.__FF)
        self.__write_ilc_value_to_store_setup("S",self.__S)
        self.__write_ilc_value_to_store_setup("B_amp",self.__B_amp)
        self.__write_ilc_value_to_store_setup("S_tol",self.S_tol.reshape(1,-1))
        self.__write_ilc_value_to_store_setup("B_tol",self.B_tol)
        self.__write_ilc_value_to_store_setup("FF_tol",self.FF_tol)
        self.__write_ilc_value_to_store_setup("U_init",self.__U_init)

    def __write_ilc_value_to_store_setup(self,name,data):
        data = np.array(data)
        self.ss.writeILC(self.steps_iteration,name,data)
        


