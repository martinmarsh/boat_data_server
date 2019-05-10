from simple_pid import PID


class Helm:

    def __init__(self):
        """
        example settings:   kp = Value('f', 1)
        ki = Value('f', 0.05)
         kd = Value('f', 0.5)
        damping = Value('i', 20)
        with simulation:
                 self.gain = 10
        self.momentum = 1
        self.helm_direction = 1
        self.power_bias = 0


        """
        self.cts = -1
        self.pid = self.kp = self.ki = self.kd = None
        self.compass_sample_time = .25
        self.compass_read_at = self.helm_last_read_at = self.compass_read_at = None
        self.heading = 0
        self.last_heading = 0
        self.damping = 10
        print(self.kp, self.ki, self.kd, self.damping)

    def set_pid(self, kp, ki, kd, damping):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.pid = PID(self.kp, self.ki, self.kd, setpoint=0)
        self.pid.sample_time = None
        self.damping = damping
        print(self.pid.Kp, self.pid.Ki, self.pid.Kd, self.pid.sample_time, self.damping)

    def get_drive(self, dt, heading, cts):
        self.heading = heading
        self.cts = cts

        # min turn rate resolvable is 1 deci-degree per sec ie 1 degree per 10 seconds, max 1800 is physically unlikely
        turn_rate = self.relative_direction(self.heading - self.last_heading) / dt
        self.last_heading = self.heading

        error = self.relative_direction(self.cts - self.heading)

        abs_error = abs(error)

        # for small errors less than 8 degrees ignore noisy turn rate and make desired rate same as error

        if abs_error > 600:
            turn_limit = 75
        else:
            turn_limit = 50

        if abs_error < 60:
            correction = int(error/2)
        else:

            # make correction the desired rate of turn in deci-degrees
            # A default settlement time of 4 seconds means that at 20 deg the max turn rate will start to reduce
            # at 12 degrees it will be 3 degrees per second
            # at 6 degrees error the settlement time is 3 degrees per seconds and the turn rate

            correction = int(error/5)

            # limit rate to 5 degrees per second
            if correction > turn_limit:
                correction = turn_limit
            elif correction < -turn_limit:
                correction = -turn_limit

        self.pid.setpoint = correction
        helm_adjust = self.pid(turn_rate) / self.damping

        return helm_adjust

    @staticmethod
    def relative_direction(diff):
        if diff < -1800:
            diff += 3600
        elif diff > 1800:
            diff -= 3600
        return diff
