import json
import falcon
from .task import BoatData


class OrientationResource:

    @staticmethod
    def get_doc():
        return {
            'heading': round(BoatData.heading.value, 1),
            'cts': BoatData.cts.value,
            'calibration': BoatData.calibration.value,
            'pitch': BoatData.pitch.value,
            'roll': BoatData.roll.value,
            'power': BoatData.power.value,
            'rudder': round(BoatData.rudder.value, 1),

        }

    def on_get(self, req, resp):
        doc = self.get_doc()
        # Create a JSON representation of the resource
        resp.body = json.dumps(doc, ensure_ascii=False)

    def on_post(self, req, resp):
        """Only cts will be updated via POST of course structure other values ignored
        """
        cts = req.media.get('cts', None)
        resp.status = falcon.HTTP_200
        if cts is not None:
            attr = getattr(BoatData, 'cts', None)
            attr.value = int(cts)
            resp.status = falcon.HTTP_201

        doc = self.get_doc()
        # Create a JSON representation of the resource
        resp.body = json.dumps(doc, ensure_ascii=False)


class SimulationResource:

    @staticmethod
    def get_doc():
        return {
            "on": BoatData.simulator_on.value,
            "gain": BoatData.simulator_gain.value,
            "speed": BoatData.simulator_speed.value,
            "power_bias": BoatData.simulator_power_bias.value,
        }

    def on_get(self, req, resp):
        doc = self.get_doc()
        # Create a JSON representation of the resource
        resp.body = json.dumps(doc, ensure_ascii=False)

    def on_post(self, req, resp):
        resp.status = falcon.HTTP_201
        for var, val in req.media.items():
            var = 'simulator_{}'.format(var)
            attr = getattr(BoatData, var, None)
            if var in ["simulator_rudder_rate", "simulator_speed"]:
                attr.value = float(val)
            else:
                attr.value = int(val)
                print("v", var, attr.value)
            resp.status = falcon.HTTP_201
        doc = self.get_doc()
        # Create a JSON representation of the resource
        resp.body = json.dumps(doc, ensure_ascii=False)


class CalibrationResource:

    @staticmethod
    def get_doc():
        return {
            'kp': BoatData.kp.value,
            'ki': BoatData.ki.value,
            'kd': BoatData.kd.value,
            "rudder_rate": round(BoatData.rudder_rate.value, 3),
            'set_cal': BoatData.set_cal.value,
            'calibration': BoatData.calibration.value,
        }

    def on_get(self, req, resp):
        doc = self.get_doc()
        # Create a JSON representation of the resource
        resp.body = json.dumps(doc, ensure_ascii=False)

    def on_post(self, req, resp):
        resp.status = falcon.HTTP_201
        for var, val in req.media.items():
            # check name for security
            attr = getattr(BoatData, var, None)
            if var == "rudder_rate":
                attr.value = float(val)
            elif var in ['kp', 'ki', 'kd', 'set_cal']:
                attr.value = int(val)
                resp.status = falcon.HTTP_201
        doc = self.get_doc()
        # Create a JSON representation of the resource
        resp.body = json.dumps(doc, ensure_ascii=False)
