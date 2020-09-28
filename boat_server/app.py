import falcon
from .resources import calibration_resource, orientation_resource
from subprocess import Popen, PIPE
import os
import json


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


api.add_route('/api/calibration', calibration_resource)
api.add_route('/api/orientation', orientation_resource)

api.add_static_route('/', '{}/web/'.format(current_directory), fallback_filename='index.html')
api.add_static_route('/css', '{}/web/css/'.format(current_directory))
api.add_static_route('/media', '{}/web/media/'.format(current_directory))


ip = None
try:
    p = Popen(['ifconfig'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    op, err = p.communicate()
    rc = p.returncode
    if rc == 0:
        op = str(op)
        p = op.find('192.')
        p2 = op.find(' ', p)
        ip = op[p:p2]
        config = {
            "host": "http://{}:8079".format(ip)
        }

        with open('./web/config.json', 'w') as outfile:
            json.dump(config, outfile)

except (OSError, AttributeError):
    pass





