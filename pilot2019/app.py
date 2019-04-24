import falcon
from .boat_data_resource import Resource
from .task import process_start


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


boat_data_resource = Resource()
api.add_route('/boat_data', boat_data_resource)

process_start()



