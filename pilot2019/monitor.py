from time import sleep, monotonic
from timeit import timeit
from .boat_io_simulator import BoatModel as SimulatedBoatModel
from .helm_control import Helm
from .boat_io import BoatModel


class Monitor:

    def __init__(self, bd):
        self.bd = bd
        self.boat = None
        self.simulator_on = False
        self.helm = Helm()
        self.compass_sample_time = .24955   # 0.25
        self.orientation_sample = 60   # 15 secs at .25
        self.auto_helm_sample = 4      # 1 secs at .25
        self.pitch_total = 0
        self.roll_total = 0
        self.compass_read_at = self.helm_last_read_at = self.compass_read_at = None
        self.heading = 0
        self.last_heading = 0
        self.last_cts = self.cts = -1
        self.last_kp = self.last_kd = self.last_ki = 0
        self.simulator_setup()

        # must be last statement
        self.loop_for_ever()

    def helm_calibration(self):
        self.last_kp = self.bd.kp.value
        self.last_kd = self.bd.kd.value
        self.last_ki = self.bd.ki.value
        self.helm.set_tunings(self.last_kp, self.last_kd, self.last_ki)

    def simulator_setup(self):
        self.simulator_on = self.bd.simulator_on.value
        if self.simulator_on:
            print("***on")
            self.bd.simulator_on.value = self.simulator_on = 1    # ensure both =1, value 2 means reset
            self.boat = SimulatedBoatModel()
            self.boat.gain = self.bd.simulator_gain.value
            self.boat.speed = self.bd.simulator_speed.value
            self.boat.power_bias = self.bd.simulator_power_bias.value
            self.boat.rudder_rate = self.bd.simulator_rudder_rate.value
            self.boat.compass = self.heading
        else:
            print("***off")
            self.bd.simulator_on.value = self.simulator_on = 0
            self.boat = BoatModel()

        self.helm_last_read_at = self.compass_read_at = monotonic()
        self.last_cts = self.cts = self.last_heading = self.heading = self.boat.read_compass()

    def auto_helm(self):
        dt = self.compass_read_at - self.helm_last_read_at
        self.helm_last_read_at = self.compass_read_at
        # Calculate drive factor and pass it to the boat steering helm drive
        power, direction = self.helm.get_drive(dt, self.heading, self.cts)
        self.boat.helm_drive(power, direction)
        self.bd.power.value = (power * direction)

    def loop_for_ever(self):
        self.helm_calibration()
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
            if self.cts != self.last_cts:
                power, direction = self.helm.fast_response_drive(self.heading, self.cts)
                self.boat.helm_drive(power, direction)
                self.last_cts = self.cts
            self.bd.calibration.value = self.boat.calibration
            helm_count += 1
            orientation_count += 1
            if self.last_kp != self.bd.kp.value or self.last_kd != self.bd.kd.value or self.last_ki != self.bd.ki.value:
                self.helm_calibration()
            if helm_count == self.auto_helm_sample:
                if self.bd.simulator_on.value != self.simulator_on:
                    self.simulator_setup()
                    # skip auto_helm until next iteration
                else:
                    self.auto_helm()
                helm_count = 0
            if orientation_count == self.orientation_sample:
                self.bd.max_roll.value = int(self.roll_total/self.orientation_sample)
                self.roll_total = 0
                self.bd.max_pitch.value = int(self.pitch_total / self.orientation_sample)
                self.pitch_total = 0
                orientation_count = 0
