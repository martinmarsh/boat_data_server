from multiprocessing import Process, Value
from .monitor import Monitor


class BoatData:
    """
     'c': ctypes.c_char,     'u': ctypes.c_wchar,
    'b': ctypes.c_byte,     'B': ctypes.c_ubyte,
    'h': ctypes.c_short,    'H': ctypes.c_ushort,
    'i': ctypes.c_int,      'I': ctypes.c_uint,
    'l': ctypes.c_long,     'L': ctypes.c_ulong,
    'q': ctypes.c_longlong, 'Q': ctypes.c_ulonglong,
    'f': ctypes.c_float,    'd': ctypes.c_double


    """
    heading = Value('f', 0.0)
    enable_drive = Value('i', 0)
    roll = Value('i', 0)
    pitch = Value('i', 0)
    max_roll = Value('i', 0)
    max_pitch = Value('i', 0)
    cts = Value('i', 0)
    power = Value('i', 0)
    rudder = Value('f', 0)
    rudder_rate = Value('f', 1.2)
    config = Value('i', 0)
    calibration = Value('i', 0)        # calibration reported by chip
    kp = Value('i', 1)
    ki = Value('i', 0)
    kd = Value('i', 0)
    set_cal = Value('b', 0)           # chip calibration:  0 = no action, 1 = unset, 2 = set
    simulator_on = Value('b', 1)      # 0 = live io,  >0 = simulated io,(2 means reset sim parameters)
    simulator_gain = Value('i', 36)
    simulator_speed = Value('f', 6.0)
    simulator_power_bias = Value('i', 0)


def background(bd):
    Monitor(bd)


def process_start():
    p = Process(target=background, args=(BoatData,))
    p.start()
