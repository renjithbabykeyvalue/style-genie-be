import json
import falcon
from bson import json_util
import base64


from src.models.models import UserMeasurement, UserProfile


class Measurements(object):
    def on_get(self, req, resp):
        id = req.get_param("id", default=None)
        query = {}
        if id:
            query["userProfile"] = id
        measurement = [measurement.to_mongo()
                       for measurement in UserMeasurement.objects(**query)]

        print(measurement.__len__())
        resp.status = falcon.HTTP_200
        resp.text = json.dumps({
            'status': 'ok',
            "measurement": json.loads(json_util.dumps(measurement))
        })

    def on_post(self, req, resp):
        print(req)
        print(req.stream.read().decode('utf-8'))
        resp.status = falcon.HTTP_200
        resp.text = json.dumps({
            'status': 'ok',
            'message': 'Images uploaded successfully.'
        })
