#%% Import
import h5py
import collections.abc
import re
import math 

from MMLToolbox.util.types import *

#%% Define Class

class StoreSetup:
  """This class can be used to store the data you get from your PXI system and also data you acquire through post-processing in an HDF5 file."""

  def __init__(self, fileName:str = "", meastype:str="", B_turns=3, sample_thickness=0, sample_width=0, sample_number=0, drill_width=[0,0], drill_diameter=0) -> None:
    """The constructore will create a hdf5 file with the given name. Additionaly the user can specify the type of measurement
    they want to performe. The constructore will initialise the hdf5 file with measurement specific information that can be used 
    for post proscessing."""
    
    self.fileName = fileName
    self.meastype = meastype
    self.B_turns = B_turns
    self.sample_thickness = sample_thickness
    self.sample_width = sample_width
    self.sample_number = sample_number
    self.drill_width = drill_width
    self.drill_diameter = drill_diameter         

  def initMeasurementProtocol(self) -> None:
    self.__createFile()

    if self.meastype.lower() == DEFAULT:
        info_dict_meas = {}
        info_dict_sample = {}
      
    if self.meastype.lower() == EPSTEIN:
      info_dict_sample = {"sample_thikness": (self.sample_thickness, "m"), 
                          "sample_width": (self.sample_width, "m"),
                          "sample_number": (self.sample_number, "-"),
                          "B_area": (self.sample_thickness*self.sample_width*self.sample_number, "m^2")}
      info_dict_meas = EPSTEIN_PARAM

    if self.meastype.lower() == BHC:
      info_dict_sample = {"sample_thikness": (self.sample_thickness, "m"), 
                          "B_turns": (self.B_turns, "-"),
                          "drill_width_x": (self.drill_width[0], "m"),
                          "drill_width_y": (self.drill_width[1], "m"),
                          "drill_diameter": (self.drill_diameter, "m"),
                          "Bx_mat_area": ((self.drill_width[0]-self.drill_diameter)*self.sample_thickness, "m^2"),
                          "By_mat_area": ((self.drill_width[1]-self.drill_diameter)*self.sample_thickness, "m^2"),}
      info_dict_meas = BHC_PARAM
      
    if self.meastype.lower() == PBHC:  
      info_dict_sample = {"sample_thickness": (self.sample_thickness, "m"), 
                          "drill_width_x": (self.drill_width[0], "m"),
                          "drill_width_y": (self.drill_width[1], "m"),
                          "drill_diameter": (self.drill_diameter, "m"),
                          "Bx_mat_area": ((self.drill_width[0]-self.drill_diameter)*self.sample_thickness, "m^2"),
                          "By_mat_area": ((self.drill_width[1]-self.drill_diameter)*self.sample_thickness, "m^2"),
                          "Bx_air_area": (7.270989610030249e-06+self.sample_thickness*(self.drill_diameter-1e-3), "m^2"),
                          "By_air_area": (5.596711050782946e-06+self.sample_thickness*(self.drill_diameter-1e-3), "m^2")}
      info_dict_meas = PBHC_PARAM

    if self.meastype.lower() == SENSOR_ARRAY_1:
      info_dict_sample = {"sample_thikness": (self.sample_thickness, "m")}
      info_dict_meas = SENSOR_ARRAY_1_PARAM
    

    info = {**info_dict_meas,**info_dict_sample}
    self.writeInfo(info)

  def __createFile(self) -> None:
    """This function creates an HDF5 file with the following groups:
    info: Used to give a brief description about the measurement circuit and/or specific information about the measurements.
    
    data: Used to store data acquired from the measurement. It does not matter if the data comes from the DMMs or analog inputs.
    outputSignal: Used to store the electrical signal that was used to perform the measurement.
    postProc: Used to store the data after it was processed.
    """
    with h5py.File(f"{self.fileName}.hdf5", "w") as hf:
      hf.create_group("info")
      hf.create_group("data")
      hf.create_group("outputSignal")
      hf.create_group("postProc")
      hf.create_group("eval")
      hf.create_group("ilc")

