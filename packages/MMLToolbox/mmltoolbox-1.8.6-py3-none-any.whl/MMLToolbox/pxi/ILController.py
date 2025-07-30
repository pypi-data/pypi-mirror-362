import matplotlib.pyplot as plt
import numpy as np

class ILController:

    def __init__(self, measurementParams:dict, cutfrequency, i_max, U_max, U2_ref, B_ref,maxIterations,outputSignals:dict, measurementDeviceSpecs:dict, peakIBoundaryU):
        
        self.sampleFrequency = measurementParams['sampleFrequency']
        self.frequency = measurementParams['frequency']
        self.wavepoints = measurementParams['wavepoints']
        self.n_mean = measurementParams['n_mean']

        self.cutfrequency = cutfrequency

        self.i_max = i_max
        self.U_max = U_max
        
        self.U2_ref = U2_ref
        self.B_ref = B_ref

        self.maxIterations = maxIterations

        self.mainSteps = outputSignals['mainSteps']
        self.upSteps = outputSignals['upSteps']
        self.downSteps = outputSignals['downSteps']
        self.zeroSteps = outputSignals['zeroSteps']

        self.S = np.zeros(maxIterations)
        self.FF = np.zeros(maxIterations)

        self.amp_e_up = np.linspace(0,1,len(self.upSteps))
        self.amp_e_down = np.linspace(1,0,len(self.downSteps))

        self.Rohrer_voltage_factor = measurementDeviceSpecs['Rohrer_voltage_factor']
        self.Rohrer_current_factor= measurementDeviceSpecs['Rohrer_current_factor']

        self.peakIBoundaryU = peakIBoundaryU


    def getRMS(self, B_corr, B_ref):
        #TODO: bei B_ref[5000:6000] warum?
        e_JA_B = B_corr - B_ref[5000:6000]
        RMS = np.sqrt(np.sum(e_JA_B**2)/len(e_JA_B))

        return RMS
    
    def getTOLJA(self, B_ref):
        tol_JA = max(B_ref)*0.02
        return tol_JA
    
    def getFFB(self, B_corr):
        B_eff = np.sqrt(1/len(B_corr)*np.sum(B_corr**2))
        B_glr = 1/len(B_corr)*np.sum(abs(B_corr))
        FF_B = B_eff/B_glr

        return FF_B
    
    def getKP(self, U_new, U2_temp, B_corr):
        U_peak = max(U_new)
        k_sys_U = max(U2_temp)/U_peak
        k_sys_B = max(B_corr)/U_peak

        
        if self.frequency > self.cutfrequency:
            k_p = 0.25/(k_sys_U) #0.5 for 100Hz # 0.25 for 50Hz
            return k_p
        else:
            k_p = 0.1/(k_sys_B) #0.3 before 0.25 works for 1Hz/ 0.4 for 10Hz
            return k_p


    def checkITempBiggerThanIMax(self, I_temp, i_max):
        if max(abs(I_temp)) > i_max:
            i_max_plt = i_max*np.ones(len(I_temp))
            plt.figure()
            plt.plot(I_temp,label="i_calc from J-A Model")
            plt.plot(i_max_plt,'r',label="max current I_prim from Rohrer-Amplifier")
            plt.legend()
            plt.ylabel('i in A')
            plt.xlabel('samples')
            plt.grid("on")
            print("calculated value of I_prim is to high/desired B_peak not possible --> reduce B_peak")
            return True
        else: 
            return False

    def checkCriteriaBeforStart(self, FF_B, RMS, tol_JA):
        print('FF_error = ' + str(abs(FF_B-1.111)) + ' (< 0.01111)')
        print('RMS = ' + str(RMS) + ' (< ' + str(tol_JA) + ')')
        if RMS < tol_JA and abs(FF_B-1.111) < 0.01111:
                print("criteria are met!")
                return True
        print("criteria not met! :(")
        return False
    
    def checkCriteria(self,U2_temp_all, U2_temp, B_corr, B_corr_all, numIterations):
        if self.frequency > self.cutfrequency:
            e = self.U2_ref - U2_temp_all
            tol = max(self.U2_ref)*0.02
            FF_tol = 0.01111
        else:
            e = self.B_ref - B_corr_all
            tol = max(self.B_ref)*0.02
            FF_tol = 0.01111

        e[0:len(self.zeroSteps)] = 0 
        e[-len(self.zeroSteps):] = 0 
        e[len(self.zeroSteps):len(self.zeroSteps)+len(self.upSteps)] = self.amp_e_up*e[len(self.zeroSteps):len(self.zeroSteps)+len(self.upSteps)]
        e[-len(self.zeroSteps)-len(self.upSteps):-len(self.zeroSteps)] = self.amp_e_down*e[-len(self.zeroSteps)-len(self.upSteps):-len(self.zeroSteps)]

        # FF and RMS condition
        self.S[numIterations] = np.sqrt(np.sum(e[5000:6000]**2)/len(e[5000:6000]))

        U2_eff = np.sqrt(1/len(U2_temp)*np.sum(U2_temp**2))
        U2_glr = 1/len(U2_temp)*np.sum(abs(U2_temp))
        B_eff = np.sqrt(1/len(B_corr)*np.sum(B_corr**2))
        B_glr = 1/len(B_corr)*np.sum(abs(B_corr))

        if self.frequency > self.cutfrequency:
            self.FF[numIterations] = U2_eff/U2_glr
        else:
            self.FF[numIterations] = B_eff/B_glr

        if self.S[numIterations] < tol and abs(self.FF[numIterations]-1.111) < FF_tol:
            print("criteria are met!")
            return True
        else:
            return False
        
    def createNewSignal(self, U_new, len_upsignal, len_downsignal, len_mainsignal):
        U_new_fft = np.fft.rfft(U_new)
        U_new_fft_abs = np.abs(U_new_fft)
        freq = np.fft.rfftfreq(self.wavepoints, d=1/self.sampleFrequency)

        U_new_fft_filter = U_new_fft.copy()
        U_new_fft_filter[freq > 10*self.frequency] = 0
        U_new_fft_filter_abs = np.abs(U_new_fft_filter)
        U_new_filtered = np.fft.irfft(U_new_fft_filter)

        if self.frequency > self.cutfrequency:
            upSignal_x = U_new[0:len_upsignal]/(self.peakIBoundaryU*self.Rohrer_voltage_factor)
            mainSignal_x = U_new[len_upsignal:-len_downsignal]/(self.peakIBoundaryU*self.Rohrer_voltage_factor)
            downSignal_x =U_new[-len_downsignal:]/(self.peakIBoundaryU*self.Rohrer_voltage_factor)
        else:
            upSignal_x = U_new_filtered[0:len_upsignal]/(self.peakIBoundaryU*self.Rohrer_voltage_factor)
            mainSignal_x = U_new_filtered[len_upsignal:-len(downSignal_x)]/(self.peakIBoundaryU*self.Rohrer_voltage_factor)
            downSignal_x = U_new_filtered[-len_downsignal:]/(self.peakIBoundaryU*self.Rohrer_voltage_factor)


        mainSignal = [mainSignal_x]
        upSignal = [upSignal_x]
        downSignal = [downSignal_x]

        return [mainSignal, upSignal, downSignal]