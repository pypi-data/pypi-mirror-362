import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate
import scipy.optimize
import sys

from . import StoreSetup
from . import PXIPostProcessing

MU_0 = 4+np.pi+1e-7

class MatModel:
    def __init__(self, storeSetup:StoreSetup):
        # Store Setup
        self.ss = storeSetup
        self.sampleFrequency = storeSetup.readInfoValue['sampleFrequency']
        self.frequency = storeSetup.readInfoValue['frequency']
        self.wavepoints = storeSetup.readInfoValue['wavepoints']
        self.n_mean = storeSetup.readInfoValue['n_mean']
        self.mainSteps = storeSetup.readInfoValue['lenMainSignalDMM']
        self.upSteps = storeSetup.readInfoValue['lenUpSignalDMM']
        self.downSteps = storeSetup.readInfoValue['lenDownSignalDMM']
        self.zeroSteps = storeSetup.readInfoValue['lenZeroSignalDMM']
        self.B_turns = storeSetup.readInfoValue['B_turns']
        self.B_area = storeSetup.readInfoValue['B_area']
        self.H_turns = storeSetup.readInfoValue['H_turns']
        self.l_eff = storeSetup.readInfoValue['l_eff']
        self.Rohrer_voltage_factor = storeSetup.readInfoValue['Rohrer_voltage_factor']
        self.Rohrer_current_factor= storeSetup.readInfoValue['Rohrer_current_factor']
        # Variable
        self.U1_temp = None   # Real Exciation Voltage form Rohrer
        self.I1_temp = None   # Real Exciation Current form Rohrer
        self.H_corr = None    # H field due to excitation coil
        self.R = None         # Resistance of Measurement Setup
        self.U2_temp = None   # Induced Voltage secondary side
        self.J_corr = None    # Polarization
        self.M_corr = None    # Magnetization
        self.B_corr = None    # magnetic Flux density
        self.init_params = None   # Initial Parameter of JA Model
        self.opt_params = None    # Optimized Parameter of JA Model
        self.M_calc = None    # Compute Magnetization
        self.B_ref = None     # Reference magnetic flux density
        self.dB_ref = None    # Derivitave of B_ref


    def JAModelCalcM(self,params,H_corr):
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

    #% J-A Model different approach
    def __JAModelCalcM(self, params,H_corr):
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
    def JAModelCalcH(self,params,B_ref):
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
    def __objectiveFunction(self, params,H_corr,M_corr):
        M_calc = self.JA_M_calc_params(params,H_corr)
        Q = np.sqrt(np.sum((M_corr-M_calc)**2)/len(M_corr))
        return Q

    # constraints for the parameters
    def __constraint_a(self, params):
        a,alpha,Ms,k,c,xc,x_in,Hc = params
        return a - (Ms/3)*(1/xc + alpha)
    def __constraint_c(self, params):
        a,alpha,Ms,k,c,xc,x_in,Hc = params
        return c - (3*a*x_in)/Ms
    def __constraint_k(self, params):
        a,alpha,Ms,k,c,xc,x_in,Hc = params
        return k - Hc/(1-(alpha*Ms/(3*a)))
    
    def computeVariablesFromMeasurements(self):
        self.U1_temp = self.ss.readData(0,"U")[self.upSteps:-self.downSteps]*self.Rohrer_voltage_factor
        self.I1_temp = self.ss.readData(0,"I")[self.upSteps:-self.downSteps]*self.Rohrer_current_factor
        self.H_corr = PXIPostProcessing.calc_average(self.I1_temp,self.sampleFrequency,self.frequency,1)*self.H_turns/self.l_eff
        self.R = max(self.U1_temp)/max(self.I1_temp)
        self.U2_temp = self.ss.readData(0,"U2")[self.upSteps:-self.downSteps]
        J_corr = PXIPostProcessing.calc_BCoil(self.U2_temp,self.sampleFrequency,self.frequency,self.n_mean,self.mainSteps,1,self.B_turns,self.B_area)
        self.J_corr = np.concatenate([J_corr, [J_corr[len(J_corr)-1]]])
        self.M_corr = self.J_corr/MU_0
        self.B_corr = MU_0*(self.H_corr + self.M_corr)

    def createInitJAModelParams(self):
        M_corr = self.M_corr
        H_corr = self.H_corr

        # 1. calc Ms
        Ms = max(self.M_corr)

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
        self.init_params = [a,alpha,Ms,k,c,xc,x_in,Hc]

    def checkJAModel(self,params):        
        M_calc = self.JAModelCalcM(params,self.H_corr)
        B_calc = MU_0*(self.H_corr + M_calc)

        plt.figure()
        plt.plot(self.H_corr,self.B_corr, label ="measured")
        plt.plot(self.H_corr,B_calc, label ="calculated with J-A")
        plt.legend()
        plt.ylabel('B in Tesla')
        plt.xlabel('H in A/m')
        plt.grid("on")

    def optimizeParams(self, max_iterations, params, M_corr, H_corr):
        options_set = {'maxiter':max_iterations}
        constraints = [{'type':'eq','fun':self.__constraint_a},
                       {'type':'eq','fun':self.__constraint_c}]
                       #{'type':'eq','fun':constraint_k}]
        opt_params = scipy.optimize.minimize(self.__objectiveFunction,params,args=(H_corr,M_corr),constraints=constraints,options=options_set)
        self.opt_params = list(opt_params.x)
        return opt_params

    def createInitSignal(self,params,B_ref):
        self.B_ref = B_ref
        dB_ref = np.gradient(B_ref)

        H_calc = self.JAModelCalcH(params,B_ref)
        I_ref = H_calc*(self.l_eff/self.H_turns)
        self.__checkCurrentInLimit(I_ref)    

        U2_ref = self.B_turns*self.B_area*self.sampleFrequency*dB_ref
        U_out = U2_ref + self.R*I_ref
        self.__checkVoltageInLimit(U_out)

        mainSignal = [U_out[self.upSteps:-self.downSteps]/(self.Rohrer_voltage_factor)]
        upSignal = [U_out[:self.upSteps]/(self.Rohrer_voltage_factor)]
        downSignal = [U_out[-self.downSteps:]/(self.Rohrer_voltage_factor)]

        return upSignal,mainSignal,downSignal

    def __checkCurrentInLimit(self,I_ref):
        I_temp = I_ref/self.Rohrer_current_factor
        I_max = 4*np.ones(I_temp.shape)
        if max(I_temp) > max(I_max):
          sys.exit("calculated value of I is to high --> reduce B")

    def __checkVoltageInLimit(self,U_ref):
        U_temp = U_ref/self.Rohrer_voltage_factor
        U_max = 4*np.ones(U_temp.shape)
        if max(U_temp) > max(U_max):
          sys.exit("calculated value of U is to high --> reduce B")

    
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
