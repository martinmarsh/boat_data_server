import falcon
from .resources import CalibrationResource, OrientationResource, SimulationResource
from .task import process_start
import os


class CORSComponent(object):

    def process_response(self, req, resp, resource, req_succeeded):
        resp.set_header('Access-Control-Allow-Origin', '*')

        if req_succeeded and req.method == 'OPTIONS' and req.get_header('Access-Control-Request-Method'):
            # NOTE(kgriffs): This is a CORS preflight request. Patch the
            #   response accordingly.

            allow = resp.get_header('Allow')
            resp.delete_header('Allow')

            allow_headers = req.get_header(
                'Access-Control-Request-Headers',
                default='*'
            )

            resp.set_headers((
                ('Access-Control-Allow-Methods', allow),
                ('Access-Control-Allow-Headers', allow_headers),
                ('Access-Control-Max-Age', '86400'),  # 24 hours
            ))


api = application = falcon.API(middleware=[CORSComponent()])

current_directory = os.getcwd()
print(current_directory)

calibration_resource = CalibrationResource()
orientation_resource = OrientationResource()
simulation_resource = SimulationResource()

api.add_route('/api/calibration', calibration_resource)
api.add_route('/api/orientation', orientation_resource)
api.add_route('/api/simulation', simulation_resource)
api.add_static_route('/', '{}/web/'.format(current_directory), fallback_filename='index.html')
api.add_static_route('/css', '{}/web/css/'.format(current_directory))
api.add_static_route('/media', '{}/web/media/'.format(current_directory))

os.environ['REACT_APP_THIS_HOST'] = "http://localhost"

process_start()



