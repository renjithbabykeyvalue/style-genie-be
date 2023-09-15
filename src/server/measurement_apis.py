import json
import falcon
from bson import json_util

from src.models.models import UserMeasurement, UserProfile
from src.services.body_measurement import get_body_measurements

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
        body = req.context['json']
        front_image = body.get("front_image")
        if front_image is None:
            resp.status = falcon.HTTP_400
            resp.text = json.dumps({
                'status': 'failed',
                'message': 'front_image is mandatory',
            })
            return
        measurements = get_body_measurements(front_image)
        resp.status = falcon.HTTP_200
        resp.text = json.dumps({
            'status': 'ok',
            'message': 'Obtained measurements.',
            'content': measurements
        })
