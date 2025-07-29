import h5py 
import numpy as np
import scipy.signal._savitzky_golay
import numpy as np

from .StoreSetup import StoreSetup
from math import factorial
from scipy.interpolate import interp1d
from scipy.optimize import root

MU_0 = 4*np.pi*1e-7

class EvalPostProc():
    def __init__(self, h5Folder):
        self.h5Folder = h5Folder
        self.ss = None
        self.info = {}
        self.B_meas = None        # Measured B
        self.H_meas = None        # Measured H
        self.B_smooth = None      # Filtered B
        self.H_smooth = None      # Filtered H
        self.B_correct = None     # Correct B by using Function correctHystCurveInterpolateAnhystereticCurve
        self.H_correct = None     # Correct H by using Function correctHystCurveInterpolateAnhystereticCurve
        self.B_an = None          # Anhysterese B by using Function origHystCurveInterpolateAnhystereticCurve
        self.H_an = None          # Anhysterese H by using Function origHystCurveInterpolateAnhystereticCurve
        self.B_an_correct = None  # Anhysterese B by using Function correctHystCurveInterpolateAnhystereticCurve
        self.H_an_correct = None  # Anhysterese H by using Function correctHystCurveInterpolateAnhystereticCurve
        self.B_commutation = None # B of commutation curve by using max(B)
        self.H_commutation = None # H of commutation curve by using max(H)
        self.B_mur = None         # B used for relative Permeability
        self.H_mur = None         # H used for relative Permeability
        self.mur_sec = None       # Relative Permeability based on B/H
        self.mur_grad = None      # Relative Premeability based on dB/dH

    ################################
    # User Functions
    ################################
    def readBHResults(self,filename,step,B_dir,H_dir) -> None:
        self.ss = StoreSetup(f"./{self.h5Folder}/{filename}")
        
        B_values = self.ss.readPostProc(step, B_dir)
        H_values = self.ss.readPostProc(step, H_dir)

        H_values = self.__correctOrientation(B_values,H_values)
        self.B_meas = B_values
        self.H_meas = H_values

        self.info["step"] = step
        self.info["B_dir"] = B_dir
        self.info["H_dir"] = H_dir

    def filterMeasurements(self,windowsize,order):
        #TODO: Implement twostepfilter wie in julia --> gibt es das in Python überhaupt?
        H_smooth = scipy.signal.savgol_filter(self.H_meas,windowsize, order)
        B_smooth = scipy.signal.savgol_filter(self.B_meas,windowsize, order)
        
        self.B_smooth = B_smooth
        self.H_smooth = H_smooth

    def correctHystCurveInterpolateAnhystereticCurve(self,B,H,numSamplePoints):      
        # Get Anhysterese from Data
        B_an,H_an,B_an_itp_of_H,B_asc,H_asc,B_desc,H_desc = self.__interpolateAnhystereticCurve(B,H,numSamplePoints)
        self.B_an = B_an
        self.H_an = H_an
        self.info["B_asc"] = B_asc
        self.info["H_asc"] = H_asc
        self.info["B_desc"] = B_desc
        self.info["H_desc"] = H_desc

        # Correct Hysterese based on computed Anhysterse
        delta_H, H_correct = self.__correctHystCurve(H,B_an_itp_of_H)
        B_an,H_an,B_an_itp_of_H,B_asc,H_asc,B_desc,H_desc = self.__interpolateAnhystereticCurve(B,H_correct,numSamplePoints)

        self.B_an_correct = B_an
        self.H_an_correct = H_an
        self.B_correct = B
        self.H_correct = H_correct
        self.info["B_asc_correct"] = B_asc
        self.info["H_asc_correct"] = H_asc
        self.info["B_desc_correct"] = B_desc
        self.info["H_desc_correct"] = H_desc
        self.info["delta_H"] = delta_H
        return B_an_itp_of_H
    
    def getCommutationCurve(self,B,H):
        self.B_commutation = max(B)
        self.H_commutation = max(H)
    
    def getPermeability(self,B,H,H_min=1):
        # Neglect H-Values smaller than Hmin, this makes some issue computing the permeability        
        mask = np.abs(H) >= H_min
        self.B_mur = np.array(B[mask])
        self.H_mur = np.array(H[mask])

        self.mur_sec = self.__getPermeabilitySecMethod(self.B_mur,self.H_mur)
        self.mur_grad = self.__getPermeabilityGradMethod(self.B_mur,self.H_mur)

    def saveResults(self,step=None,B_dir=None,H_dir=None):
        step = step if step is not None else self.info["step"]
        B_dir = B_dir if B_dir is not None else self.info["B_dir"]
        H_dir = H_dir if H_dir is not None else self.info["H_dir"]
        dir_temp = B_dir[1]

        self.ss.writeEval(step,f"{B_dir}_meas",self.B_meas)
        self.ss.writeEval(step,f"{B_dir}_smooth",self.B_smooth)
        self.ss.writeEval(step,f"{B_dir}_correct", self.B_correct)
        self.ss.writeEval(step,f"{B_dir}_an",self.B_an)
        self.ss.writeEval(step,f"{B_dir}_an_correct",self.B_an_correct)
        self.ss.writeEval(step,f"{B_dir}_commutation",self.B_commutation)
        self.ss.writeEval(step,f"{B_dir}_mur",self.B_mur)

        self.ss.writeEval(step,f"{H_dir}_meas",self.H_meas)
        self.ss.writeEval(step,f"{H_dir}_smooth",self.H_smooth)
        self.ss.writeEval(step,f"{H_dir}_correct",self.H_correct)
        self.ss.writeEval(step,f"{H_dir}_an",self.H_an)
        self.ss.writeEval(step,f"{H_dir}_an_correct",self.H_an_correct)
        self.ss.writeEval(step,f"{H_dir}_commutation",self.H_commutation)
        self.ss.writeEval(step,f"{H_dir}_mur",self.H_mur)

        self.ss.writeEval(step,f"mur_sec_{dir_temp}",self.mur_sec)
        self.ss.writeEval(step,f"mur_grad_{dir_temp}",self.mur_grad)

    ################################
    # Internal Functions
    ################################

    # Staticmethod
    @staticmethod
    def __correctOrientation(B,H):
        H_corr = np.array(H)
        max_index_B = np.argmax(B)
        if H[max_index_B] < 0.0:
            H_corr = H_corr * -1
        return H_corr
    
    @staticmethod
    def __findAscendingDescendingIndices(H, M):
        ind_ascending = []
        ind_descending = []
        for n in range(len(H)): 
            if not np.any((H > H[n]) & (M < M[n])): 
                ind_ascending.append(n) 
            elif not np.any((H < H[n]) & (M > M[n])): 
                ind_descending.append(n)
        return ind_ascending, ind_descending
    
    @staticmethod
    def __uniqueSort(B, H):
        ha = np.sort(H) 
        ba = np.sort(B) 
        b, index = np.unique(ba, return_index=True)
        h = ha[index]
        return b, h
    
    @staticmethod
    def __correctHystCurve(H, B_an_itp_of_H):
        s = root(B_an_itp_of_H, [0.0], method='hybr')
        deltaH = s.x[0]
        H_correct = H - deltaH
        return np.array(deltaH), np.transpose(H_correct)
    
    @staticmethod
    def __getPermeabilitySecMethod(B,H):
        temp = B/H
        mur = temp/MU_0
        return mur
    
    @staticmethod
    def __getPermeabilityGradMethod(B,H):
        temp = np.gradient(B,H)
        mur = temp/MU_0
        return mur

    # Non-static Methoc
    def __interpolateAnhystereticVector(self,B,H,num_sample_points):
        ind_ascending, ind_descending = self.__findAscendingDescendingIndices(H,B)

        B_asc, H_asc = self.__uniqueSort(B[ind_ascending], H[ind_ascending])
        B_desc, H_desc = self.__uniqueSort(B[ind_descending], H[ind_descending])

        Ba = np.linspace(min(np.min(B_asc), np.min(B_desc)), max(np.max(B_asc), np.max(B_desc)), num_sample_points)
      
        H_asc_of_M = interp1d(B_asc, H_asc, fill_value="extrapolate")
        H_desc_of_M = interp1d(B_desc, H_desc, fill_value="extrapolate")
     
        H_asc_itp = H_asc_of_M(Ba)
        H_desc_itp = H_desc_of_M(Ba)
        H_avg = (H_asc_itp + H_desc_itp) / 2
        B_of_H = interp1d(H_avg, Ba, fill_value="extrapolate")
        return H_avg,Ba,B_of_H,H_asc_itp,H_desc_itp
      
    def __interpolateAnhystereticCurve(self,B, H, numSamplePoints):
        H_an_vector,Ba,B_an_itp_of_H_vector,H_asc_vector, H_desc_vector = self.__interpolateAnhystereticVector(B,H,numSamplePoints)
        H_an = H_an_vector
        B_an = B_an_itp_of_H_vector(H_an_vector)
        H_asc = H_asc_vector
        H_desc = H_desc_vector
        B_asc = Ba
        B_desc = Ba
        B_an_itp_of_H = B_an_itp_of_H_vector
        
        return B_an,H_an,B_an_itp_of_H,B_asc,H_asc,B_desc,H_desc

 

    
    

    

