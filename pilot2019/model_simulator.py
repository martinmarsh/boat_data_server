from time import monotonic


class BoatModel:

    def __init__(self):
        self.calibration = 0
        self.power = 0
        self.compass = 0
        self.compass_correction = 0
        self.roll = 0
        self.pitch = 0
        self.run = 0

        self.helm = 0
        self.gain = 0.01
        self.momentum = 1
        self.helm_direction = 1
        self.power_bias = 0
        self.last_read_at = monotonic()
        self.read_at = self.last_read_at

    def read_compass(self):
        self.read_at = monotonic()
        dt = self.read_at - self.last_read_at
        self.last_read_at = self.read_at
        self.helm += (self.power * self.helm_direction + self.power_bias) * self.gain * dt

        self.compass += int(self.helm * dt * self.momentum)
        if self.compass > 3600:
            self.compass -= 3600
        elif self.compass < 0:
            self.compass += 3600
        # print(self.compass, round(dt, 3))
        return self.compass

    def read_pitch(self):
        return self.pitch

    def read_roll(self):
        return self.roll

    def update(self):
        self.read_compass()

    def helm_drive(self, helm_adjust):
        """
           Drives the helm motor using PWM where 1,000,000 is
           full on
           :param helm_adjust: +/- 1000 for full on
           :return:
           """

        self.helm_direction = 1 if helm_adjust > 0 else -1

        self.power = min(abs(helm_adjust), 1000)

        print(self.power * self.helm_direction)

    def config_save(self):
        pass

    def config_delete(self):
        pass
