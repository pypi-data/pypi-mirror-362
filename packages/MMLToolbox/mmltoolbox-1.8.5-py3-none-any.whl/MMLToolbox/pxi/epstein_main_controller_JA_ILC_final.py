#%% Information
# Author: Franz Maier adapted from Andreas Gschwandter "epstein_main"
# Date: 01.10.2024
# Description: Template to control the magnetic field in Epstein-Frame-Measurement

#%% Import
import warnings
import numpy as np
import matplotlib.pyplot as plt
import time
import sys
import scipy.integrate
import scipy.optimize

from PyMeas import StoreSetup, PostProcessing

from PXITool import  PreProcessing, PXIControl, StoreSetup
warnings.simplefilter("ignore", UserWarning)

#% J-A Model for parameteridentification
def JA_M_calc_params(params,H_corr):
    [a,alpha,Ms,k,c] = params
    dH = np.roll(H_corr,-1) - H_corr

    M_an = np.zeros(len(H_corr))
    M_irr = np.zeros(len(H_corr))
    M_calc = np.zeros(len(H_corr))
    H_e = np.zeros(len(H_corr))
    signdH = np.zeros(len(H_corr))
    M_calc[0] = M_corr[0]
    M_irr[0] = M_corr[0]

    for i in range(1,int(sampleFrequency/frequency)):
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
def JA_M_calc(params,H_corr):
    [a,alpha,Ms,k,c] = params
    dH = np.roll(H_corr,-1) - H_corr 

    M_an = np.zeros(len(H_corr))
    M_irr = np.zeros(len(H_corr))
    M_calc = np.zeros(len(H_corr))
    H_e = np.zeros(len(H_corr))
    signdH = np.zeros(len(H_corr))

    for i in range(len(zeroSteps+upSteps),wavepoints-1):
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
def JA_H_calc(params,B_ref):
    [a,alpha,Ms,k,c] = params
    mu_0 = 4*np.pi*10**(-7)
    dB_ref = (np.roll(B_ref,-1) - B_ref) 

    M_an = np.zeros(len(B_ref))
    M_irr = np.zeros(len(B_ref))
    M_calc = np.zeros(len(B_ref))
    H_e = np.zeros(len(B_ref))
    H_calc = np.zeros(len(B_ref))
    signdB_ref = np.zeros(len(B_ref))
    signdB_ref[len(zeroSteps)-1] = np.sign(dB_ref[len(zeroSteps)-1])

    H_calc[len(zeroSteps)-1] = 1*10**(-4)

    for i in range(len(zeroSteps),wavepoints-len(zeroSteps)-1):
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
def objective_function(params,H_corr,M_corr):
    M_calc = JA_M_calc_params(params,H_corr)
    Q = np.sqrt(np.sum((M_corr-M_calc)**2)/len(M_corr))
    return Q

# constraints for the parameters
def constraint_a(params):
    a,alpha,Ms,k,c = params
    return a - (Ms/3)*(1/xc + alpha)
def constraint_c(params):
    a,alpha,Ms,k,c = params
    return c - (3*a*x_in)/Ms
def constraint_k(params):
    a,alpha,Ms,k,c = params
    return k - Hc/(1-(alpha*Ms/(3*a)))


#%% Configuration
# Info
fileName = "M1" #Same as in Material Library
description = "Measurement with Epstein in uniaxial direction" #Addional information

# Sample Info in SI
############## Change by User ##############
sample_thickness = 0.3e-3 
sample_width = 30e-3
sample_number = 20
############################################

info_dict_sample = {"sample_thikness": (sample_thickness, "m"), 
                    "sample_width": (sample_width, "m"),
                    "sample_number": (sample_number, "-")}

# Measurement Info in SI
############## Defined by Measurement Device --> Don't change!! ##############
B_turns = 700
B_area = sample_thickness*sample_width*sample_number

H_turns = 700
l_eff = 0.94

Rohrer_voltage_factor = 100 #V/V
Rohrer_current_factor = 10 #A/V
############################################

info_dict_meas = {"B_turns": (B_turns, "-"),
                  "B_area": (B_area, "m^2"),
                  "H_turns": (H_turns, "-"),
                  "l_eff": (l_eff, "m"),
                  "Rohrer_voltage_factor": (Rohrer_voltage_factor, "V/V"),
                  "Rohrer_current_factor": (Rohrer_current_factor, "A/V")}

# Signal in SI
################################
peakIBoundaryU = 2.5 #max excitation to cover whole Hysteresis-curve
peakIBoundaryL = False 
frequency = 100

numPeriods = 3
sampleFrequency = frequency*1000 #max 1.8MHz!! DMM
zeroPeriod = 2
up_down_Periods = 2
daqFreqFactor = 1

