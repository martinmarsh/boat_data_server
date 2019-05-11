

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
        self.kp = self.ki = self.kd = None
        self.compass_sample_time = .25
        self.compass_read_at = self.helm_last_read_at = self.compass_read_at = None
        self.heading = 0
        self.last_heading = 0
        self.set_point = 0
        self.gain = 50
        self._last_input = 0
        self.integral = 0
        print(self.kp, self.ki, self.kd, self.gain)

    def set_pid(self, kp, ki, kd, gain):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        # self.pid = PID(self.kp, self.ki, self.kd, setpoint=0)
        # self.pid.sample_time = None
        self.gain = gain
        self._last_input = 0
        self.integral = 0
        # print(self.pid.Kp, self.pid.Ki, self.pid.Kd, self.pid.sample_time, self.gain)

    def get_drive(self, dt, heading, cts):
        self.heading = heading
        self.cts = cts

        # min turn rate resolvable is 1 deci-degree per sec ie 1 degree per 10 seconds, max 1800 is physically unlikely
        turn_rate = int(self.relative_direction(self.heading - self.last_heading) // dt)
        self.last_heading = self.heading

        error = self.relative_direction(self.cts - self.heading)

        abs_error = abs(error)

        # for small errors less than 8 degrees ignore noisy turn rate and make desired rate same as error

        if abs_error > 600:
            turn_limit = 75
        else:
            turn_limit = 50

        if abs_error < 60:
            correction = error//2
        else:

            # make correction the desired rate of turn in deci-degrees
            # A default settlement time of 4 seconds means that at 20 deg the max turn rate will start to reduce
            # at 12 degrees it will be 3 degrees per second
            # at 6 degrees error the settlement time is 3 degrees per seconds and the turn rate

            correction = error//5

            # limit rate to 5 degrees per second
            # correction = turn_limit if correction > turn_
            # limit else -turn_limit if correction < -turn_limit else correction
            if correction > turn_limit:
                correction = turn_limit
            elif correction < -turn_limit:
                correction = -turn_limit

        self.set_point = correction
        helm_adjust = self.pid(turn_rate, dt) * self.gain
        return helm_adjust

    @staticmethod
    def relative_direction(diff):
        diff += 3600 if diff < -1800 else -3600 if diff > 1800 else 0
        return diff

    def pid(self, input_, dt):
        error = self.set_point - input_
        d_input = input_ - self._last_input

        proportional = self.kp * error

        # compute integral and derivative terms
        self.integral += int(self.ki * error * dt)

        derivative = int(-self.kd * d_input / dt)

        # compute final output
        output = proportional + self.integral + derivative

        print(output, 'params:', proportional, derivative, self.integral)

        # keep track of state
        self._last_input = input_

        return output
