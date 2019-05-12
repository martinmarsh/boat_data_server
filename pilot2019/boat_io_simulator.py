from time import monotonic


class BoatModel:

    def __init__(self):
        self.calibration = 0
        self._power = 0
        self.compass = 0
        self.compass_correction = 0
        self.roll = 0
        self.pitch = 0
        self.run = 0

        self.helm = 0
        self.gain = 0.02
        self.momentum = 1
        self._direction = 1
        self.power_bias = 0
        self.last_read_at = monotonic()
        self.read_at = self.last_read_at

    def read_compass(self):
        self.read_at = monotonic()
        dt = self.read_at - self.last_read_at
        self.last_read_at = self.read_at
        self.helm += (self._power * self._direction + self.power_bias) * self.gain * dt

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

    def helm_drive(self, power, direction):
        """
        Drives the helm motor using PWM where 1,000,000 is
        full on
        :param power: +/- 1000 for full on
        :param direction: 1 for starboard -1 for port
        :return:
        """
        self._direction = direction
        self._power = power
        print(power * direction)

    def config_save(self):
        pass

    def config_delete(self):
        pass
