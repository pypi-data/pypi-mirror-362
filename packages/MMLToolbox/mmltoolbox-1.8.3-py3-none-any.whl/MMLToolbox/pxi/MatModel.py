import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate
import scipy.optimize
import sys

from . import PXIPostProcessing

class MatModel:
    def __init__(self, measurementParams:dict ,outputSignals:dict, tempUnits:dict, measurementDeviceSpecs:dict):
        
        self.sampleFrequency = measurementParams['sampleFrequency']
        self.frequency = measurementParams['frequency']
        self.wavepoints = measurementParams['wavepoints']
        self.n_mean = measurementParams['n_mean']

        self.mainSteps = outputSignals['mainSteps']
        self.upSteps = outputSignals['upSteps']
        self.downSteps = outputSignals['downSteps']
        self.zeroSteps = outputSignals['zeroSteps']

        self.B_turns = measurementDeviceSpecs['B_turns']
        self.B_area = measurementDeviceSpecs['B_area']
        self.H_turns = measurementDeviceSpecs['H_turns']
        self.l_eff = measurementDeviceSpecs['l_eff']
        self.Rohrer_voltage_factor = measurementDeviceSpecs['Rohrer_voltage_factor']
        self.Rohrer_current_factor= measurementDeviceSpecs['Rohrer_current_factor']

    
    def JA_M_calc_params(self, params,H_corr):
        [a,alpha,Ms,k,c] = params
        dH = np.roll(H_corr,-1) - H_corr

        M_corr = self.getM_corr()

        M_an = np.zeros(len(H_corr))
        M_irr = np.zeros(len(H_corr))
        M_calc = np.zeros(len(H_corr))
        H_e = np.zeros(len(H_corr))
        signdH = np.zeros(len(H_corr))
        M_calc[0] = M_corr[0]
        M_irr[0] = M_corr[0]

        for i in range(1,int(self.sampleFrequency/self.frequency)):
            signdH[i] = np.sign(dH[i])
            if signdH[i] == 0:
                signdH[i] = signdH[i-1]
            H_e[i] = H_corr[i] + alpha*M_calc[i-1]
            M_an[i] = Ms*(np.tanh(H_e[i]/a)**(-1) - a/H_e[i])

            dMirr_dH = (M_an[i]-M_irr[i-1])/(k*signdH[i]-alpha*(M_an[i]-M_irr[i-1]))
            M_irr[i] = M_irr[i-1] +  dMirr_dH*dH[i]

            M_calc[i] = (1-c)*M_irr[i] + c*M_an[i]
        return M_calc

    #% J-A Model
    def JA_M_calc(self, params,H_corr):
        [a,alpha,Ms,k,c] = params
        dH = np.roll(H_corr,-1) - H_corr 

        M_an = np.zeros(len(H_corr))
        M_irr = np.zeros(len(H_corr))
        M_calc = np.zeros(len(H_corr))
        H_e = np.zeros(len(H_corr))
        signdH = np.zeros(len(H_corr))

        for i in range(len(self.zeroSteps+self.upSteps),self.wavepoints-1):
            signdH[i] = np.sign(dH[i])
            if signdH[i] == 0:
                signdH[i] = signdH[i-1]
            H_e[i] = H_corr[i] + alpha*M_calc[i-1]
            M_an[i] = Ms*(np.tanh(H_e[i]/a)**(-1) - a/H_e[i])

            dMirr_dH = (M_an[i]-M_irr[i-1])/(k*signdH[i]-alpha*(M_an[i]-M_irr[i-1]))
            M_irr[i] = M_irr[i-1] +  dMirr_dH*dH[i]

            M_calc[i] = (1-c)*M_irr[i] + c*M_an[i]
        return M_calc

    #% inverse J-A Modell
    def JA_H_calc(self, params,B_ref):
        [a,alpha,Ms,k,c] = params
        mu_0 = 4*np.pi*10**(-7)
        dB_ref = (np.roll(B_ref,-1) - B_ref) 

        M_an = np.zeros(len(B_ref))
        M_irr = np.zeros(len(B_ref))
        M_calc = np.zeros(len(B_ref))
        H_e = np.zeros(len(B_ref))
        H_calc = np.zeros(len(B_ref))
        signdB_ref = np.zeros(len(B_ref))
        signdB_ref[len(self.zeroSteps)-1] = np.sign(dB_ref[len(self.zeroSteps)-1])

        H_calc[len(self.zeroSteps)-1] = 1*10**(-4)

        for i in range(len(self.zeroSteps),self.wavepoints-len(self.zeroSteps)-1):
            signdB_ref[i-1] = np.sign(dB_ref[i-1])
            if signdB_ref[i-1] == 0:
                signdB_ref[i-1] = signdB_ref[i-2]

            H_e[i-1] = H_calc[i-1] + alpha*M_calc[i-1]
            M_an[i-1] = Ms*(np.tanh(H_e[i-1]/a)**(-1) - a/(H_e[i-1]))

            dMan_dHe = (Ms/a)*(1 - np.tanh(H_e[i-1]/a)**(-2) + (a/H_e[i-1])**2) 
            M_irr[i-1] = (M_calc[i-1] - c*M_an[i-1])/(1-c)
            dMirr_dBe = (M_an[i-1] - M_irr[i-1])/(mu_0*k*signdB_ref[i-1])

            dM_dB = ((1-c)*dMirr_dBe + (c/mu_0)*dMan_dHe)/(1 + mu_0*(1-c)*(1-alpha)*dMirr_dBe + c*(1-alpha)*dMan_dHe)

            M_calc[i] = M_calc[i-1] + dM_dB*dB_ref[i-1]
            H_calc[i] = B_ref[i]/mu_0 - M_calc[i]

        return H_calc

    # objective function
    def objective_function(self, params,H_corr,M_corr):
        M_calc = self.JA_M_calc_params(params,H_corr)
        Q = np.sqrt(np.sum((M_corr-M_calc)**2)/len(M_corr))
        return Q

    # constraints for the parameters
    def constraint_a(self, params):
        a,alpha,Ms,k,c,xc,x_in,Hc = params
        return a - (Ms/3)*(1/xc + alpha)
    def constraint_c(self, params):
        a,alpha,Ms,k,c,xc,x_in,Hc = params
        return c - (3*a*x_in)/Ms
    def constraint_k(self, params):
        a,alpha,Ms,k,c,xc,x_in,Hc = params
        return k - Hc/(1-(alpha*Ms/(3*a)))

    def getH_corr(self, I_temp):
        H_corr = PXIPostProcessing.calc_average(I_temp,self.sampleFrequency,self.frequency,1)*self.H_turns/self.l_eff
        return H_corr
    
    def getI_calc(self, H_corr):
        i_calc = H_corr*(self.l_eff/self.H_turns)
        return i_calc
    
    def getR(self, U_temp, I_temp):
        R = max(U_temp)/max(I_temp)
        return(R)
    
    def getI_corr(self, U2_temp):
        I_corr = PXIPostProcessing.calc_BCoil(U2_temp,self.sampleFrequency,self.frequency,self.n_mean,self.mainSteps,1,self.B_turns,self.B_area)
        I_corr = np.concatenate([I_corr, [I_corr[len(I_corr)-1]]])
        return I_corr
    
    def getMU_0(self):
        mu_0 = 4*np.pi*10**(-7)
        return mu_0
    
    def getM_corr(self, U2_temp):
        Mcorr = self.getI_corr(U2_temp)/self.getMU_0()
        return Mcorr
    
    def getB_corr(self, U_temp, I_temp):
        B_corr = self.getMU_0()*(self.getH_corr(I_temp) + self.getM_corr(U_temp))
        return B_corr
    
    def getB_ref(self, B_corr):
        

        B_peak = max(B_corr)
        B_peak = 0.95*max(B_corr)
        
        mainSignal_B_ref = np.sin(2*np.pi*self.frequency*self.mainSteps)*B_peak
        upSignal_B_ref = np.concatenate((np.sin(2*np.pi*self.frequency*self.zeroSteps)*0.001, self.upSteps/max(self.upSteps)*np.sin(2*np.pi*self.frequency*self.upSteps)))*B_peak
        downSignal_B_ref = np.concatenate((np.sin(2*np.pi*self.frequency*self.downSteps)*np.flip(self.downSteps)/max(self.downSteps), np.sin(2*np.pi*self.frequency*self.zeroSteps)*0.001))*B_peak

        B_ref = np.concatenate((upSignal_B_ref, mainSignal_B_ref, downSignal_B_ref))

        return B_ref
    
    def getDB_ref(self, B_ref):
        dB_ref = np.gradient(B_ref)
        return dB_ref
    
    def getU2_ref(self, db_ref):
        U2_ref = (self.B_turns*self.B_area*self.sampleFrequency)*db_ref
        return U2_ref
    
    def getI_calc(self, H_corr):    
        i_calc = H_corr*(self.l_eff/self.H_turns)
        return i_calc
    
    def getUAC(self, U2_ref, i_ref, R):

        U_AC = U2_ref+ R*i_ref
        U_AC[len(self.zeroSteps):len(self.zeroSteps)+len(self.upSteps)] = U_AC[len(self.zeroSteps):len(self.zeroSteps)+len(self.upSteps)]*self.upSteps/max(self.upSteps)
        U_AC[-len(self.zeroSteps)-len(self.downSteps)+1:-len(self.zeroSteps)+1] = U_AC[-len(self.zeroSteps)-len(self.downSteps):-len(self.zeroSteps)]*np.flip(self.downSteps)/max(self.downSteps)

        return U_AC

    def getI_ref(self, params, B_ref):
        H_calc = self.JA_H_calc(params,B_ref)

        i_ref = H_calc*(self.l_eff/self.H_turns)
        return i_ref
    
    def evaluateResults(self, B_ref, B_corr, U2_ref, U2_temp, i_ref, i_calc):
        plt.figure()
        plt.plot(B_ref[5000:6000],label="B_ref")
        plt.plot(B_corr,label="B_meas")
        plt.legend()
        plt.ylabel('B in Tesla')
        plt.xlabel('samples')
        plt.grid("on")

        plt.figure()
        plt.plot(U2_ref[5000:6000],label="U2_ref")
        plt.plot(U2_temp[1000:2000],label="U2_meas")
        plt.legend()
        plt.ylabel('U2 inV')
        plt.xlabel('samples')
        plt.grid("on")

        plt.figure()
        plt.plot(i_ref[5000:6000],label="i_ref")
        plt.plot(i_calc,label="i_meas")
        plt.legend()
        plt.ylabel('I_prim in A')
        plt.xlabel('samples')
        plt.grid("on")



    def checkI_ref(self, i_ref):
        
        

        i_max = 28*np.ones(len(i_ref))

        plt.figure()
        plt.plot(i_ref,label="i_ref from J-A Model")
        plt.plot(i_max,'r',label="max current I_prim from Rohrer-Amplifier")
        plt.legend()
        plt.ylabel('i in A')
        plt.xlabel('samples')
        plt.grid("on")

        # if i_ref is bigger then Rohrer i_max (30A --> 28A was choosen)
        if max(i_ref) > max(i_max):
            sys.exit("calculated value of I_prim is to high --> reduce B_peak")


    def createParams(self, M_corr, H_corr):

        # 1. calc Ms
        Ms = max(M_corr)

        # 2. calc alpha
        zero_crossings_M = np.where(np.diff(np.sign(M_corr)))[0]
        zero_crossings_H = np.where(np.diff(np.sign(H_corr)))[0]

        Hc = np.mean([abs(H_corr[zero_crossings_M[0]+1]),abs(H_corr[zero_crossings_M[1]]+1)])
        Mr = np.mean([abs(M_corr[zero_crossings_H[0]+1]),abs(M_corr[zero_crossings_H[1]]+1)])
        alpha = Hc/Mr

        # 3. cacl a
        dMc = M_corr[zero_crossings_M[0]+1] - M_corr[zero_crossings_M[0]]
        dHc = H_corr[zero_crossings_M[0]+1] - H_corr[zero_crossings_M[0]]
        xc = dMc/dHc

        a = Ms/3*(1/xc +alpha)

        # 4. calc c
        dM0 = np.mean(abs(M_corr[1]-M_corr[0]))
        dH0 = np.mean(abs(H_corr[1]-H_corr[0]))
        x_in = abs(dM0/dH0)

        c = (3*a*x_in)/Ms

        # 5. calc k
        k = Hc

        return [a,alpha,Ms,k,c,xc,x_in,Hc]
    
    def checkJAModel(self, params, H_corr, B_corr):
        
        mu_0 = self.getMU_0()

        
        M_calc = self.JA_M_calc_params(params,H_corr)

        B_calc = mu_0*(H_corr + M_calc)

        plt.figure()
        plt.plot(H_corr,B_corr, label ="measured")
        plt.plot(H_corr,B_calc, label ="calculated with J-A")
        plt.legend()
        plt.ylabel('B in Tesla')
        plt.xlabel('H in A/m')
        plt.grid("on")

    def optimizeParams(self, max_iterations, params, M_corr, H_corr):
        options_set = {'maxiter':max_iterations}
        constraints = [{'type':'eq','fun':self.constraint_a},
                       {'type':'eq','fun':self.constraint_c}]
                       #{'type':'eq','fun':constraint_k}]

        opt_params = scipy.optimize.minimize(self.objective_function, params, args=(H_corr,M_corr),constraints=constraints,options=options_set)

        return opt_params
    
    
        
