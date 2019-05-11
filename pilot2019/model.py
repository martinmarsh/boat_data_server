from time import sleep
import pigpio


class BoatModel:

    def __init__(self):
        self._pi = pigpio.pi()
        self._pi.set_mode(23, pigpio.OUTPUT)
        self._pi.set_mode(24, pigpio.OUTPUT)
        self._cm = self._pi.i2c_open(1, 0x60)  # compass module CMPS12
        self.calibration = None
        self.power = 0
        self.compass = 0
        self.compass_correction = 0
        self.helm_direction = 1
        self.roll = 0
        self.pitch = 0
        self.run = 0

    def _port(self):
        self._pi.write(23, 0)
        if self.run:
            self._pi.write(24, 1)
        else:
            self._pi.write(24, 0)

    def _starboard(self):
        self._pi.write(24, 0)
        if self.run:
            self._pi.write(23, 1)
        else:
            self._pi.write(23, 0)

    def _read_signed_word(self, hi_reg, lo_reg):
        return int.from_bytes([
            self._pi.i2c_read_byte_data(self._cm, hi_reg),
            self._pi.i2c_read_byte_data(self._cm, lo_reg)
        ], byteorder='big', signed=True)

    def read_compass(self):
        # Read Compass in  deci-degrees
        self.compass = self._read_signed_word(2, 3) + self.compass_correction
        self.calibration = self._pi.i2c_read_byte_data(self._cm, 0x1E)

        if self.compass > 3600:
            self.compass -= 3600
        if self.compass < 0:
            self.compass += 3600
        return self.compass

    def read_pitch(self):
        self.pitch = self._pi.i2c_read_byte_data(self._cm, 4)
        return self.pitch

    def read_roll(self):
        self.roll = self._pi.i2c_read_byte_data(self._cm, 5)
        return self.pitch

    def _read_cmps_data(self):
        # Read Compass in  deci-degrees
        self.read_compass()
        self.read_pitch()
        self.read_roll()

        acc_x = self._read_signed_word(0x0C, 0x0D)
        acc_y = self._read_signed_word(0x0E, 0x0F)
        acc_z = self._read_signed_word(0x10, 0x11)

        gyo_x = self._read_signed_word(0x12, 0x13)
        gyo_y = self._read_signed_word(0x14, 0x15)
        gyo_z = self._read_signed_word(0x16, 0x17)

        mag_x = self._read_signed_word(0x06, 0x07)
        mag_y = self._read_signed_word(0x08, 0x09)
        mag_z = self._read_signed_word(0x0A, 0x0B)

        bosch_heading = self._read_signed_word(0x1A, 0x1B) / 16
        pitch_16 = self._read_signed_word(0x1C, 0x1D)

        temp = self._read_signed_word(0x18, 0x19)

        print("{} temp {} head {} {} roll {} pitch {} {}"
              "  acc {} {} {}  gyo {} {} {} mag {} {} {}".
              format(self.calibration, temp, self.compass, bosch_heading, self.roll, self.pitch, pitch_16,
                     acc_x, acc_y, acc_z,
                     gyo_x, gyo_y, gyo_z, mag_x, mag_y, mag_z
                     ))

    def update(self):
        self._read_cmps_data()

    def helm_drive(self, helm_adjust):
        """
        Drives the helm motor using PWM where 1,000,000 is
        full on
        :param helm_adjust: +/- 1000 for full on
        :return:
        """

        self.helm_direction = 1 if helm_adjust > 0 else -1
        if self.helm_direction > 1:
            self._starboard()
        else:
            self._port()

        self.power = min(abs(helm_adjust), 1000)

        # 5khz rate - pulse width is fraction of 1M
        self._pi.hardware_PWM(18, 5000, int(self.power * 1000))

    def config_save(self):
        self._pi.i2c_write_byte_data(self._cm, 0, 0xF0)
        sleep(.02)
        self._pi.i2c_write_byte_data(self._cm, 0, 0xF5)
        sleep(.02)
        self._pi.i2c_write_byte_data(self._cm, 0, 0xF6)
        sleep(.02)

    def config_delete(self):
        self._pi.i2c_write_byte_data(self._cm, 0, 0xE0)
        sleep(.02)
        self._pi.i2c_write_byte_data(self._cm, 0, 0xE5)
        sleep(.02)
        self._pi.i2c_write_byte_data(self._cm, 0, 0xE6)
        sleep(.02)
