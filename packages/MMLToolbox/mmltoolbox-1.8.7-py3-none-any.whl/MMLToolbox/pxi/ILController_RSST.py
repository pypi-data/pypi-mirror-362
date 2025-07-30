import numpy as np
import sys
import matplotlib.pyplot as plt

import MMLToolbox.pxi.PXIPostProcessing as PXIPostProcessing
from MMLToolbox.pxi.StoreSetup import StoreSetup
from MMLToolbox.pxi.SignalHandler import SignalHandler
from MMLToolbox.pxi.PXIHandler import PXIHandler
from MMLToolbox.util.types import *

MU_0 = 4*np.pi*1e-7


class ILController_RSST:
    def __init__(self, storeSetup:StoreSetup,meas_type=str,use_previous_U=False,do_demag=False,I_limit=30,U_limit=450,maxIterations=10,n_mean=30):
        self.ss = storeSetup
        self.meas_type = meas_type
        self.signal_handler = SignalHandler(storeSetup,meas_type,do_demag)
        self.pxi_handler = PXIHandler(storeSetup)
        self.use_previous_U = use_previous_U
        self.do_demag = do_demag
        self.n_mean = n_mean

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
        self.U_error = None

        # ILC Parameter
        self.frequency = self.ss.readInfoValue("frequency")
        self.sample_freq = self.frequency*self.ss.readInfoValue("sampleFrequencyFactor")
        self.k_p = None
        self.max_iterations = maxIterations
        self.ilc_iter = None
        self.B_amp = None
        self.I_limit = I_limit
        self.U_limit = U_limit
        self.rohrer_voltage_factor = self.ss.readInfoValue("Rohrer_voltage_factor")

        # ILC Storage
        self.store_dict = {}
        self.__Bx_iter = None
        self.__By_iter = None
        self.__Ux_output = None
        self.__Uy_output = None
        self.__B_amp = None
        self.__U_init = None
        self.__U_output = None
    
    ################################################
    # User Function
    ################################################
    def startILCAlgorithm(self):
        if self.do_demag:
          self.__do_demag_procedure()

        U_previous = self.ss.readInfoValue("U_init")
        for steps_iter,B_value in enumerate(self.B_values):
            self.steps_iteration = steps_iter
            self.__reset_storage_for_ilc_algorithm()
            self.U_output = self.signal_handler.getBaseOutSignal()*self.U_init
            self.B_ref = self.__define_ref_signal(B_value)
            self.B_targ = np.max(self.B_ref,axis=1)

            for ilc_iter in range(self.max_iterations):
                self.ilc_iter = ilc_iter
                self.pxi_handler.doMeasurement(signal=self.U_output,iteration=steps_iter)
                self.__postprocessing_measurement_data()
                if ilc_iter == 0:
                    self.k_p = self.__get_ilc_factor()
                self.__compute_error()
                self.U_output = self.__get_new_excitation_signal()
                self.__check_voltage_and_current_limit_reached()
                self.__handle_signal_for_uniaxial()
                self.__store_ilc_values()
                if self.__is_stopping_criteria_fullfilled():
                    break
                
            self.__get_new_U_init()
            self.__write_ilc_values_to_store_setup()
            
            if self.use_previous_U and steps_iter == 0:
                    U_previous = self.U_init               
        return U_previous

    ################################################
    # ILC Function
    ################################################
    def __compute_error(self):
        max_ref = np.max(self.B_ref,axis=1)
        max_meas = np.max(self.B_meas,axis=1)
        self.B_amp = max_meas
        err = max_ref - max_meas
        self.err = err.reshape(2,-1)
        self.B_tol = np.array([max_ref*1.02+1e-4,max_ref*0.98-1e-4])
    
    def __get_ilc_factor(self):
        U_meas_peak = np.max(self.U_output,axis=1)
        B_peak = np.max(self.B_meas,axis=1)
        k_sys_B = B_peak/U_meas_peak
        k_sys_B[np.abs(k_sys_B) < 1e-8] = np.inf
        k_p = 1/k_sys_B
        return k_p.reshape(2,-1)

    def __is_stopping_criteria_fullfilled(self):
        if np.all(self.B_amp<=self.B_tol[0,:]) and np.all(self.B_amp>=self.B_tol[1,:]):
            print(f"\n\n#############################\nCriteria fullfilled for: \nBx_amp={self.B_targ[0]:.2f}T \nBy_amp={self.B_targ[1]:.2f}T \n#############################\n\n")
            return True
        else:
            return False    
        
    def __get_new_U_init(self):
        U_max = np.max(self.U_output,axis=1)
        U_init = np.sqrt(U_max[0]**2+U_max[1]**2)
        self.U_init = U_init            

    ################################################
    # Signal Function
    ################################################
    def __get_new_excitation_signal(self):
        err = self.k_p*self.err*self.signal_handler.getBaseOutSignal()
        U_new = self.U_output + err
        return U_new
        
    def __postprocessing_measurement_data(self):
        len_up = self.signal_handler.len_up_signal
        len_down = self.signal_handler.len_down_signal
        len_up_DAQ = self.signal_handler.len_up_signal_DAQ
        len_down_DAQ = self.signal_handler.len_down_signal_DAQ

        U_B_meas_x = self.ss.readData(self.steps_iteration,"Bx")[len_up:-len_down]
        U_B_meas_y = self.ss.readData(self.steps_iteration,"By")[len_up:-len_down]
        self.U_B_meas = np.array([U_B_meas_x,U_B_meas_y])

        B_meas_x = self.__U_B_to_B("Bx",U_B_meas_x)
        B_meas_y = self.__U_B_to_B("By",U_B_meas_y)
        self.B_meas = np.array([B_meas_x,B_meas_y])

        U_meas_x = self.ss.readData(self.steps_iteration,"Ux")[len_up_DAQ:-len_down_DAQ]*self.ss.readInfoValue("Rohrer_voltage_factor")
        U_meas_y = self.ss.readData(self.steps_iteration,"Uy")[len_up_DAQ:-len_down_DAQ]*self.ss.readInfoValue("Rohrer_voltage_factor")
        self.U_meas = np.array([U_meas_x,U_meas_y])

        I_meas_x = self.ss.readData(self.steps_iteration,"Ix")[len_up_DAQ:-len_down_DAQ]*self.ss.readInfoValue("Rohrer_current_factor")
        I_meas_y = self.ss.readData(self.steps_iteration,"Iy")[len_up_DAQ:-len_down_DAQ]*self.ss.readInfoValue("Rohrer_current_factor")
        self.I_meas = np.array([I_meas_x,I_meas_y])
    
    def __U_B_to_B(self,name,data):
        area = self.ss.readInfoValue(f"{name}_mat_area")
        amp = self.ss.readInfoValue(f"B_amp")
        turns = self.ss.readInfoValue(f"B_turns")
        t = self.ss.readInfoValue("time")
        
        signal = PXIPostProcessing.calc_BCoil(data,self.sample_freq,self.frequency,self.n_mean,t,amp,turns,area)
        return signal
    
    def __define_ref_signal(self,B_amp):
        B_ref = self.signal_handler.getBaseRefSignal()[:,self.signal_handler.len_up_signal:-self.signal_handler.len_down_signal]*B_amp
        return B_ref

    def __check_voltage_and_current_limit_reached(self):
        if np.max(self.U_output) > self.U_limit or np.max(self.I_meas) > self.I_limit:
            sys.exit(f"U > {self.U_limit:.2f} or I > {self.I_limit:.2f}")

    def __handle_signal_for_uniaxial(self):
        phi = int(self.ss.readInfoValue("phi"))
        if self.meas_type == UNIAXIAL and (phi == 0 or phi==180):
            self.U_B_meas[1,:] = 0
            self.B_meas[1,:] = 0
            self.I_meas[1,:] = 0
            self.U_meas[1,:] = 0
            self.U_output[1,:] = 0
            self.B_amp[1] = 0
        elif self.meas_type == UNIAXIAL and phi == 90:
            self.U_B_meas[0,:] = 0
            self.B_meas[0,:] = 0
            self.I_meas[0,:] = 0
            self.U_meas[0,:] = 0
            self.U_output[0,:] = 0
            self.B_amp[0] = 0

    ################################################
    # Storage Function
    ################################################
    def __reset_storage_for_ilc_algorithm(self):
        self.__Bx_iter = []
        self.__By_iter = []
        self.__Ux_output = []
        self.__Uy_output = []
        self.__B_amp = []
        self.__U_init = []
        self.__U_output = []

    def __store_ilc_values(self):
        self.__Bx_iter.append(self.B_meas[0,:].flatten())
        self.__By_iter.append(self.B_meas[1,:].flatten())
        self.__Ux_output.append(self.U_output[0,:].flatten())
        self.__Uy_output.append(self.U_output[1,:].flatten())
        self.__U_output.append(np.max(self.U_output,axis=1).flatten())
        self.__B_amp.append(self.B_amp)
        U_temp = np.max(self.U_output,axis=1)
        U_temp = np.sqrt(U_temp[0]**2+U_temp[1]**2)
        self.__U_init.append(U_temp)

    def __write_ilc_values_to_store_setup(self):
        self.__write_ilc_value_to_store_setup("Bx",self.__Bx_iter)
        self.__write_ilc_value_to_store_setup("By",self.__By_iter)
        self.__write_ilc_value_to_store_setup("Ux",self.__Ux_output)
        self.__write_ilc_value_to_store_setup("Uy",self.__Uy_output)
        self.__write_ilc_value_to_store_setup("B_amp",self.__B_amp)
        self.__write_ilc_value_to_store_setup("B_tol",self.B_tol)
        self.__write_ilc_value_to_store_setup("U_init",self.__U_init)
        self.__write_ilc_value_to_store_setup("B_targ",self.B_targ)
        self.__write_ilc_value_to_store_setup("U_output",self.__U_output)

    def __write_ilc_value_to_store_setup(self,name,data):
        data = np.array(data)
        self.ss.writeILC(self.steps_iteration,name,data)

    ################################################
    # Helper Function
    ################################################          
    def __do_demag_procedure(self):
        signal = self.signal_handler.getDemagSignal()*(self.U_init*1.3+0.2)
        self.pxi_handler.doDemag(signal=signal)
        


