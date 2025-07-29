import h5py
import re

from abc import ABC
from MMLToolbox.util.types import *


class StoreH5(ABC):
  def __init__(self, fileName: str) -> None:
    self.fileName = f"{fileName}"

  ################## Create Groups ################## 
  def create_group(self, groups: List) -> None:
    with h5py.File(f"{self.fileName}.hdf5", "w") as hf:
      for group in groups:
        hf.create_group(group)

  ################## write ################## 
  def write(self, group: str, data: Dict[str, Any], iter: int=None) -> None:
    with h5py.File(f"{self.fileName}.hdf5", "a") as hf:
      grp = hf[group]
      if iter is None: 
        pass
        self._write_without_iter(grp,data)
      else:
        self._write_with_iter(grp,data,iter)


  def _write_without_iter(self,grp: h5py.Group, data: Dict[str,Any]) -> None:
    for name, value in data.items():
      grp.create_dataset(name=name, data=value)


  def _write_with_iter(self,grp: h5py.Group, data: Dict[str,Any],iter: int) -> None:
    if f"step-{int(iter)}" in grp:
      grp_step = grp[f"step-{iter}"]
    else:
      grp_step = grp.create_group(f"step-{iter}")

    for name, value in data.items():
      grp_step.create_dataset(name=name, data=value)


  ################## APPEND ##################
  def append(self, group: str, data: Dict[str, Any]) -> None:
    with h5py.File(f"{self.fileName}.hdf5", "a") as hf:
      grp = hf[group]
      for attr, value in data.items():
        if attr not in grp:
          self.write(group,{attr: value})
        else:
          old_data = list(self.read(group, attr))
          new_data = old_data + list(value)
          del grp[attr]
          self.write(group,{attr: new_data})


  ################## READ ################## 
  def read(self,group: str, attr: str, iter=None):
    with h5py.File(f"{self.fileName}.hdf5", "r") as hf:
      grp = hf[group]
      if iter is None:
        return self._read_without_iter(grp, attr)
      else:
        return self._read_with_iter(grp, attr, iter)


  def _read_without_iter(self,grp: h5py.Group, attr: str):
    if attr == "all":
      return self._read_all_attr(grp)
    else:
      return self._read_single_attr(grp,attr)


  def _read_with_iter(self,grp: h5py.Group, attr: str, iter):
    returnDict = {}
    if iter == "all":
      for iter_step in grp.keys():
        grp_iter = grp[iter_step]
        if attr == "all":
          returnDict[iter_step] = self._read_all_attr(grp_iter)
        else:
          returnDict[iter_step] = self._read_single_attr(grp_iter,attr)
      return dict(sorted(returnDict.items(), key=lambda item: int(re.search("(\d+)",item[0]).group(1))))
    else:
      grp_iter = grp[f"step-{iter}"]
      if attr == "all":
        return self._read_all_attr(grp_iter)
      else:
        return self._read_single_attr(grp_iter,attr)


  def _read_all_attr(self,grp):
    returnDict={}
    for attr in grp.keys():
      returnDict[attr] = grp[attr][()]
    return returnDict


  def _read_single_attr(self,grp: h5py.Group,attr:str):
    return grp[attr][()]
  


