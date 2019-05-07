import json
import falcon
from .task import BoatData


class FastResource:
    doc_in = None

    @staticmethod
    def get_doc():
        return {
            'orientation':
                {
                    'heading': round(BoatData.heading.value, 1),
                    'cts': BoatData.cts.value,
                    'calibration': BoatData.calibration.value,
                    'pitch': BoatData.pitch.value,
                    'roll': BoatData.roll.value,
                }
        }

    def on_get(self, req, resp):
        doc = self.get_doc()
        # Create a JSON representation of the resource
        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        """Only cts will be updated via POST of course structure other values ignored
        """
        self.doc_in = req.media
        sec_data = self.doc_in.get('course')
        cts = sec_data.get('cts', None)
        if cts is not None:
            attr = getattr(BoatData, 'cts', None)
            attr.value = int(cts)

        doc = self.get_doc()
        # Create a JSON representation of the resource
        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_201


class FullResource:
    doc_in = None

    @staticmethod
    def get_doc():
        return {
            'orientation':
                {
                    'heading':  round(BoatData.heading.value, 1),
                    'cts': BoatData.cts.value,
                    'calibration': BoatData.calibration.value,
                    'set_cal': BoatData.set_cal.value,
                    'pitch': BoatData.pitch.value,
                    'roll': BoatData.roll.value,
                    'max_pitch': BoatData.max_pitch.value,
                    'max_roll': BoatData.max_roll.value,
                    'turn_rate': BoatData.turn_rate.value,
                },
            'auto_helm':
                {
                    'power': BoatData.power.value,
                    'damping': BoatData.damping.value,
                    'kp': BoatData.kp.value,
                    'ki': BoatData.ki.value,
                    'kd': BoatData.kd.value,
                    'set_helm': BoatData.set_helm.value,
                },

        }

    def write_doc_section(self, section):
        sec_data = self.doc_in.get(section)
        if sec_data:
            for var, val in sec_data.items():
                attr = getattr(BoatData, var, None)
                if attr:
                    if var in ['kp', 'ki', 'kd']:
                        attr.value = float(val)
                    elif var in ['damping', 'set_cal', 'set_helm', 'cts']:
                        attr.value = int(val)

    def on_get(self, req, resp):

        doc = self.get_doc()

        # Create a JSON representation of the resource
        resp.body = json.dumps(doc, ensure_ascii=False)

        # The following line can be omitted because 200 is the default
        # status returned by the framework, but it is included here to
        # illustrate how this may be overridden as needed.
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):

        self.doc_in = req.media
        if 0 < req.content_length < 10000:
            # self.doc_in = json.load(req.stream)
            self.write_doc_section('orientation')
            self.write_doc_section('auto_helm')

        doc = self.get_doc()
        # Create a JSON representation of the resource
        resp.body = json.dumps(doc, ensure_ascii=False)

        # The following line can be omitted because 200 is the default
        # status returned by the framework, but it is included here to
        # illustrate how this may be overridden as needed.
        resp.status = falcon.HTTP_201
