from typing import Type, Union, Dict, Any, List, Tuple, Callable
from numpy import ndarray


# Device Types
EPSTEIN = "epstein"
BHC = "bhc"
PBHC = "pbhc"
SENSOR_ARRAY_1 = "sensor_array_1"
DEFAULT = ""

# Signal Form Types
UNIAXIAL = "uniaxial"
ROTATIONAL_CW = "rotational_CW"
ROTATIONAL_CCW = "rotational_CCW"
NELDERMEAD = "nelder_mead"

# Device Parameter
EPSTEIN_PARAM = {"B_turns": (700, "-"),
                 "H_turns": (700, "-"),
                 "l_eff": (0.94, "m"),
                 "Rohrer_voltage_factor": (100, "V/V"),
                 "Rohrer_current_factor": (10, "A/V")}

BHC_PARAM = {"B_amp": (1, "-"),
             "Hx_turns": (834, "-"),
             "Hx_area": (32.789*1e-6, "m^2"),
             "Hx_amp": (1, "-"),
             "Hx_factor": (1.2998118846563584, "-"),
             "Hy_turns": (831, "-"),
             "Hy_area": (32.789*1e-6, "m^2"),
             "Hy_amp": (1, "-"),
             "Hy_factor": (1.299731189472277, "-"),
             "Hall_factor": (1/50, "-"),
             "Rohrer_voltage_factor": (100, "V/V"),
             "Rohrer_current_factor": (10, "A/V")}

PBHC_PARAM = {"Bx_turns": (1, "-"),
              "Bx_amp": (970, "-"),
              "Bx_factor": (1.0633699292753307, "-"),

              "By_turns": (1, "-"),
              "By_amp": (970, "-"),
              "By_factor": (1.053961454331827, "-"),

              "Hx_upper_turns": (51, "-"),
              "Hx_upper_area": (0.02360*0.00024836, "m^2"),
              "Hx_upper_amp": (970, "-"),
              "Hx_upper_factor": (1.3497478190997254, "-"),

              "Hy_upper_turns": (52, "-"),
              "Hy_upper_area": (0.0220*0.00024836, "m^2"),
              "Hy_upper_amp": (970, "-"),
              "Hy_upper_factor": (1.083887512000803, "-"),

              "Hx_lower_turns": (51, "-"),
              "Hx_lower_area": (0.02360*0.00024836, "m^2"),
              "Hx_lower_amp": (970, "-"),
              "Hx_lower_factor": (1, "-"),

              "Hy_lower_turns": (52, "-"),
              "Hy_lower_area": (0.0220*0.00024836, "m^2"),
              "Hy_lower_amp": (970, "-"),
              "Hy_lower_factor": (1, "-"),

              "Hall_factor": (1/50, "-"),

              "Rohrer_voltage_factor": (100, "V/V"),
              "Rohrer_current_factor": (10, "A/V")}


SENSOR_ARRAY_1_PARAM = {"sensor_factor_1": ([0.97841796875,0.97646484375,0.941015625], ("x", "y", "z")),
                        "sensor_factor_2": ([0.965625,0.95986328125,1.0349609375], ("x", "y", "z")),
                        "sensor_factor_3": ([1.037890625,1.03203125,1.0134765625], ("x", "y", "z")),
                        "sensor_factor_4": ([0.972265625,0.971484375,0.971484375], ("x", "y", "z"))}