############################################
if hasattr(peakIBoundaryU, "__len__") and len(peakIBoundaryU)>0: numIntervalls=len(peakIBoundaryU) 
else: numIntervalls=1
############################################

info_dict_signal = {# "peakExcitationUpper": (peakIBoundaryU, "V"),
                    # "peakExcitationLower": (peakIBoundaryL, "V"),
                    "frequency": (frequency, "Hz"),
                    "numPeriods": (numPeriods, "-"),
                    "sampleFrequency": (sampleFrequency, "Hz"),
                    "numIntervalls": (numIntervalls, "-"),
                    "daqFreqFactor":(daqFreqFactor, "-")}


#%% Define Output Signal
mainSteps = np.arange(0,numPeriods/frequency,1/sampleFrequency)
upSteps = np.arange(0,up_down_Periods/frequency,1/sampleFrequency)
downSteps = np.arange(0,up_down_Periods/frequency,1/sampleFrequency)
zeroSteps = np.arange(0,zeroPeriod/frequency,1/sampleFrequency)

#%% Demagnetize
all_steps = np.arange(0,(zeroPeriod+up_down_Periods+numPeriods+up_down_Periods+zeroPeriod)/frequency,1/sampleFrequency)
signal_demag = np.flip(all_steps)/max(all_steps)*np.sin(2*np.pi*frequency*all_steps)
upSignal_x = signal_demag[0:len(zeroSteps)+len(upSteps)]
mainSignal_x = signal_demag[len(zeroSteps)+len(upSteps):len(zeroSteps)+len(upSteps)+len(mainSteps)]
downSignal_x = signal_demag[len(zeroSteps)+len(upSteps)+len(mainSteps):]

mainSignal = [mainSignal_x]
upSignal = [upSignal_x]
downSignal = [downSignal_x]

U_in = np.concatenate([upSignal_x,mainSignal_x,downSignal_x])*peakIBoundaryU*Rohrer_voltage_factor

n_mean = 5
wavepoints = len(mainSignal_x)+len(upSignal_x)+len(downSignal_x)
t = np.arange(0,wavepoints/sampleFrequency,(wavepoints/sampleFrequency)/wavepoints)

# Use when one signals x-direction
NIOutput = {"outx": {"slotName":"PXI1Slot14","channel": "ao0","minVal":-5,"maxVal":5, "rate":sampleFrequency,"digitalSignal":False,"switchTrigger":True}}

# Input DMM, B- and H-Coil for both direction
NIDMM = {"U": {"slotName": "PXI1Slot16","range": 5,"sampleFreq": sampleFrequency, "wavepoints":wavepoints},
         "I": {"slotName": "PXI1Slot15","range": 5,"sampleFreq": sampleFrequency, "wavepoints":wavepoints},
         "U2": {"slotName": "PXI1Slot17","range": 500,"sampleFreq": sampleFrequency, "wavepoints":wavepoints},}

###################### No further adaption by user necessary ###################### 
# Define Class
infoDict = {"description": (description,"-"), 
            **info_dict_sample,
            **info_dict_meas,
            **info_dict_signal, 
            "niOutput":NIOutput, 
            "niDMM":NIDMM,
            "lenUpSignalDMM": (len(upSignal_x), "-"),
            "lenMainSignalDMM": (len(mainSignal_x), "-"),
            "lenDownSignalDMM": (len(downSignal_x), "-"),
            "tDMM": (mainSteps, "s")}

ppTool = PreProcessing.PreProcessing_re(peakIBoundaryU,
                                        peakIBoundaryL,
                                        frequency,
                                        numPeriods,
                                        sampleFrequency,
                                        numIntervalls,
                                        mainSignal,
                                        upSignal,
                                        downSignal)
       
ss = StoreSetup.StoreSetup(fileName)
ss.createFile()
ss.writeInfo(infoDict)
pxiHandler = PXIControl.PXIControl()

# To Measurement
allMeasurments = []
allSignals = []

for i in range(1):
    pxiHandler.connectHardware(dmmDict=NIDMM,analogOutDict=NIOutput,switchSlotName="PXI1Slot13")
    allSignals = []
    outputSignal = ppTool.getOutputSignal(i)# outpusignal = new calculated outputsignal
    ######################################################
    # Use when one signals x-direction
    allSignals = np.asarray(outputSignal[0])
    ss.writeOutputSignal(i,"outx",outputSignal[0])
    ######################################################

    #pxiHandler.startAnalogOutputTask(allSignals)
    pxiHandler.triggerDevices(allSignals)
    dmm_results = pxiHandler.getMeasResults()#Messergebnisse der DMMS 2D array 
    #daq_results = pxiHandler.analogInResults
    pxiHandler.closeAnalogOutputTask()
    #pxiHandler.closeAnalogInputTask()
    ss.writeData(i,NIDMM.keys(),dmm_results)
    time.sleep(1)

