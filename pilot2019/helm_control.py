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
        self.last_turn_direction = self.turn_direction = 1

    def set_tunings(self, kp, kd, ki, rudder_rate):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.rudder_rate = rudder_rate
        self._last_input = 0
        self.integral = 0
        print(self.kp,  self.kd,  self.ki, self.rudder_rate)

    def get_drive(self, dt, heading, cts):
        self.heading = heading
        self.cts = cts
        self.last_turn_direction = self.turn_direction
        # min turn rate resolvable is 1 deci-degree per sec ie 1 degree per 10 seconds, max 1800 is physically unlikely
        self.turn_rate = int(self.relative_direction(self.heading - self.last_heading) // dt)
        self.turn_direction = -1 if self.turn_rate < 0 else 1
        self.last_heading = self.heading

        self.error = self.relative_direction(self.heading - self.cts)

        # Power is proportional to wheel turning speed ignoring inefficiencies due to turning force varaitions and
        # increases in motor current to compensate.  Assume rudder angle is sum of "power"
        self.estimate_rudder_position(dt)

        # Required rudder is dependant on the compass error

        required_rudder = -self.error/40    # Error is in deci-degrees - 80 degree error ->  20 degree rudder

        required_rudder = 20 if required_rudder > 20 else -20 if required_rudder < -20 else required_rudder

        # ensure rudder estimate does not drift from zero by resetting origin when turn direction changes ie real
        # rudder passes through zero. However, don't do this if we have a large estimated direction as at zero
        # speed the rudder might  be driven too far.

        if self.last_turn_direction != self.turn_direction and self.rudder_position < 10:
            self.rudder_position = 0
        print("required", required_rudder, "actual", self.rudder_position)

        self.set_point = self.rudder_position
        drive = self.pd(required_rudder, dt)

        if abs(required_rudder) < 5:
            # compute integral from -input from zero allows pushing to zero when some compass error
            self.integral += int(self.ki * -required_rudder * dt)
            drive += self.integral
        else:
            self.integral = 0

        self.power_direction = -1 if drive > 0 else 1
        self.power = min(abs(drive), 1000)

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

    def pd(self, pd_input, dt):
        error = self.set_point - pd_input
        self.d_input = pd_input - self._last_input

        proportional = self.kp * error

        # compute derivative
        derivative = int(-self.kd * self.d_input / dt)

        # compute final output
        output = proportional + derivative

        print('pid:', output, 'params (p,d):', proportional, derivative,
              'rudder:', self.rudder_position)

        # keep track of state
        self._last_input = pd_input

        return output
