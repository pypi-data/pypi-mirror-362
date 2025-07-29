import serial
import numpy as np
from datetime import datetime
import tkinter.messagebox as messagebox

class Optic:
    '''
    Die Klasse entspricht dem Matlab-Code vom Husstedt. Jedoch kann für das neue CHRocodile 2 die CHRocodileLib verwendet werden.
    Daher wird diese Klasse bei Lieferung vom neuen Controller auf die CHRocodileLib umgeschrieben.
    '''
    def __init__(self, com_port='COM6', baud_rate=921600): #com_port wird geändert of IP
        self.sp = None
        self.fullscale = None
        self.dmax = None
        self.maxstd = None
        self.war = True
        self.measnumber = 10
        self.intaverage = 1
        self.bytenumber = (self.measnumber + 1) * 20
        self.samplerate = 32
        self.com_port = com_port
        self.baud_rate = baud_rate

    def initialize(self, sensor_type):
        self.sp = serial.Serial(self.com_port, baudrate=self.baud_rate, timeout=1)
        self._send_command('$\n')
        self._send_command('$BIN\n')

        sensor_config = {
            '300': ('0', 330, 1.5),
            '3000': ('1', 3300, 5)
        }

        sen, self.dmax, self.maxstd = sensor_config.get(sensor_type, ('0', 330, 1.5))
        if sensor_type not in sensor_config:
            print(f'Illegal sensor name "{sensor_type}"! The sensor 300µm is selected!')

        self._send_command(f'$SEN{sen}')
        self._send_command('$MOD0\n')
        self._send_command(f'$AVD{self.intaverage}\n')
        self._send_command(f'$SHZ{self.samplerate}\n')
        self._send_command('$SOD1,1,1,1,1,1,1,0,1,1,0,0,0,0,0,0\n')
        self._send_command('$DCY5\n')
        self._send_command('$\n')

        self._send_command('$SCA?\n$\n')
        self.fullscale = float(self.sp.readline().decode().split()[1])

        if self.fullscale not in [330, 3300]:
            print('Fullscale range could not be read correctly!')

    def set_warnings(self, state):
        self.war = state

    def perform_dark_calibration(self):
        if messagebox.askyesno("Confirmation", "Are you really sure that there is no object in the measuring range?"):
            self._send_command('$DRK\n')

    def measure_distance(self):
        self._clear_buffer()
        self._send_command('$CTN\n')
        bytes_read = self.sp.read(self.bytenumber)
        self._send_command('$\n')

        val = self._byte2val(bytes_read)
        addinf = {'val': np.reshape(val, (10, -1)).T}
        addinf['disval'] = addinf['val'][:, 1] / 2**15 * self.fullscale
        ind = np.where(addinf['disval'] > 0)[0]
        addinf['disval'] = addinf['disval'][ind]

        if len(ind) == 0:
            return self._handle_error(addinf, "All distance measuring values are <=0!")

        addinf['std'] = np.std(addinf['disval'])
        addinf['mdisval'] = np.mean(addinf['disval'])
        ret = addinf['mdisval']

        if len(ind) < self.measnumber:
            return self._handle_warning(ret, addinf, f"Only {len(ind)} of {self.measnumber} measuring values are different from zero!")

        if addinf['mdisval'] > self.dmax:
            return self._handle_error(addinf, f"The distance measuring value is >{self.dmax}!")

        if addinf['std'] > self.maxstd:
            return self._handle_warning(ret, addinf, f"The standard deviation is {addinf['std']} >{self.maxstd}µm!")

        return ret, addinf

    # def measure_distance_with_drift_comp(self):
    #     ret, addinf = self.measure_distance()
    #     addinf['drift'] = {
    #         't': datetime.now(),
    #         'cor': self.drift_comp('getdriftspline', addinf['drift']['t'])
    #     }
    #     ret -= addinf['drift']['cor']
    #     return ret, addinf

    def close(self):
        self._send_command('$CTN\n')
        self.sp.close()

    def _send_command(self, command):
        self.sp.write(command.encode())
        self.sp.flush()

    def _clear_buffer(self):
        self.sp.reset_input_buffer()

    def _byte2val(self, bytes_read):
        sind = next((i for i in range(20) if bytes_read[i] == 255 and bytes_read[i+1] == 255), 0) - 1
        return np.frombuffer(bytes_read[sind+1:], dtype=np.uint16)[::2]

    def _handle_error(self, addinf, message):
        if self.war:
            print(f'Error in function "chrocodileE". {message}')
        addinf['std'] = 0
        addinf['mdisval'] = 0
        return np.nan, addinf

    def _handle_warning(self, ret, addinf, message):
        if self.war:
            print(f'Warning in function "chrocodileE". {message}')
        return np.nan, addinf

    # def drift_comp(self, action, t):
    #     # Implement drift compensation logic here
    #     pass

