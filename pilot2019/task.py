



class BoatData:

    heading = 0.0
    enable_drive = 0
    roll = 0
    pitch = 0
    max_roll = 0
    max_pitch = 0
    cts = 0
    power = 0
    rudder = 0
    rudder_rate = 0
    config = 0
    calibration = 0        # calibration reported by chip
    kp = 150
    ki = 5
    kd = 15
    set_cal = 0          # chip calibration:  0 = no action, 1 = unset, 2 = set
    simulator_on = 1      # 0 = live io,  >0 = simulated io,(2 means reset sim parameters)
    simulator_gain = 36
    simulator_speed = 6.0
    simulator_power_bias = 0