# evaluate demagnetization:  
# U2_temp = ss.readData(0,"U2")
# I_temp = ss.readData(0,"I")
# I_corr = PostProcessing.calc_BCoil(U2_temp,wavepoints-1,1,n_mean,t,1,B_turns,B_area)
# I_corr =np.concatenate((I_corr, [I_corr[len(I_corr)-1]], [I_corr[len(I_corr)-1]]))
# H_corr = I_temp*H_turns/l_eff
# mu_0 = 4*np.pi*10**(-7)
# M_corr = I_corr/mu_0
# plt.figure()
# plt.plot(H_corr,M_corr)
# plt.grid("on")


# Demag Ende

#%% new Input Signal
# Start Model fitting
mainSignal_x = np.sin(2*np.pi*frequency*mainSteps)
upSignal_x = np.concatenate((np.sin(2*np.pi*frequency*zeroSteps)*0, upSteps/max(upSteps)*np.sin(2*np.pi*frequency*upSteps)))
downSignal_x = np.concatenate((np.flip(downSteps)/max(downSteps)*np.sin(2*np.pi*frequency*downSteps), np.sin(2*np.pi*frequency*zeroSteps)*0))

######################################################
# Use when one signal x-direction
mainSignal = [mainSignal_x]
upSignal = [upSignal_x]
downSignal = [downSignal_x]
######################################################

wavepoints = len(mainSignal_x)+len(upSignal_x)+len(downSignal_x)
t = np.arange(0,wavepoints/sampleFrequency,(wavepoints/sampleFrequency)/wavepoints)
U_in = np.concatenate([upSignal_x,mainSignal_x,downSignal_x])*peakIBoundaryU*Rohrer_voltage_factor

#%% Define PXI-Configuration
# Output Signal DAQ-Card
######################################################

# Use when one signals x-direction
NIOutput = {"outx": {"slotName":"PXI1Slot14","channel": "ao0","minVal":-5,"maxVal":5, "rate":sampleFrequency,"digitalSignal":False,"switchTrigger":True}}

# Input DMM, B- and H-Coil for both direction
NIDMM = {"U": {"slotName": "PXI1Slot16","range": 5,"sampleFreq": sampleFrequency, "wavepoints":wavepoints},
         "I": {"slotName": "PXI1Slot15","range": 5,"sampleFreq": sampleFrequency, "wavepoints":wavepoints},
         "U2": {"slotName": "PXI1Slot17","range": 500,"sampleFreq": sampleFrequency, "wavepoints":wavepoints},}

###################### No further adaption by user necessary ###################### 
#%% Define Class
infoDict = {"description": (description,"-"), 
            **info_dict_sample,
            **info_dict_meas,
            **info_dict_signal, 
            "niOutput":NIOutput, 
            "niDMM":NIDMM,
            "lenUpSignalDMM": (len(upSignal_x), "-"),
            "lenMainSignalDMM": (len(mainSignal_x), "-"),
            "lenDownSignalDMM": (len(downSignal_x), "-"),
            "tDMM": (mainSteps, "s")}

ppTool = PreProcessing.PreProcessing_re(peakIBoundaryU,
                                        peakIBoundaryL,
                                        frequency,
                                        numPeriods,
                                        sampleFrequency,
                                        numIntervalls,
                                        mainSignal,
                                        upSignal,
                                        downSignal)
       
ss = StoreSetup.StoreSetup(fileName)
ss.createFile()
ss.writeInfo(infoDict)
pxiHandler = PXIControl.PXIControl()

#%% To Measurement
allMeasurments = []
allSignals = []

for i in range(1):
    pxiHandler.connectHardware(dmmDict=NIDMM,analogOutDict=NIOutput,switchSlotName="PXI1Slot13")
    allSignals = []
    outputSignal = ppTool.getOutputSignal(i)# outpusignal = new calculated outputsignal
    ######################################################
    # Use when one signals x-direction
    allSignals = np.asarray(outputSignal[0])
    ss.writeOutputSignal(i,"outx",outputSignal[0])
    ######################################################

    #pxiHandler.startAnalogOutputTask(allSignals)
    pxiHandler.triggerDevices(allSignals)
    dmm_results = pxiHandler.getMeasResults()#Messergebnisse der DMMS 2D array 
    #daq_results = pxiHandler.analogInResults
    pxiHandler.closeAnalogOutputTask()
    #pxiHandler.closeAnalogInputTask()
    ss.writeData(i,NIDMM.keys(),dmm_results)
    time.sleep(1)



