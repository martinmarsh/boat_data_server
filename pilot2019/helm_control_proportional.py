from simple_pid import PID


class Helm:

    def __init__(self):
        """
        example settings:   kp = Value('f', 1)
        ki = Value('f', 0.05)
         kd = Value('f', 0.5)
        gain= Value('i', 50)
        with simulation:
                 self.gain = 0.01
        self.momentum = 1
        self.helm_direction = 1
        self.power_bias = 0


        """
        self.cts = -1
        self.pid = self.kp = self.ki = self.kd = None
        self.heading = 0
        self.last_heading = 0
        self.gain = 50
        print(self.kp, self.ki, self.kd, self.gain)

    def set_pid(self, kp, ki, kd, gain):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.pid = PID(self.kp, self.ki, self.kd,
                       setpoint=0,
                       sample_time=None,
                       output_limits=(None, None),
                       proportional_on_measurement=True
                       )

        self.gain = gain
        print(self.pid.Kp, self.pid.Ki, self.pid.Kd, self.pid.sample_time, self.gain)

    def get_drive(self, dt, heading, cts):
        self.heading = heading
        self.cts = cts

        error = self.relative_direction(self.cts - self.heading)

        helm_adjust = self.pid(-error) * self.gain
        print(self.pid.components)

        return helm_adjust

    @staticmethod
    def relative_direction(diff):
        diff += 3600 if diff < -1800 else -3600 if diff > 1800 else 0

        return diff
