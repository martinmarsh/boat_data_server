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
        self.kp = self.bd.kp.value
        self.ki = self.bd.kp.value
        self.kd = self.bd.kp.value
        self.pid = PID(self.kp, self.ki,  self.kd, setpoint=0)
        # must be last statement
        self.loop_for_ever()

    def loop_for_ever(self):
        self.pid.sample_time = 1.0  # update every 1.0 seconds
        read_at = monotonic()
        self.boat.update(1)
        self.cts = last_heading = self.boat.heading
        self.bd.cts.value = self.cts

        while True:
            sleep(self.pid.sample_time)
            self.cts = self.bd.cts.value
            self.pid.kp = self.bd.kp.value
            self.pid.ki = self.bd.ki.value
            self.pid.kd = self.bd.kd.value

            last_read_at = read_at
            read_at = monotonic()
            dt = read_at - last_read_at
            self.boat.update(dt)
            heading = self.boat.heading
            error = relative_direction(heading - self.cts)

            # min turn rate is 1 deci-degree per sec ie 1 degree per 10 seconds, max 1800 is physically unlikely
            turn_rate = relative_direction(heading - last_heading)/dt

            # set point is desired rate of turn in deci-degrees
            # try to correct an error in 3 second ie max  +/- 600
            # 1 degree = 3, -6 degrees = -20,  30 = 100
            desired_rate = int(relative_direction(self.cts - heading) / 3)

            # limit rate to 10 degrees per second
            if desired_rate > 100:
                desired_rate = 100
            elif desired_rate < -100:
                desired_rate = -100

            self.pid.setpoint = desired_rate
            last_heading = heading
            helm_adjust = self.pid(turn_rate)
            self.bd.dt.value = dt
            self.boat.helm_drive(helm_adjust, self.bd.damping.value)

            self.bd.heading.value = heading
            self.bd.roll.value = self.boat.roll
            self.bd.pitch.value = self.boat.pitch
            self.bd.helm_adjust.value = helm_adjust
            self.bd.desired_rate.value = desired_rate
            self.bd.turn_rate.value = turn_rate
            self.bd.power.value = (self.boat.power * self.boat.helm_direction)
            self.bd.dt.value = dt
            self.bd.calibration.value = self.boat.calibration
            self.bd.error.value = error
