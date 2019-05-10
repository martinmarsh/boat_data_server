from time import sleep, monotonic
from simple_pid import PID
from .model_simulator import BoatModel
# from .model import BoatModel


def relative_direction(diff):
    if diff < -1800:
        diff += 3600
    elif diff > 1800:
        diff -= 3600
    return diff


class Monitor:

    def __init__(self, bd):
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
        self.bd = bd
        self.boat = BoatModel()
        self.cts = -1
        self.pid = self.kp = self.ki = self.kd = None
        self.compass_sample_time = .25
        self.orientation_sample = 60   # 15 secs at .25
        self.auto_helm_sample = 4      # 15 secs at .25
        self.pitch_total = 0
        self.roll_total = 0
        self.compass_read_at = self.helm_last_read_at = self.compass_read_at = None
        self.heading = 0
        self.last_heading = 0

        print(self.kp, self.ki, self.kd)
        # must be last statement
        self.loop_for_ever()

    def set_pid(self):
        self.kp = self.bd.kp.value
        self.ki = self.bd.ki.value
        self.kd = self.bd.kd.value
        self.pid = PID(self.kp, self.ki, self.kd, setpoint=0)
        self.pid.sample_time = None
        print(self.pid.Kp, self.pid.Ki, self.pid.Kd, self.pid.sample_time)

    def auto_helm(self):
        dt = self.compass_read_at - self.helm_last_read_at
        self.helm_last_read_at = self.compass_read_at

        # min turn rate resolvable is 1 deci-degree per sec ie 1 degree per 10 seconds, max 1800 is physically unlikely
        turn_rate = relative_direction(self.heading - self.last_heading) / dt
        self.last_heading = self.heading

        error = relative_direction(self.cts - self.heading)

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
        helm_adjust = self.pid(turn_rate) / self.bd.damping.value

        print(abs_error)
        self.boat.helm_drive(helm_adjust)
        self.bd.turn_rate.value = int(turn_rate/10)
        self.bd.power.value = (self.boat.power * self.boat.helm_direction)

    def loop_for_ever(self):
        self.helm_last_read_at = self.compass_read_at = monotonic()
        self.last_heading = self.heading = self.boat.read_compass()
        self.set_pid()

        helm_count = 0
        orientation_count = 0

        while True:
            sleep(self.compass_sample_time)
            pitch = self.boat.read_pitch()
            roll = self.boat.read_roll()
            self.bd.pitch.value = pitch
            self.bd.roll.value = roll
            self.pitch_total += abs(pitch)
            self.roll_total += abs(roll)
            self.heading = self.boat.read_compass()
            self.compass_read_at = monotonic()
            self.bd.heading.value = self.heading/10
            self.cts = int(self.bd.cts.value * 10)
            self.bd.calibration.value = self.boat.calibration
            helm_count += 1
            orientation_count += 1
            if helm_count == self.auto_helm_sample:
                self.auto_helm()
                helm_count = 0
            if orientation_count == self.orientation_sample:
                self.bd.max_roll.value = int(self.roll_total/self.orientation_sample)
                self.roll_total = 0
                self.bd.max_pitch.value = int(self.pitch_total / self.orientation_sample)
                self.pitch_total = 0
                orientation_count = 0
