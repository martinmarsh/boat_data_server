from time import monotonic


class Helm:

    def __init__(self):
        """
        example settings:
             kp = Value('f', 50)
             ki = Value('f', 3)
             kd = Value('f', 25)

        with simulation:
            self.gain = 0.01
             self.momentum = 1
            self.power_bias = 0
        """
        self.cts = -1
        self.kp = self.ki = self.kd = None
        self.compass_sample_time = .25
        self.compass_read_at = self.helm_last_read_at = self.compass_read_at = None
        self.heading = 0
        self.last_heading = 0
        self.set_point = 0
        self._last_input = 0
        self.integral = 0
        self.d_input = 0
        self.helm_full_start = False
        self.error = 0
        self.turn_rate = 0
        self.power = 0
        self.rudder_rate = 0
        self.rudder_position = 0
        self.power_direction = 1          # power power_direction
        self.turn_direction = 1

    def set_tunings(self, kp, kd, ki, rudder_rate):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.rudder_rate = rudder_rate
        self._last_input = 0
        self.integral = 0
        print(self.kp,  self.kd,  self.ki, self.rudder_rate)

    def fast_response_drive(self, heading, cts):
        self.cts = cts
        error = self.relative_direction(self.cts - heading)
        direction = -1 if error < 0 else 1
        if abs(error) > 90 and not self.helm_full_start:
            self.integral = 0
            self.d_input = 0
            self.power = 1000
            self.power_direction = direction
            self.helm_full_start = monotonic()
        return self.power, self.power_direction

    def _major_course_control(self):
        turning_time = monotonic() - self.helm_full_start
        direction = -1 if self.error < 0 else 1
        abs_turn_rate = abs(self.turn_rate)
        power = 1000

        if abs_turn_rate > 10:
            self.integral = 0
            time_to_cts = abs(self.error / self.turn_rate)
            if time_to_cts < turning_time:
                direction = -direction
                if abs_turn_rate < 50:
                    self.helm_full_start = False
            if (abs(self.turn_rate) > 100 or abs(self.rudder_position) > 20) and self.turn_direction == direction:
                power = 0
        elif abs(self.rudder_position) > 2:
            self.helm_full_start = False
            self.integral = 0

        return power, direction

    def get_drive(self, dt, heading, cts):
        self.estimate_rudder_position(dt)
        self.heading = heading
        self.cts = cts

        # min turn rate resolvable is 1 deci-degree per sec ie 1 degree per 10 seconds, max 1800 is physically unlikely
        self.turn_rate = int(self.relative_direction(self.heading - self.last_heading) // dt)
        self.turn_direction = -1 if self.turn_rate < 0 else 1
        self.last_heading = self.heading

        self.error = self.relative_direction(self.cts - self.heading)
        abs_error = abs(self.error)

        # When a large course change is ordered control boat turning rate until in PID control range
        if self.helm_full_start:
            if abs_error < 90:
                self.helm_full_start = False
                self.integral = 0
            else:
                return self._major_course_control()

        if abs_error < 50 and abs(self.turn_rate) < 10:
            self.rudder_position = 0

        # make correction the desired rate of turn in deci-degrees
        # A default settlement time of 6 seconds means that:
        # at 9 degrees it will be 1.5 degrees per second
        # at 6 degrees error the settlement time is 1 degrees per second

        correction = self.error//6

        # limit rate to 5 degrees per second
        # correction = turn_limit if correction > turn_
        # limit else -turn_limit if correction < -turn_limit else correction
        turn_limit = 50
        if correction > turn_limit:
            correction = turn_limit
        elif correction < -turn_limit:
            correction = -turn_limit

        self.set_point = correction
        drive = self.pid(self.turn_rate, dt) // 4  # Allows k parameters to be 4 times more
        self.power_direction = -1 if drive < 0 else 1
        self.power = min(abs(drive), 1000)

        if (abs(self.turn_rate) > 100 or abs(self.rudder_position) > 20) and\
                self.turn_direction == self.power_direction:
            self.power = 0
            self.integral = 0
        return self.power, self.power_direction

    def estimate_rudder_position(self, dt):
        self.rudder_position += self.power * self.power_direction * self.rudder_rate * dt / 1000

    @staticmethod
    def relative_direction(diff):
        if diff < -1800:
            diff += 3600
        elif diff > 1800:
            diff -= 3600
        return diff

    def pid(self, input_, dt):
        error = self.set_point - input_
        self.d_input = input_ - self._last_input

        proportional = self.kp * error

        # compute integral and derivative terms
        self.integral += int(self.ki * error * dt)

        derivative = int(-self.kd * self.d_input / dt)

        # compute final output
        output = proportional + self.integral + derivative

        print('pid:', output, 'params (p,d,i):', proportional, derivative, self.integral,
              'rudder:', self.rudder_position)

        # keep track of state
        self._last_input = input_

        return output