#%%##############################################################################################
########################### Feed-Forward-Controller Epstein #####################################
#################################################################################################
# all calculations are based on measurements with compensation coil

U_temp = ss.readData(0,"U")[len(upSignal_x):-len(downSignal_x)]*Rohrer_voltage_factor

# calculate H
I_temp = ss.readData(0,"I")[len(upSignal_x):-len(downSignal_x)]*Rohrer_current_factor
H_corr = PostProcessing.calc_average(I_temp,sampleFrequency,frequency,1)*H_turns/l_eff

# calculate primary resistance
R = max(U_temp)/max(I_temp)

# calculate I 
U2_temp = ss.readData(0,"U2")[len(upSignal_x):-len(downSignal_x)]
U2_temp = U2_temp - np.mean(U2_temp)
I_corr = PostProcessing.calc_BCoil(U2_temp,sampleFrequency,frequency,n_mean,mainSteps,1,B_turns,B_area)
I_corr = np.concatenate([I_corr, [I_corr[len(I_corr)-1]]])

mu_0 = 4*np.pi*10**(-7)
M_corr = I_corr/mu_0
B_corr = mu_0*(H_corr + M_corr)

#%%##############################################################################################
# J-A Model Parameters
#################################################################################################

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
#################################################################################################
# J-A model check
#################################################################################################

initial_params = [a,alpha,Ms,k,c]
M_calc = JA_M_calc_params(initial_params,H_corr)

B_calc = mu_0*(H_corr + M_calc)

plt.figure()
plt.plot(H_corr,B_corr, label ="measured")
plt.plot(H_corr,B_calc, label ="calculated with J-A")
plt.legend()
plt.ylabel('B in Tesla')
plt.xlabel('H in A/m')
plt.grid("on")


#%%##############################################################################################
# optimization of Parameters
#################################################################################################

options_set = {'maxiter':250}
constraints = [{'type':'eq','fun':constraint_a},
               {'type':'eq','fun':constraint_c}]
               #{'type':'eq','fun':constraint_k}]

opt_params = scipy.optimize.minimize(objective_function, initial_params, args=(H_corr,M_corr),constraints=constraints,options=options_set)
#%%##############################################################################################
# check results
#################################################################################################

params = opt_params.x
[a,alpha,Ms,k,c] = params
params = [a,alpha,Ms,k,c] #to retain correct datatype

#% evaluation of optimization
M_calc = JA_M_calc_params(params,H_corr)
B_calc = mu_0*(H_corr + M_calc)

plt.figure()
plt.plot(H_corr,B_corr, label ="measured")
plt.plot(H_corr,B_calc, label ="calculated with J-A")
plt.legend()
plt.ylabel('B in Tesla')
plt.xlabel('H in A/m')
plt.grid("on")


#%%##############################################################################################
#################################################################################################
# calculation of B_ref
# when JA is optimized, just change the B_peak values and proceed from here
#################################################################################################
#################################################################################################

B_peak = max(B_corr)
B_peak = 0.95*max(B_corr)
#B_peak = 0.75*max(B_corr)
#B_peak = 0.1*max(B_corr)

mainSignal_B_ref = np.sin(2*np.pi*frequency*mainSteps)*B_peak
upSignal_B_ref = np.concatenate((np.sin(2*np.pi*frequency*zeroSteps)*0.001, upSteps/max(upSteps)*np.sin(2*np.pi*frequency*upSteps)))*B_peak
downSignal_B_ref = np.concatenate((np.sin(2*np.pi*frequency*downSteps)*np.flip(downSteps)/max(downSteps), np.sin(2*np.pi*frequency*zeroSteps)*0.001))*B_peak

B_ref = np.concatenate((upSignal_B_ref, mainSignal_B_ref, downSignal_B_ref))
dB_ref = np.gradient(B_ref)

#################################################################################################
# #%% test other signal-form (300V/100Hz):
# Set number of iterations to 10! FF criteria does not work for other signals tha sin
# B_ref = np.concatenate((upSignal_B_ref, mainSignal_B_ref, downSignal_B_ref))
# B_peak = 0.2*max(B_corr)
# dB_ref_test = B_ref
# for i in range(len(B_ref)):
#     if B_ref[i] > 0:
#         dB_ref_test[i] = 1
#     else:
#         dB_ref_test[i] = -1

