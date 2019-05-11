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
    roll = Value('i', 0)
    pitch = Value('i', 0)
    max_roll = Value('i', 0)
    max_pitch = Value('i', 0)
    cts = Value('i', 0)
    power = Value('i', 0)
    config = Value('i', 0)
    calibration = Value('i', 0)  # reported calibration
    kp = Value('i', 50)
    ki = Value('i', 3)
    kd = Value('i', 25)
    set_cal = Value('i', 0)  # 0 = no action, 1 = unset, 2 = set


def background(bd):
    Monitor(bd)


def process_start():
    p = Process(target=background, args=(BoatData,))
    p.start()
