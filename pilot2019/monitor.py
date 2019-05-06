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
        self.bd = bd
        self.boat = BoatModel()
        self.cts = -1
        self.pid = self.kp = self.ki = self.kd = None
        self.compass_sample_time = .25
        self.auto_helm_sample = 4
        self.compass_read_at = self.helm_last_read_at = self.compass_read_at = None
        self.heading = 0
        self.last_heading = 0;

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

        # min turn rate is 1 deci-degree per sec ie 1 degree per 10 seconds, max 1800 is physically unlikely
        turn_rate = relative_direction(self.heading - self.last_heading) / dt

        self.last_heading = self.heading

        # set point is desired rate of turn in deci-degrees
        # try to correct an error in 3 second ie max  +/- 600
        # 1 degree = 3, -6 degrees = -20,  30 = 100
        desired_rate = int(relative_direction(self.cts - self.heading) / 3)

        # limit rate to 15 degrees per second
        if desired_rate > 150:
            desired_rate = 150
        elif desired_rate < -150:
            desired_rate = -150

        self.pid.setpoint = desired_rate

        helm_adjust = self.pid(turn_rate) / self.bd.damping.value

        self.bd.dt.value = dt
        self.boat.helm_drive(helm_adjust)

        self.bd.helm_adjust.value = helm_adjust
        self.bd.desired_rate.value = desired_rate
        self.bd.turn_rate.value = turn_rate
        self.bd.power.value = (self.boat.power * self.boat.helm_direction)

    def loop_for_ever(self):
        self.helm_last_read_at = self.compass_read_at = monotonic()
        self.last_heading = self.heading = self.boat.read_compass()
        self.set_pid()
        count = 0

        while True:
            sleep(self.compass_sample_time)
            self.heading = self.boat.read_compass()
            self.compass_read_at = monotonic()
            self.bd.heading.value = self.heading
            self.cts = self.bd.cts.value
            count += 1

            if count == self.auto_helm_sample:
                self.auto_helm()
                count = 0

                self.bd.roll.value = self.boat.read_roll()
                self.bd.pitch.value = self.boat.read_pitch()

                self.bd.calibration.value = self.boat.calibration
                self.bd.error.value = relative_direction(self.heading - self.cts)