# dB_ref_test[0:len(zeroSteps)] = 0.001
# dB_ref_test[len(zeroSteps):len(zeroSteps)+len(upSteps)] = upSteps/max(upSteps)*dB_ref_test[len(zeroSteps):len(zeroSteps)+len(upSteps)]
# dB_ref_test[len(zeroSteps)+len(upSteps)+len(mainSteps):len(zeroSteps)+len(upSteps)+len(mainSteps)+len(downSteps)] = np.flip(downSteps)/max(downSteps)*dB_ref_test[len(zeroSteps)+len(upSteps)+len(mainSteps):len(zeroSteps)+len(upSteps)+len(mainSteps)+len(downSteps)]
# dB_ref_test[-len(zeroSteps):] = 0.001

# B_ref_test = scipy.integrate.cumtrapz(dB_ref_test)
# B_ref_test = np.concatenate([B_ref_test, [B_ref_test[len(B_ref_test)-1]]])
# B_ref_test = B_ref_test*(B_peak/max(B_ref_test))
# dB_ref_test = np.gradient(B_ref_test)

# B_ref = B_ref_test
# dB_ref = dB_ref_test
#################################################################################################

#%%##############################################################################################
# inverse J-A Modell to get i_ref
#################################################################################################
H_calc = JA_H_calc(params,B_ref)

i_ref = H_calc*(l_eff/H_turns)
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


#%%##############################################################################################
# calculation of U_AC 
#################################################################################################

U2_ref = (B_turns*B_area*sampleFrequency)*dB_ref

U_AC = U2_ref+ R*i_ref
U_AC[len(zeroSteps):len(zeroSteps)+len(upSteps)] = U_AC[len(zeroSteps):len(zeroSteps)+len(upSteps)]*upSteps/max(upSteps)
U_AC[-len(zeroSteps)-len(downSteps)+1:-len(zeroSteps)+1] = U_AC[-len(zeroSteps)-len(downSteps):-len(zeroSteps)]*np.flip(downSteps)/max(downSteps)

upSignal_x = U_AC[0:len(upSignal_x)]/(peakIBoundaryU*Rohrer_voltage_factor)
mainSignal_x = U_AC[len(upSignal_x):-len(downSignal_x)]/(peakIBoundaryU*Rohrer_voltage_factor)
downSignal_x =U_AC[-len(downSignal_x):]/(peakIBoundaryU*Rohrer_voltage_factor)

mainSignal = [mainSignal_x]
upSignal = [upSignal_x]
downSignal = [downSignal_x]

U_new = np.concatenate([upSignal_x,mainSignal_x,downSignal_x])*peakIBoundaryU*Rohrer_voltage_factor

plt.figure()
plt.plot(U_in[5000:6000],label="U_init")
plt.plot(U_new[5000:6000],label="U_JA")
plt.legend()
plt.ylabel('U_AC in V')
plt.xlabel('samples')
plt.grid("on")
#%% Define PXI-Configuration
# Output Signal DAQ-Card
######################################################

# Use when one signals x-direction
NIOutput = {"outx": {"slotName":"PXI1Slot14","channel": "ao0","minVal":-5,"maxVal":5, "rate":sampleFrequency,"digitalSignal":False,"switchTrigger":True}}

# Input DMM, B- and H-Coil for both direction
NIDMM = {"U": {"slotName": "PXI1Slot16","range": 5,"sampleFreq": sampleFrequency, "wavepoints":wavepoints},
         "I": {"slotName": "PXI1Slot15","range": 5,"sampleFreq": sampleFrequency, "wavepoints":wavepoints},
         "U2": {"slotName": "PXI1Slot17","range": 500,"sampleFreq": sampleFrequency, "wavepoints":wavepoints},}

###################### No further adaption by user necessary ###################### 
#%% Define Class
infoDict = {"description": (description,"-"), 
            **info_dict_sample,
            **info_dict_meas,
            **info_dict_signal, 
            "niOutput":NIOutput, 
            "niDMM":NIDMM,
            "lenUpSignalDMM": (len(upSignal_x), "-"),
            "lenMainSignalDMM": (len(mainSignal_x), "-"),
            "lenDownSignalDMM": (len(downSignal_x), "-"),
            #"phaseShift" : (phaseShift, "samples"),
            "tDMM": (mainSteps, "s")}

ppTool = PreProcessing.PreProcessing_re(peakIBoundaryU,
                                        peakIBoundaryL,
                                        frequency,
                                        numPeriods,
                                        sampleFrequency,
                                        numIntervalls,
                                        mainSignal,
                                        upSignal,
                                        downSignal)
       
ss = StoreSetup.StoreSetup(fileName)
ss.createFile()
ss.writeInfo(infoDict)
pxiHandler = PXIControl.PXIControl()

#%% To Measurement
allMeasurments = []
allSignals = []

