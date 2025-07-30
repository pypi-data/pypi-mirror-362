#%% Import 
import numpy as np
import pandas as pd
import scipy.integrate

#%% Function
def calc_BCoil(U, fs, f, n_mean, t, amp, turn, area):
    """
    Calculate magnetic flux density form measurements with B-Coil

    Parameters:
        U (np.array): measured voltage
        fs (float): sample frequency
        f (float): excitation frequency
        n_mean (int): Moving average parameter, if n_mean = 1 --> no averaging
        t (np.array): measuring time
        amp (float): amplification of voltage signal
        turn (int): number of windings
        area (float): size of B-coil area

    Return:
        np.array: magnetic flux density
    """
    U_mean = U - np.mean(U)
    num = scipy.integrate.cumtrapz(U_mean, t,initial=0)/(amp*turn*area)
    
    Ns_per = int(fs/f)
    num_corr = np.zeros((Ns_per))
    for id in range(len(num_corr)):
        num_corr[id] = np.mean(num[id:-1:Ns_per])
    
    if n_mean > 1:
        pre = num_corr[-(n_mean//2+1):]
        post = num_corr[:n_mean//2]
        num_corr_ext = np.concatenate((pre, num_corr, post),axis=0)
        series = pd.Series(num_corr_ext)
        num_corr_ext = series.rolling(window=n_mean, center=True).mean()
        num_corr = np.array(num_corr_ext[n_mean//2+1:-n_mean//2])

    num_corr = num_corr - (max(num_corr)+min(num_corr))/2
    return num_corr

def calc_HCoil(U, fs, f, n_mean, t, amp, turn, area):
    """
    Calculate magnetic field strength from measurements with H-Coil

    Parameters:
        U (np.array): measured voltage
        fs (float): sample frequency
        f (float): excitation frequency
        n_mean (int): Moving average parameter, if n_mean = 1 --> no averaging
        t (np.array): measuring time
        amp (float): amplification of voltage signal
        turn (int): number of windings
        area (float): size of H-coil area

    Return:
        np.array: magnetic field strength
    """
    U_mean = U - np.mean(U)
    num = scipy.integrate.cumtrapz(U_mean, t,initial=0,axis=0)/(amp*turn*area*4*np.pi*1e-7)
    
    Ns_per = int(fs/f)
    num_corr = np.zeros((Ns_per))
    for id in range(len(num_corr)):
        num_corr[id] = np.mean(num[id:-1:Ns_per])
    
    if n_mean > 1:
        pre = num_corr[-(n_mean//2+1):]
        post = num_corr[:n_mean//2]
        num_corr_ext = np.concatenate((pre, num_corr, post),axis=0)
        series = pd.Series(num_corr_ext)
        num_corr_ext = series.rolling(window=n_mean, center=True).mean()
        num_corr = np.array(num_corr_ext[n_mean//2+1:-n_mean//2])

    num_corr = num_corr - (max(num_corr)+min(num_corr))/2
    return num_corr

def calc_SenisHallSensor(U, fs, f, n_mean, hall_factor=50):
    """
    Calculate magnetic field strength from measurements with Senis Hall-Sensor

    Parameters:
        U (np.array): measured voltage
        fs (float): sample frequency
        f (float): excitation frequency
        n_mean (int): Moving average parameter, if n_mean = 1 --> no averaging
        hall_factor (int): hall factor of sensor
    Return:
        np.array: magnetic field strength
    """
    U_scale = U/(hall_factor*4*np.pi*1e-7) # 50 = Hall Factor
    U_mean = U_scale - np.mean(U_scale)
    Ns_per = int(fs/f)
    num_corr = np.zeros((Ns_per))
    for id in range(len(num_corr)):
        num_corr[id] = np.mean(U_mean[id:-1:Ns_per])
    
    if n_mean > 1:
        pre = num_corr[-(n_mean//2+1):]
        post = num_corr[:n_mean//2]
        num_corr_ext = np.concatenate((pre, num_corr, post),axis=0)
        series = pd.Series(num_corr_ext)
        num_corr_ext = series.rolling(window=n_mean, center=True).mean()
        num_corr = np.array(num_corr_ext[n_mean//2+1:-n_mean//2])

    num_corr = num_corr - (max(num_corr)+min(num_corr))/2
    return num_corr


def calc_average(U, fs, f, n_mean):
    """
    Calculate Average from measurements using PXI-System 

    Parameters:
        U (np.array): measured quantity
        fs (float): sample frequency
        f (float): excitation frequency
        n_mean (int): Moving average parameter, if n_mean = 1 --> no averaging
    Return:
        np.array: average quantity
    """
    U_mean = U - np.mean(U)
    Ns_per = int(fs/f)
    num_corr = np.zeros((Ns_per))
    for id in range(len(num_corr)):
        num_corr[id] = np.mean(U_mean[id:-1:Ns_per])
    
    if n_mean > 1:
        pre = num_corr[-(n_mean//2+1):]
        post = num_corr[:n_mean//2]
        num_corr_ext = np.concatenate((pre, num_corr, post),axis=0)
        series = pd.Series(num_corr_ext)
        num_corr_ext = series.rolling(window=n_mean, center=True).mean()
        num_corr = np.array(num_corr_ext[n_mean//2+1:-n_mean//2])

    num_corr = num_corr - (max(num_corr)+min(num_corr))/2
    return num_corr
    

def calc_losses(B,H,frequency,density=7600):
    losses = 0.5*np.abs(np.dot(H,np.roll(B,1))-np.dot(B,np.roll(H,1)))
    losses_wpkg = losses * frequency / density
    return losses, losses_wpkg