#################################
# Update Functions
#################################

  def insertData(self, stepNumber, dataName, data):
    with h5py.File(f"{self.fileName}.hdf5", "r+") as hf:
      
      dict_length = len(hf["data"])
      prev_data = hf["data"][f"step-{stepNumber}"]
      del hf["data"][f"step-{stepNumber}"]
      self.writeData(stepNumber,dataName, data)
      
      for i in range(stepNumber + 1, dict_length):
        current_data = hf["data"][f"step-{i}"]
        del hf["data"][f"step-{i}"]
        hf["data"][f"step-{i}"] = prev_data

        prev_data = current_data
      
      hf["data"][f"step-{dict_length}"] = prev_data
        

  def insertOutputSignal(self, stepNumber, dataName, data):
    with h5py.File(f"{self.fileName}.hdf5", "r+") as hf:
      
      dict_length = len(hf["outputSignal"])
      prev_data = hf["outputSignal"][f"step-{stepNumber}"]
      del hf["outputSignal"][f"step-{stepNumber}"]
      self.writeOutputSignal(stepNumber,dataName, data)
      
      for i in range(stepNumber + 1, dict_length):
        current_data = hf["outputSignal"][f"step-{i}"]
        del hf["outputSignal"][f"step-{i}"]
        hf["outputSignal"][f"step-{i}"] = prev_data

        prev_data = current_data
      
      hf["outputSignal"][f"step-{dict_length}"] = prev_data
        

  def updateNumIntervalls(self):
    with h5py.File(f"{self.fileName}.hdf5", "r+") as hf:
      del hf["info"]["numIntervalls"]
      hf["info"]["numIntervalls"] = len(hf["data"]) 


