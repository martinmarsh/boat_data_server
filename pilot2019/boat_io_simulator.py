from time import monotonic, sleep
import math


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
        self.gain = 36
        self.speed = 12
        self._direction = 1
        self.rudder_angle = 0
        self.power_bias = 0
        self.rudder_rate = 1.2
        self.last_read_at = monotonic()
        self.read_at = self.last_read_at

    def read_compass(self):
        self.read_at = monotonic()
        dt = self.read_at - self.last_read_at
        self.last_read_at = self.read_at
        # rudder angle - wheel turns 360 degrees in either power_direction giving an rudder angle of about 30 degrees.
        # The helm gearing ratio is therefore 360/30 = 12
        # wheel turns at full motor speed 20 degrees per second ie 20*30/360 = 1.9 degrees of rudder per second
        # this gives 30/1.2 ie 25 seconds to full lock
        self.rudder_angle += ((self._power * self._direction + self.power_bias) / 1000 * dt * self.rudder_rate)
        # the pivotal force is related to the rudder angle and speed
        # to estimate this lets say at 6knots turning wheel 45 turns boat at 10 per second ie
        # 2.7 degrees of rudder is 0.047 so gain would be 10/0.047 = 212/6 = approx 36
        radians = math.radians(self.rudder_angle)
        force = math.sin(radians) * math.cos(radians)
        self.helm = force * self.gain * self.speed * dt

        self.compass += int(self.helm * dt * 10)   # *10 for deci degrees
        if self.compass > 3600:
            self.compass -= 3600
        elif self.compass < 0:
            self.compass += 3600
        print('angle', self.rudder_angle, 'force', force, 'helm', self.helm, 'compass', self.compass, 'dt', round(dt, 3))
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
        print("simulation mode - cannot save")
        sleep(2.0)

    def config_delete(self):
        print("simulation mode - cannot delete")
        sleep(2.0)