for i in range(numIntervalls):
    pxiHandler.connectHardware(dmmDict=NIDMM,analogOutDict=NIOutput,switchSlotName="PXI1Slot13")
    allSignals = []
    outputSignal = ppTool.getOutputSignal(i)# outpusignal = new calculated outputsignal
    ######################################################
    # Use when one signals x-direction
    allSignals = np.asarray(outputSignal[0])
    ss.writeOutputSignal(i,"outx",outputSignal[0])
    ######################################################

    #pxiHandler.startAnalogOutputTask(allSignals)
    pxiHandler.triggerDevices(allSignals)
    dmm_results = pxiHandler.getMeasResults()#Messergebnisse der DMMS 2D array 
    #daq_results = pxiHandler.analogInResults
    pxiHandler.closeAnalogOutputTask()
    #pxiHandler.closeAnalogInputTask()
    ss.writeData(i,NIDMM.keys(),dmm_results)
    time.sleep(1)

#%% evaluation of Results
U2_temp = ss.readData(0,"U2")[len(upSignal_x):-len(downSignal_x)]
I_corr = PostProcessing.calc_BCoil(U2_temp,sampleFrequency,frequency,n_mean,mainSteps,1,B_turns,B_area)
I_corr = np.concatenate([I_corr, [I_corr[len(I_corr)-1]]])

I_temp = ss.readData(0,"I")[len(upSignal_x):-len(downSignal_x)]*Rohrer_current_factor
H_corr = PostProcessing.calc_average(I_temp,sampleFrequency,frequency,1)*H_turns/l_eff
i_calc = H_corr*(l_eff/H_turns)

M_corr = I_corr/mu_0
B_corr = mu_0*(H_corr + M_corr)
e_JA_B = B_corr - B_ref[5000:6000]
e_JA_U2 = U2_temp[1000:2000] - U2_ref[5000:6000]
RMS = np.sqrt(np.sum(e_JA_B**2)/len(e_JA_B))
tol_JA = max(B_ref)*0.02

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


#%%
B_eff = np.sqrt(1/len(B_corr)*np.sum(B_corr**2))
B_glr = 1/len(B_corr)*np.sum(abs(B_corr))
FF_B = B_eff/B_glr

print('FF_error = ' + str(abs(FF_B-1.111)) + ' (< 0.01111)')
print('RMS = ' + str(RMS) + ' (< ' + str(tol_JA) + ')')
if RMS < tol_JA and abs(FF_B-1.111) < 0.01111:
        sys.exit("criteria are met!")


# %% Hybrid ILC
U_peak = max(U_new)
k_sys_U = max(U2_temp)/U_peak
k_sys_B = max(B_corr)/U_peak

cutfrequency = 30 # when U2 becomes to noise --> switch to B-control

if frequency > cutfrequency:
    k_p = 0.25/(k_sys_U) #0.5 for 100Hz # 0.25 for 50Hz
else:
    k_p = 0.1/(k_sys_B) #0.3 before 0.25 works for 1Hz/ 0.4 for 10Hz

i_max = 28 #to protect Rohrer 
U_max = 480 #to protect Rohrer 

max_num_iterations = 50
numIterations = 0

S = np.zeros(max_num_iterations)
FF = np.zeros(max_num_iterations)

U_in_array = np.zeros((max_num_iterations+1,wavepoints))
U_in_array[0] = U_new

