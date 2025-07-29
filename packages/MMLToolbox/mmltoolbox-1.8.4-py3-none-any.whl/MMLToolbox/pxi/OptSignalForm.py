import numpy as np
import scipy.optimize as opt

import MMLToolbox.pxi.PXIPostProcessing as PXIPostProcessing
from MMLToolbox.pxi.StoreSetup import StoreSetup
from MMLToolbox.pxi.SignalHandler import SignalHandler
from MMLToolbox.pxi.PXIHandler import PXIHandler
from MMLToolbox.util.types import *

MU_0 = 4*np.pi*1e-7

class StopOptimization(Exception):
    pass

class OptSignalForm:
    def __init__(self, storeSetup:StoreSetup,meas_type=str,use_previous_U=False,do_demag=False,step=0.1,epsilon=0.05,maxIterations=10,n_mean=30):
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
        self.phi = storeSetup.readInfoValue("phi")
        self.steps_iteration = 0
        self.U_B_meas = None
        self.B_meas = None
        self.U_meas = None
        self.I_meas = None

        # Optimization Parameter
        self.frequency = self.ss.readInfoValue("frequency")
        self.sample_freq = self.frequency*self.ss.readInfoValue("sampleFrequencyFactor")
        self.bounds = [(0,4),(0,4)]
        self.epsilon = epsilon
        self.step = step
        self.max_iterations = maxIterations
        self.rohrer_voltage_factor = self.ss.readInfoValue("Rohrer_voltage_factor")

        # Optimization Storage
        self.store_dict = {}
        self.__B_iter_max = None
        self.__U_init = None
        self.__Error = None
        self.__Phi_real = None
    
    ################################################
    # User Function
    ################################################
    def startOPTalgorithm(self):
        if self.do_demag:
          self.__do_demag_procedure()

        U_previous = self.ss.readInfoValue("U_init")
        for steps_iter,self.B_value in enumerate(self.B_values):
            self.steps_iteration = steps_iter
            self.__reset_storage_for_opt_algorithm()
            self.__check_for_unixial()
            self.B_target = [self.B_value*np.cos(np.radians(self.phi)),self.B_value*np.sin(np.radians(self.phi))]
            initial_simplex = np.array([self.U_init, self.U_init + np.array([self.step, 0.0]), self.U_init + np.array([0.0, self.step])])

            if self.steps_iteration > 0:
                corr_factor = self.B_values[steps_iter]/self.B_values[steps_iter-1]
                self.U_init = self.U_init*corr_factor
                initial_simplex = np.array([self.U_init, self.U_init + np.array([self.step*0.25, 0.0]), self.U_init + np.array([0.0, self.step*0.25])])

            try:
                result = opt.minimize(self.__function_to_minimize,self.U_init,method='Nelder-Mead',bounds=self.bounds,options={'initial_simplex': initial_simplex, 'adaptive':True,'maxiter':self.max_iterations,"disp":True})
                self.U_init = result['x']
                self.pxi_handler.doMeasurement(signal=self.signal_handler.getBaseOutSignal()*self.U_init.reshape(2,1),iteration=self.steps_iteration)
                self.__postprocessing_measurement_data()
                self.error = self.__compute_error()
            except StopOptimization as e:
                print("Optimization stopped early:", e)
                self.U_init = abs(self.U_opt.reshape(2,))
            
            self.__write_opt_values_to_store_setup()
            
            if self.use_previous_U and steps_iter == 0:
                    U_previous = self.U_init             
        return U_previous

    ################################################
    # Optimization Function
    ################################################
    def __function_to_minimize(self,U):
        self.U_opt = U.reshape(2,1)*[[np.sign(self.B_target[0])], [np.sign(self.B_target[1])]]
        self.pxi_handler.doMeasurement(signal=self.signal_handler.getBaseOutSignal()*self.U_opt,iteration=self.steps_iteration)
        self.__postprocessing_measurement_data()
        self.error = self.__compute_error()
        self.__store_optimization_values()
        print(f'U = {U}')
        print(f'Error = {self.error:.6f}\n')
        
        if self.error < self.epsilon:
            raise StopOptimization(f"Function value {self.error:.6f} below threshold. Stopping.")
        
        return self.error

    def __compute_error(self):
        # Get maximum of measured Magnetic Field B    
        Bx_meas_max = np.max(self.B_meas[0,:])*np.sign(self.B_target[0])
        By_meas_max = np.max(self.B_meas[1,:])*np.sign(self.B_target[1])

        print(f'\nBx_meas={Bx_meas_max:.3f}, By_meas={By_meas_max:.3f}'), print(f'Bx_targ={self.B_target[0]:.3f}, By_targ={self.B_target[1]:.3f}')

        # Calculate vector-based error 
        B_meas_vector = np.array([Bx_meas_max,By_meas_max])
        B_target_vector = np.array([self.B_target[0],self.B_target[1]])
        error = np.linalg.norm(B_meas_vector - B_target_vector) / self.B_value
        return error
    
    def __check_for_unixial(self):
        if (self.phi == 0 or self.phi == 180):
            self.bounds = [(0,4),(0,0)]
            self.y_factor = 0.0
            self.x_factor = 1.0

        elif self.phi == 90 or self.phi == 270:
            self.bounds = [(0,0),(0,4)]
            self.x_factor = 0.0
            self.y_factor = 1.0

        else:
            self.bounds = [(0,4),(0,4)]
            self.x_factor = 1.0
            self.y_factor = 1.0
                
    ################################################
    # Signal Function
    ################################################
    def __postprocessing_measurement_data(self):
        len_up = self.signal_handler.len_up_signal
        len_down = self.signal_handler.len_down_signal
        len_up_DAQ = self.signal_handler.len_up_signal_DAQ
        len_down_DAQ = self.signal_handler.len_down_signal_DAQ

        U_B_meas_x = self.ss.readData(self.steps_iteration,"Bx")[len_up:-len_down]
        U_B_meas_y = self.ss.readData(self.steps_iteration,"By")[len_up:-len_down]
        self.U_B_meas = np.array([U_B_meas_x,U_B_meas_y])

        B_meas_x = self.__U_B_to_B("Bx",U_B_meas_x)*self.x_factor
        B_meas_y = self.__U_B_to_B("By",U_B_meas_y)*self.y_factor
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

    ################################################
    # Storage Function
    ################################################
    def __reset_storage_for_opt_algorithm(self):
        self.__B_iter_max = []
        self.__U_init = []
        self.__Error = []
        self.__Phi_real = []

    def __store_optimization_values(self):
        self.__B_iter_max.append([np.max(self.B_meas[0,:]),np.max(self.B_meas[1,:])])
        self.__U_init.append(self.U_opt.flatten())
        self.__Error.append(self.error)
        self.__Phi_real.append(np.degrees(np.arctan2(np.max(self.B_meas[1,:])*np.sign(self.B_target[0]),np.max(self.B_meas[0,:])*np.sign(self.B_target[1]))))

    def __write_opt_values_to_store_setup(self):
        self.__write_opt_value_to_store_setup("B_max",self.__B_iter_max)       
        self.__write_opt_value_to_store_setup("U_init",self.__U_init)
        self.__write_opt_value_to_store_setup("B_targ",self.B_target)
        self.__write_opt_value_to_store_setup("Error",self.__Error)
        self.__write_opt_value_to_store_setup("Phi_real",self.__Phi_real)
        self.__write_opt_value_to_store_setup("Phi_targ",self.phi)

    def __write_opt_value_to_store_setup(self,name,data):
        data = np.array(data)
        self.ss.writeILC(self.steps_iteration,name,data)

    ################################################
    # Helper Function
    ################################################          
    def __do_demag_procedure(self):
        signal = self.signal_handler.getDemagSignal()*1
        self.pxi_handler.doDemag(signal=signal)
        


