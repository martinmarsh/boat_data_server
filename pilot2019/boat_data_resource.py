import json
import falcon
from .task import BoatData


class Resource:
    doc_in = None

    @staticmethod
    def get_doc():
        return {
            'course':
                {
                    'heading': BoatData.heading.value/10,
                    'cts': BoatData.cts.value/10,
                    'error': BoatData.error.value/10
                },
            'auto_helm':
                {
                    'power': BoatData.power.value,
                    'damping': BoatData.damping.value,
                    'kp': BoatData.kp.value,
                    'ki': BoatData.ki.value,
                    'kd': BoatData.kd.value,
                },
            'helm':
                {
                    'helm_adjust': BoatData.helm_adjust.value/10,
                    'desired_rate': BoatData.desired_rate.value/10,
                },
            'orientation':
                {
                    'pitch': BoatData.pitch.value,
                    'roll': BoatData.roll.value,
                    'turn_rate': BoatData.turn_rate.value/10,
                    'calibration': BoatData.calibration.value,
                    'dt': BoatData.dt.value
                }

        }

    def write_doc_section(self, section):
        sec_data = self.doc_in.get(section)
        if sec_data:
            for var, val in sec_data.items():
                attr = getattr(BoatData, var, None)
                if attr:
                    if var in ['cts', 'heading']:
                        attr.value = int(val * 10)
                    else:
                        attr.value = val

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
            self.write_doc_section('course')
            self.write_doc_section('auto_helm')

        doc = self.get_doc()
        # Create a JSON representation of the resource
        resp.body = json.dumps(doc, ensure_ascii=False)

        # The following line can be omitted because 200 is the default
        # status returned by the framework, but it is included here to
        # illustrate how this may be overridden as needed.
        resp.status = falcon.HTTP_201

