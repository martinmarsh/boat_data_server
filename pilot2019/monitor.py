from time import sleep, monotonic
from .model_simulator import BoatModel
from .helm_control import Helm
# from .model import BoatModel


class Monitor:

    def __init__(self, bd):

        self.bd = bd
        self.boat = BoatModel()
        self.helm = Helm()
        self.cts = -1
        self.compass_sample_time = .25
        self.orientation_sample = 60   # 15 secs at .25
        self.auto_helm_sample = 4      # 15 secs at .25
        self.pitch_total = 0
        self.roll_total = 0
        self.compass_read_at = self.helm_last_read_at = self.compass_read_at = None
        self.heading = 0
        self.last_heading = 0
        # must be last statement
        self.loop_for_ever()

    def helm_calibration(self):
        self.helm.set_pid(self.bd.kp.value, self.bd.ki.value, self.bd.kd.value, self.bd.gain.value)

    def auto_helm(self):
        dt = self.compass_read_at - self.helm_last_read_at
        self.helm_last_read_at = self.compass_read_at

        # Calculate drive factor and pass it to the boat steering helm drive
        drive = self.helm.get_drive(dt, self.heading, self.cts)
        self.boat.helm_drive(drive)

        self.bd.power.value = (self.boat.power * self.boat.helm_direction)

    def loop_for_ever(self):
        self.helm_last_read_at = self.compass_read_at = monotonic()
        self.last_heading = self.heading = self.boat.read_compass()
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
