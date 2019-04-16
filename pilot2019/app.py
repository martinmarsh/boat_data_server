import falcon
from .boat_data_resource import Resource
from .task import process_start

api = application = falcon.API()

boat_data_resource = Resource()
api.add_route('/boat_data', boat_data_resource)

process_start()



