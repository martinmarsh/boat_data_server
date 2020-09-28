import json
import falcon
from boat_server.settings import R


class Data:

    helm_set = {
        "hts": 0,
        "gain": 0,
        "tsf": 0,
        "auto_mode": 0,  # 0 no action/done,  stand by  1 off,  2 on
        "calibration": 0,
        "set_cal": 0,  # chip calibration:  0 = no action/done, 1 = unset, 2 = set

    }

    boat_data = {}

    @classmethod
    def update_boat_data(cls):
        get_items = ["compass", "compass_cal", "max_heal", "min_heal", "max_pitch", "min_pitch", "power",
                     "rudder", "auto_helm"]
        read_values = R.hmget('current_data', *get_items)
        cls.boat_data = convert_list(get_items, read_values)
        cls.helm_set["calibration"] = cls.boat_data['compass_cal']


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
        return {
            'heading': Data.boat_data["compass"],
            'hts': Data.helm_set["hts"],
            'calibration': Data.boat_data["compass_cal"],
            'pitch': max(abs(Data.boat_data["max_pitch"]), abs(Data.boat_data["min_pitch"])),
            'roll': (Data.boat_data["max_heal"] + Data.boat_data["min_heal"])/2,
            'power': Data.boat_data["power"],
            'rudder': Data.boat_data["rudder"],
            'auto_helm': Data.boat_data["auto_helm"],

        }

    def on_get(self, req, resp):
        Data.update_boat_data()
        doc = self.get_doc()
        # Create a JSON representation of the resource
        resp.body = json.dumps(doc, ensure_ascii=False)

    def on_post(self, req, resp):
        """Only hts will be updated via POST
        returned doc is not updated to reduce overhead
        """
        hts = req.media.get('hts', None)
        auto_mode = req.media.get('auto_mode', None)

        resp.status = falcon.HTTP_200
        if hts is not None:
            Data.helm_set["hts"] = int(hts)
            R.hset('helm', 'hts',  Data.helm_set["hts"] * 10)
            resp.status = falcon.HTTP_201
        if auto_mode is not None:
            Data.helm_set["auto_mode"] = int(auto_mode)
            R.hset('helm', 'auto_mode', Data.helm_set["auto_mode"])
        doc = self.get_doc()
        # Create a JSON representation of the resource
        resp.body = json.dumps(doc, ensure_ascii=False)


class CalibrationResource:

    @staticmethod
    def get_doc():
        return {
            'gain': Data.helm_set["gain"],
            'tsf': Data.helm_set["tsf"],

            'set_cal':  Data.helm_set["set_cal"],
            'calibration':  Data.helm_set["calibration"],
        }

    def on_get(self, req, resp):
        doc = self.get_doc()
        # Create a JSON representation of the resource
        resp.body = json.dumps(doc, ensure_ascii=False)

    def on_post(self, req, resp):
        resp.status = falcon.HTTP_201
        for var, val in req.media.items():
            # check name for security
            if var in ['gain', 'tsf', 'set_cal', 'auto_mode'] and val is not None:
                Data.helm_set[var] = int(val)
                R.hset('helm', var, Data.helm_set[var])
                resp.status = falcon.HTTP_201
        doc = self.get_doc()
        # Although boat data is not used here it makes sense to update it when
        # we change calibration etc
        Data.update_boat_data()
        # Create a JSON representation of the resource
        resp.body = json.dumps(doc, ensure_ascii=False)


calibration_resource = CalibrationResource()
orientation_resource = OrientationResource()
