from multiprocessing import Process, Value
from .monitor import Monitor


class BoatData:
    """
     'c': ctypes.c_char,     'u': ctypes.c_wchar,
    'b': ctypes.c_byte,     'B': ctypes.c_ubyte,
    'h': ctypes.c_short,    'H': ctypes.c_ushort,
    'i': ctypes.c_int,      'I': ctypes.c_uint,
    'l': ctypes.c_long,     'L':

    def process_response(self, req, resp, resource, req_succeeded):
        resp.set_header('Access-Control-Allow-Origin', '*')

        if req_succeeded and req.method == 'OPTIONS' and req.get_header('Access-Control-Request-Method'):
            # NOTE(kgriffs): This is a CORS preflight request. Patch the
            #   response accordingly.

            allow = resp.get_header('Allow')
            resp.delete_header('Allow')

            allow_headers = req.get_header(
                'Access-Control-Request-Headers',
                default='*'
            )

            resp.set_headers((
                ('Access-Control-Allow-Methods', allow),
                ('Access-Control-Allow-Headers', allow_headers),
                ('Access-Control-Max-Age', '86400'),  # 24 hours
            ))
ctypes.c_ulong,
    'q': ctypes.c_longlong, 'Q': c

    def process_response(self, req, resp, resource, req_succeeded):
        resp.set_header('Access-Control-Allow-Origin', '*')

        if req_succeeded and req.method == 'OPTIONS' and req.get_header('Access-Control-Request-Method'):
            # NOTE(kgriffs): This is a CORS preflight request. Patch the
            #   response accordingly.

            allow = resp.get_header('Allow')
            resp.delete_header('Allow')

            allow_headers = req.get_header(
                'Access-Control-Request-Headers',
                default='*'
            )

            resp.set_headers((
                ('Access-Control-Allow-Methods', allow),
                ('Access-Control-Allow-Headers', allow_headers),
                ('Access-Control-Max-Age', '86400'),  # 24 hours
            ))
types.c_ulonglong,
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
    kp = Value('i', 150)
    ki = Value('i', 5)
    kd = Value('i', 15)
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