#################################
# Write FUnctions
#################################
  def write(self,grp_name,iter,data_name,data):
    """ This method is used to store in the HDF5 file.

    :param grp_name: The name of the group in which the data should be stored
    :type grp_name: str
    
    :param iter: The iteration number when performing multiple measurements.
    :type iter: int

    :param dataName: The name(s) of the data that you want to store.
    :type dataName: str or list

    :param data: The data or a 2D list of different data sets you want to store.
    :type data: list or 2D list

    :return: None
    :rtype: None
    """    
    with h5py.File(f"{self.fileName}.hdf5", "a") as hf:
      grp = hf[grp_name]

      if f"step-{iter}" in grp:
        if isinstance(data_name,collections.abc.Iterable) and not isinstance(data_name,str):
          for name in data_name:
            if name in grp[f"step-{iter}"]: del grp[f"step-{iter}"][name]
        else:
          if data_name in grp[f"step-{iter}"]: del grp[f"step-{iter}"][data_name]

      if isinstance(data_name,collections.abc.Iterable) and not isinstance(data_name,str):
        self.__writeIterable(grp,iter,data_name,data)
      else:
        self.__writeSingle(grp,iter,data_name,data)


  def writeData(self,iter,dataName,data) -> None:
    """ This method is used to store acquired data in the HDF5 file.

    :param iter: The iteration number when performing multiple measurements.
    :type iter: int

    :param dataName: The name(s) of the data that you want to store.
    :type dataName: str or list

    :param data: The data or a 2D list of different data sets you want to store.
    :type data: list or 2D list

    :return: None
    :rtype: None
    """
    grp_name = "data"
    self.write(grp_name,iter,dataName,data)


  def writeOutputSignal(self,iter,dataName,data) -> None:
    """This method is used to store one or more output signals used to power the measurement circuit.

    :param iter: The iteration number when performing multiple measurements.
    :type iter: int

    :param dataName: The name(s) of the data that you want to store.
    :type dataName: str or list

    :param data: The data or a 2D list of different data sets you want to store.
    :type data: list or 2D list

    :return: None
    :rtype: None    
    """
    grp_name = "outputSignal"
    self.write(grp_name,iter,dataName,data)


  def writePosProc(self,iter,dataName,data) -> None:
    """    This method is used to store all the processed data in the HDF5 file.

    :param iter: The iteration number when performing multiple measurements.
    :type iter: int

    :param dataName: The name(s) of the data that you want to store.
    :type dataName: str or list

    :param data: The data or a 2D list of different data sets you want to store.
    :type data: list or 2D list

    :return: None
    :rtype: None
    """
    grp_name = "postProc"
    self.write(grp_name,iter,dataName,data)

  def writeEval(self,iter,dataName,data) -> None:
    """    This method is used to store all the processed data in the HDF5 file.

    :param iter: The iteration number when performing multiple measurements.
    :type iter: int

    :param dataName: The name(s) of the data that you want to store.
    :type dataName: str or list

    :param data: The data or a 2D list of different data sets you want to store.
    :type data: list or 2D list

    :return: None
    :rtype: None
    """
    grp_name = "eval"
    self.write(grp_name,iter,dataName,data)


  def writeILC(self,iter,dataName,data) -> None:
    """    This method is used to store all the processed data in the HDF5 file.

    :param iter: The iteration number when performing multiple measurements.
    :type iter: int

    :param dataName: The name(s) of the data that you want to store.
    :type dataName: str or list

    :param data: The data or a 2D list of different data sets you want to store.
    :type data: list or 2D list

    :return: None
    :rtype: None
    """
    grp_name = "ilc"
    self.write(grp_name,iter,dataName,data)

  def writeInfo(self, infoData) -> None:
    """This function takes a nested dictionary and uses the keys as names for groups where it will store the connected data.

    :param infoData:  A dictionary that can contain other dictionaries or tuples. All keys in the dictionary will be used as group names.
    :type infoData: dict

    :return: None
    :rtype: None
    """

    self._sample_frequency_feasible(infoData)

    with h5py.File(f"{self.fileName}.hdf5", "a") as hf:
      grp_info = hf["info"]

      for group_name, data in infoData.items():
        if group_name in grp_info:
          del grp_info[group_name]
        grp_name = grp_info.create_group(group_name)

        if isinstance(data, dict):
          names = list(data.keys())

          for name in names:
            items: dict = data[name]
            hfKey = grp_name.create_group(name)

            for key, item in items.items():
              self.__writeInfoEntry(hfKey,item,key)

        else:
          if isinstance(data, tuple):
            value, unit = data
            self.__writeInfoEntry(grp_name,value,"value",unit)


  def __writeInfoEntry(self,grp_name:h5py.File,value,name:str="value",unit:str="") -> None:
    if value is str:
      grp_name.create_dataset(name=name, data=value, dtype=h5py.special_dtype(vlen=str))
    else:
      grp_name.create_dataset(name=name, data=value)

    if unit != "":
      grp_name.create_dataset(name="unit", data=unit, dtype=h5py.special_dtype(vlen=str))


  def __writeIterable(self,grp,iter,dataName,data) -> None:
    if f"step-{int(iter)}" in grp:
      grp_name = grp[f"step-{int(iter)}"]
    else:
      grp_name = grp.create_group(f"step-{int(iter)}")

    for name, value in zip(dataName,data):
      grp_name.create_dataset(name=name, data=value)


  def __writeSingle(self,grp,iter,name,value) -> None:
    if f"step-{int(iter)}" in grp:
      grp_name = grp[f"step-{int(iter)}"]
    else:
      grp_name = grp.create_group(f"step-{int(iter)}")

    grp_name.create_dataset(name=name, data=value)