#%% ILC-Algorithm
for numIterations in range(0,max_num_iterations):
    #############################################
    # read & filter U2
    U2_temp_all = ss.readData(0,"U2")
    U2_temp = U2_temp_all[len(upSignal_x):-len(downSignal_x)]
    I_corr_all = PostProcessing.calc_BCoil(U2_temp_all,wavepoints-1,1,n_mean,t,1,B_turns,B_area)
    I_corr_all = np.concatenate((I_corr_all, [I_corr_all[len(I_corr_all)-1]], [I_corr_all[len(I_corr_all)-1]]))

    I_temp = ss.readData(0,"I")*Rohrer_current_factor
    H_corr_all = I_temp*H_turns/l_eff

    M_corr_all = I_corr_all/mu_0
    B_corr_all = mu_0*(H_corr_all + M_corr_all)

    B_corr = PostProcessing.calc_BCoil(U2_temp,sampleFrequency,frequency,n_mean,mainSteps,1,B_turns,B_area)
    B_corr =np.concatenate([B_corr, [B_corr[len(B_corr)-1]]])

    if max(abs(I_temp)) > i_max:
        i_max_plt = i_max*np.ones(len(I_temp))
        plt.figure()
        plt.plot(I_temp,label="i_calc from J-A Model")
        plt.plot(i_max_plt,'r',label="max current I_prim from Rohrer-Amplifier")
        plt.legend()
        plt.ylabel('i in A')
        plt.xlabel('samples')
        plt.grid("on")
        sys.exit("calculated value of I_prim is to high/desired B_peak not possible --> reduce B_peak")

    # calculate error
    amp_e_up = np.linspace(0,1,len(upSteps))
    amp_e_down = np.linspace(1,0,len(downSteps))

    if frequency > cutfrequency:
        e = U2_ref - U2_temp_all
        tol = max(U2_ref)*0.02
        FF_tol = 0.01111
    else:
        e = B_ref - B_corr_all
        tol = max(B_ref)*0.02
        FF_tol = 0.01111

    e[0:len(zeroSteps)] = 0 
    e[-len(zeroSteps):] = 0 
    e[len(zeroSteps):len(zeroSteps)+len(upSteps)] = amp_e_up*e[len(zeroSteps):len(zeroSteps)+len(upSteps)]
    e[-len(zeroSteps)-len(upSteps):-len(zeroSteps)] = amp_e_down*e[-len(zeroSteps)-len(upSteps):-len(zeroSteps)]

    # FF and RMS condition
    S[numIterations] = np.sqrt(np.sum(e[5000:6000]**2)/len(e[5000:6000]))

    U2_eff = np.sqrt(1/len(U2_temp)*np.sum(U2_temp**2))
    U2_glr = 1/len(U2_temp)*np.sum(abs(U2_temp))
    B_eff = np.sqrt(1/len(B_corr)*np.sum(B_corr**2))
    B_glr = 1/len(B_corr)*np.sum(abs(B_corr))

    if frequency > cutfrequency:
        FF[numIterations] = U2_eff/U2_glr
    else:
        FF[numIterations] = B_eff/B_glr

    if S[numIterations] < tol and abs(FF[numIterations]-1.111) < FF_tol:
        sys.exit("criteria are met!")
        break

    # Controller
    U_new = U_new + k_p*e

    #% Q-filter
    U_new_fft = np.fft.rfft(U_new)
    U_new_fft_abs = np.abs(U_new_fft)
    freq = np.fft.rfftfreq(wavepoints, d=1/sampleFrequency)

    U_new_fft_filter = U_new_fft.copy()
    U_new_fft_filter[freq > 10*frequency] = 0
    U_new_fft_filter_abs = np.abs(U_new_fft_filter)
    U_new_filtered = np.fft.irfft(U_new_fft_filter)

    if frequency > cutfrequency:
        upSignal_x = U_new[0:len(upSignal_x)]/(peakIBoundaryU*Rohrer_voltage_factor)
        mainSignal_x = U_new[len(upSignal_x):-len(downSignal_x)]/(peakIBoundaryU*Rohrer_voltage_factor)
        downSignal_x =U_new[-len(downSignal_x):]/(peakIBoundaryU*Rohrer_voltage_factor)
    else:
        upSignal_x = U_new_filtered[0:len(upSignal_x)]/(peakIBoundaryU*Rohrer_voltage_factor)
        mainSignal_x = U_new_filtered[len(upSignal_x):-len(downSignal_x)]/(peakIBoundaryU*Rohrer_voltage_factor)
        downSignal_x = U_new_filtered[-len(downSignal_x):]/(peakIBoundaryU*Rohrer_voltage_factor)


    mainSignal = [mainSignal_x]
    upSignal = [upSignal_x]
    downSignal = [downSignal_x]

    U_in_array[numIterations+1] = U_new_filtered

    #############################################
    #% Define PXI-Configuration
    # Output Signal DAQ-Card
    ######################################################

    # Use when one signals x-direction
    NIOutput = {"outx": {"slotName":"PXI1Slot14","channel": "ao0","minVal":-5,"maxVal":5, "rate":sampleFrequency,"digitalSignal":False,"switchTrigger":True}}

    # Input DMM, B- and H-Coil for both direction
    NIDMM = {"U": {"slotName": "PXI1Slot16","range": 5,"sampleFreq": sampleFrequency, "wavepoints":wavepoints},
            "I": {"slotName": "PXI1Slot15","range": 5,"sampleFreq": sampleFrequency, "wavepoints":wavepoints},
            "U2": {"slotName": "PXI1Slot17","range": 500,"sampleFreq": sampleFrequency, "wavepoints":wavepoints},}

    ###################### No further adaption by user necessary ###################### 
    #% Define Class
    infoDict = {"description": (description,"-"), 
                **info_dict_sample,
                **info_dict_meas,
                **info_dict_signal, 
                "niOutput":NIOutput, 
                "niDMM":NIDMM,
                "lenUpSignalDMM": (len(upSignal_x), "-"),
                "lenMainSignalDMM": (len(mainSignal_x), "-"),
                "lenDownSignalDMM": (len(downSignal_x), "-"),
                "tDMM": (mainSteps, "s")}

    ppTool = PreProcessing.PreProcessing_re(peakIBoundaryU,
                                            peakIBoundaryL,
                                            frequency,
                                            numPeriods,
                                            sampleFrequency,
                                            numIntervalls,
                                            mainSignal,
                                            upSignal,
                                            downSignal)
        
    ss = StoreSetup.StoreSetup(fileName)
    ss.createFile()
    ss.writeInfo(infoDict)
    pxiHandler = PXIControl.PXIControl()

    #% To Measurement
    allMeasurments = []
    allSignals = []

    for i in range(1):
        pxiHandler.connectHardware(dmmDict=NIDMM,analogOutDict=NIOutput,switchSlotName="PXI1Slot13")
        allSignals = []
        outputSignal = ppTool.getOutputSignal(i)# outpusignal = new calculated outputsignal
        ######################################################
        # Use when one signals x-direction
        allSignals = np.asarray(outputSignal[0])
        ss.writeOutputSignal(i,"outx",outputSignal[0])
        ######################################################

        #pxiHandler.startAnalogOutputTask(allSignals)
        pxiHandler.triggerDevices(allSignals)
        dmm_results = pxiHandler.getMeasResults()#Messergebnisse der DMMS 2D array 
        #daq_results = pxiHandler.analogInResults
        pxiHandler.closeAnalogOutputTask()
        #pxiHandler.closeAnalogInputTask()
        ss.writeData(i,NIDMM.keys(),dmm_results)
        time.sleep(1)



