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
        self.rate = 1
        print(self.kp, self.ki, self.kd)
        # must be last statement
        self.loop_for_ever()

    def set_pid(self):
        self.kp = self.bd.kp.value
        self.ki = self.bd.ki.value
        self.kd = self.bd.kd.value
        self.pid = PID(self.kp, self.ki, self.kd, setpoint=0)
        self.pid.sample_time = None
        print(self.pid.Kp, self.pid.Ki, self.pid.Kd, self.pid.sample_time  )

    def loop_for_ever(self):
        read_at = monotonic()
        self.cts = last_heading = self.boat.heading
        self.bd.cts.value = self.cts
        self.set_pid()
        self.boat.update(1)

        while True:
            sleep(self.rate)
            self.cts = self.bd.cts.value
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

            # limit rate to 15 degrees per second
            if desired_rate > 150:
                desired_rate = 150
            elif desired_rate < -150:
                desired_rate = -150

            self.pid.setpoint = desired_rate
            last_heading = heading
            helm_adjust = self.pid(turn_rate)/self.bd.damping.value

            self.bd.dt.value = dt
            self.boat.helm_drive(helm_adjust)

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
