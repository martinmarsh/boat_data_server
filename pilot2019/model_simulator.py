

class BoatModel:

    def __init__(self):
        self.calibration = 0
        self.power = 0
        self.heading = 0
        self.head_correction = 0
        self.roll = 0
        self.pitch = 0
        self.run = 0
        self.dt = 0
        self.helm = 0
        self.gain = 200
        self.momentum = 1
        self.helm_direction = 1
        self.power_bias = 0

    def update(self, dt):
        self.dt = dt
        self.helm += (self.power * dt * self.helm_direction + self.power_bias) * self.gain
        print(self.helm, self.power * self.helm_direction)
        self.heading += int(self.helm * dt * self.momentum)
        if self.heading > 3600:
            self.heading -= 3600
        elif self.heading < 0:
            self.heading += 3600

    def helm_drive(self, helm_adjust):
        if helm_adjust < 0:
            self.helm_direction = -1
        elif helm_adjust > 0:
            self.helm_direction = 1

        self.power = abs(helm_adjust)
        if self.power > 0.99:
            self.power = 1

    def config_save(self):
        pass

    def config_delete(self):
        pass
