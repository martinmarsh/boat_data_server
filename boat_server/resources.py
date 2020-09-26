import json
import falcon
from boat_server.settings import R


helm_set = {
    "hts": 0,
    "gain": 0,
    "tsf": 0,
    "calibration": 0,
    "set_cal": 0,  # chip calibration:  0 = no action, 1 = unset, 2 = set
    "on": 0        # 0  stand by  1 on

}


def convert_list(keys, values):
    result = dict(zip(keys, values))
    for k, v in result.items():
        if v is not None:
            try:
                result[k] = int(v)
            except ValueError:
                try:
                    result[k] = float(v)
                except ValueError:
                    result[k] = v.decode()
    return result


class OrientationResource:

    @staticmethod
    def get_doc():

        get_items = ["compass", "compass_cal", "max_heal", "min_heal", "max_pitch", "min_pitch", "power", "rudder"]
        read_values = R.hmget('current_data', *get_items)
        data = convert_list(get_items, read_values)
        helm_set["calibration"] = data['compass_cal']

        return {
            'heading': data["compass"],
            'hts': helm_set["hts"],
            'calibration': data["compass_cal"],
            'pitch': max(abs(data["max_pitch"]), abs(data["min_pitch"])),
            'roll': (data["max_heal"] + data["min_heal"])/2,
            'power': data["power"],
            'rudder': data["rudder"]

        }

    def on_get(self, req, resp):
        doc = self.get_doc()
        # Create a JSON representation of the resource
        resp.body = json.dumps(doc, ensure_ascii=False)

    def on_post(self, req, resp):
        """Only cts will be updated via POST of course structure other values ignored
        """
        hts = req.media.get('hts', None)
        resp.status = falcon.HTTP_200
        if hts is not None:
            helm_set["hts"] = int(hts)
            R.hset('helm', 'hts',  helm_set["hts"] * 10)
            resp.status = falcon.HTTP_201

        doc = self.get_doc()
        # Create a JSON representation of the resource
        resp.body = json.dumps(doc, ensure_ascii=False)


class CalibrationResource:

    @staticmethod
    def get_doc():
        return {
            'kp': 0,
            'ki': 0,
            'kd': 0,
            "rudder_rate": 0,
            'set_cal':  helm_set["set_cal"],
            'calibration':  helm_set["calibration"],
        }

    def on_get(self, req, resp):
        doc = self.get_doc()
        # Create a JSON representation of the resource
        resp.body = json.dumps(doc, ensure_ascii=False)

    def on_post(self, req, resp):
        resp.status = falcon.HTTP_201
        for var, val in req.media.items():
            # check name for security
            if var in ['gain', 'tsf', 'set_cal']:
                helm_set[var] = int(val)
                R.hset('helm', var, helm_set[var])
                resp.status = falcon.HTTP_201
        doc = self.get_doc()
        # Create a JSON representation of the resource
        resp.body = json.dumps(doc, ensure_ascii=False)