#################################
# Read Functions
#################################
  def read(self,grp_name,iter="all",store_name="all"):
    """This method will return either the data of a specific iteration or of all iterations of specific Group. You can also choose all the available data of an iteration or only specified data.

    :param grp_name: name of group
    :type grp_name: str
    
    :param iter: (optional int) The iteration number that you want to get the data from. If no value is given, the data of all iterations will be returned.
    :type iter: int or None

    :param storeName: (optional string) The specific data you want from an iteration. If no value is given, all available data will be returned.
    :type storeName: str or None

    :return: None
    :rtype: None
    """
    with h5py.File(f"{self.fileName}.hdf5", "r") as hf:
      grp = hf[grp_name]
      if iter == "all":
        return self.__readIter(grp,store_name)
      else:
        return self.__readSingleIter(grp,iter,store_name)    

  def readData(self,iter="all",store_name="all"):
    """This method will return either the data of a specific iteration or of all iterations. You can also choose all the available data of an iteration or only specified data.

    :param iter: (optional int) The iteration number that you want to get the data from. If no value is given, the data of all iterations will be returned.
    :type iter: int or None

    :param storeName: (optional string) The specific data you want from an iteration. If no value is given, all available data will be returned.
    :type storeName: str or None

    :return: None
    :rtype: None
    """
    grp_name = "data"
    return self.read(grp_name,iter,store_name)
  
  def readILC(self,iter="all",store_name="all"):
    """This method will return either the data of a specific iteration or of all iterations. You can also choose all the available data of an iteration or only specified data.

    :param iter: (optional int) The iteration number that you want to get the data from. If no value is given, the data of all iterations will be returned.
    :type iter: int or None

    :param storeName: (optional string) The specific data you want from an iteration. If no value is given, all available data will be returned.
    :type storeName: str or None

    :return: None
    :rtype: None
    """
    grp_name = "ilc"
    return self.read(grp_name,iter,store_name)

  def readInfoValue(self,storeName):
    """    Returns the value of an item stored in the `info` group.

    :param storeName: The name of the item you want to get.
    :type storeName: str

    :return: None
    :rtype: None
    """
    with h5py.File(f"{self.fileName}.hdf5", "r") as hf:
      grp = hf[f"info/{storeName}"]
      return self.__readSingleStoreName(grp,"value")
    
  def readInfo(self,storeName):
    """    Returns all values of an item stored in the `info` group as dictionary.

    :param storeName: The name of the item you want to get.
    :type storeName: str

    :return: None
    :rtype: None
    """
    grp_name = f"info/{storeName}"
    returnDict = {}
    with h5py.File(f"{self.fileName}.hdf5", "r") as hf:
      grp = hf[grp_name]
      for iterStep in grp.keys():
        grpIter = grp[iterStep]
        returnDict[iterStep] = self.__readStoreName(grpIter)
    return returnDict
    
  def readPostProcInfoValue(self,storeName):
    """"""
    with h5py.File(f"{self.fileName}.hdf5", "r") as hf:
      grp = hf[f"postProc/{storeName}"]
      return self.__readSingleStoreName(grp,"value")
      
  def readOutputSignal(self,iter="all",store_name="all"):
    """    This method will return either the output signal of a specific iteration or of all iterations. You can also choose all the available data of an iteration or only specified data.

    :param iter: (optional int) The iteration number that you want to get the data from. If no value is given, the data of all iterations will be returned.
    :type iter: int or None

    :param storeName: (optional string) The specific data you want from an iteration. If no value is given, all available data will be returned.
    :type storeName: str or None

    :return: None
    :rtype: None
    """
    grp_name = "outputSignal"
    return self.read(grp_name,iter,store_name)


  def readPostProc(self,iter="all",store_name="all"):
    """    This method will return either the processed data of a specific iteration or of all iterations. You can also choose all the available data of an iteration or only specified data.

    :param iter: (optional int) The iteration number that you want to get the data from. If no value is given, the data of all iterations will be returned.
    :type iter: int or None

    :param storeName: (optional string) The specific data you want from an iteration. If no value is given, all available data will be returned.
    :type storeName: str or None

    :return: None
    :rtype: None
    """
    grp_name = "postProc"
    return self.read(grp_name,iter,store_name)

      
  def readEval(self,iter="all",store_name="all"):
    """    This method will return either the processed data of a specific iteration or of all iterations. You can also choose all the available data of an iteration or only specified data.

    :param iter: (optional int) The iteration number that you want to get the data from. If no value is given, the data of all iterations will be returned.
    :type iter: int or None

    :param storeName: (optional string) The specific data you want from an iteration. If no value is given, all available data will be returned.
    :type storeName: str or None

    :return: None
    :rtype: None
    """
    grp_name = "eval"
    return self.read(grp_name,iter,store_name)


  def __readIter(self,grp,storeName):
    returnDict = {}
    for iterStep in grp.keys():
      if iterStep != "info":
        grpIter = grp[iterStep]
        if storeName == "all":
          returnDict[iterStep] = self.__readStoreName(grpIter)
        else:
          returnDict[iterStep] = self.__readSingleStoreName(grpIter,storeName)

    return dict(sorted(returnDict.items(), key=lambda item: int(re.search("(\d+)",item[0]).group(1))))

  def __readSingleIter(self,grp,iter,storeName):
    grp = grp[f"step-{int(iter)}"]
    if storeName == "all":
      return self.__readStoreName(grp)
    else:
      return self.__readSingleStoreName(grp,storeName)

  def __readStoreName(self,grp):
    returnDict={}
    for storeName in grp.keys():
        if grp[storeName].shape == ():
          grpStoreName = grp[storeName][()]
          if isinstance(grpStoreName,bytes):
            returnDict[storeName] = grpStoreName.decode('utf-8')
          else:
            returnDict[storeName] = grpStoreName
        else:  
          returnDict[storeName] = grp[storeName][:]
    return returnDict

  def __readSingleStoreName(self,grp,storeName):
    return grp[storeName][()]


  #################################
  # Delete Functions
  #################################
  def delete(self,grp_name,iter):
    with h5py.File(f"{self.fileName}.hdf5", "a") as hf:
      grp = hf[grp_name]

      if f"step-{iter}" in grp:
        del grp[f"step-{iter}"]

  #################################
  # Helper Functions
  #################################
  @staticmethod
  def _adjust_sample_frequency_factor(frequency: float, sample_factor: float, factor_base: float) -> float:
    samplefreq = frequency * sample_factor
    param = factor_base / samplefreq

    if param.is_integer():
        return sample_factor  # No change needed

    param_new = max(1, math.floor(param))
    adjusted_factor = factor_base / (param_new * frequency)

    return adjusted_factor

  def _sample_frequency_feasible(self,info_dict:Dict):
    frequency = info_dict.get("frequency")
    if frequency is None:
        return 
    
    frequency = frequency[0]

    # Check and correct sampleFrequencyFactor
    if "sampleFrequencyFactor" in info_dict:
        original = info_dict["sampleFrequencyFactor"][0]
        factor_base = 1.8e6
        adjusted = self._adjust_sample_frequency_factor(frequency, original, factor_base)

        if adjusted != original:
            info_dict["sampleFrequencyFactor"] = (adjusted,"-")
            print(f"##########################\nSampleFrequencyFactor not feasible.\nChanged sampleFrequencyFactor to {adjusted:.2f}\n##########################")

    # Check and correct sampleFrequencyFactorDAQ
    if "sampleFrequencyFactorDAQ" in info_dict:
        original = info_dict["sampleFrequencyFactorDAQ"][0]
        factor_base = 100e6
        ni_inputs = info_dict.get("niInput", [])
        max_limit = 2e6 / (len(ni_inputs) * 2 * frequency) if ni_inputs else None
        adjusted = min(self._adjust_sample_frequency_factor(frequency, original, factor_base),max_limit)
        
        if adjusted != original:
            info_dict["sampleFrequencyFactorDAQ"] = (adjusted,"-")
            print(f"##########################\nSampleFrequencyFactorDAQ not feasible.\nChanged sampleFrequencyFactorDAQ to {adjusted:.2f}\n##########################")