#%% evaluation of Results

print('numbers of iterations needed: ' + str(numIterations))
print('FF_error = ' + str(abs(FF[numIterations]-1.111)) + ' (< 0.01111)')
print('RMS = ' + str(S[numIterations]) + ' (< ' + str(tol) + ')')

# calculate M
U2_temp = ss.readData(0,"U2")[len(upSignal_x):-len(downSignal_x)]
I_corr = PostProcessing.calc_BCoil(U2_temp,sampleFrequency,frequency,n_mean,mainSteps,1,B_turns,B_area)
I_corr = np.concatenate([I_corr, [I_corr[len(I_corr)-1]]])

I_temp = ss.readData(0,"I")[len(upSignal_x):-len(downSignal_x)]*Rohrer_current_factor
H_corr = PostProcessing.calc_average(I_temp,sampleFrequency,frequency,1)*H_turns/l_eff
i_calc = H_corr*(l_eff/H_turns)

M_corr = I_corr/mu_0
B_corr = mu_0*(H_corr + M_corr)

plt.figure()
plt.plot(B_ref[5000:6000],label="B_ref")
plt.plot(B_corr,label="B_meas")
plt.legend()
plt.ylabel('B in Tesla')
plt.xlabel('samples')
plt.grid("on")

plt.figure()
plt.plot(U2_ref[5000:6000],label="U2_ref")
plt.plot(U2_temp[:1000],label="U2_meas")
plt.legend()
plt.ylabel('U2 inV')
plt.xlabel('samples')
plt.grid("on")

plt.figure()
plt.plot(U_in[5000:6000],label="U_init")
plt.plot(U_in_array[0][5000:6000],label="U_JA")
plt.plot(U_in_array[numIterations][5000:6000],label="U_P-ILC")
plt.legend()
plt.ylabel('U_prim in V')
plt.xlabel('samples')
plt.grid("on")


plt.figure()
plt.plot(i_ref[5000:6000],label="i_JA")
plt.plot(i_calc[:1000],label="i_P-ILC")
plt.legend()
plt.ylabel('I_prim in A')
plt.xlabel('samples')
plt.grid("on")

# U2_eff = np.sqrt(1/len(U2_temp[:1000])*np.sum(U2_temp[:1000]**2))
# U2_glr = 1/len(U2_temp[:1000])*np.sum(abs(U2_temp[:1000]))
# FF_U = U2_eff/U2_glr

# B_eff = np.sqrt(1/len(B_corr[:1000])*np.sum(B_corr[:1000]**2))
# B_glr = 1/len(B_corr[:1000])*np.sum(abs(B_corr[:1000]))
# FF_B = B_eff/B_glr

# FF_U_disp = FF_U*np.ones(20)
# FF_B_disp = FF_B*np.ones(20)
# FF_max = 1.111+0.01111*np.ones(20)
# FF_min = 1.111-0.01111*np.ones(20)

# plt.figure()
# plt.plot(FF_B_disp,'g',label="FF_B")
# plt.plot(FF_max,'r',label="max FF")
# plt.plot(FF_min,'r',label="min FF")
# plt.legend()
# plt.ylabel('FF')
# plt.xlabel('samples')
# plt.grid("on")

# %%
