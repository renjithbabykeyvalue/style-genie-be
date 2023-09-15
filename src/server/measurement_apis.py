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

        resp.status = falcon.HTTP_200
        resp.text = json.dumps({
            'status': 'ok',
            "measurement": json.loads(json_util.dumps(measurement))
        })

    def on_post(self, req, resp):
        try:
            body = req.context['json']

            if 'measurements' in body:
                # Handle measurements
                measurements = body["measurements"]

                existing_measurements = UserMeasurement.objects(
                    userProfile=measurements["userProfile"])

                if existing_measurements:
                    existing_measurement = existing_measurements[0]

                    existing_measurement.chestSize = measurements["chestSize"]
                    existing_measurement.hipSize = measurements["hipSize"]
                    existing_measurement.waistSize = measurements["waistSize"]
                    existing_measurement.inseamLength = measurements["inseamLength"]
                    existing_measurement.save()
                else:
                    newMeasurement = UserMeasurement(
                        chestSize=measurements["chestSize"],
                        hipSize=measurements["hipSize"],
                        waistSize=measurements["waistSize"],
                        inseamLength=measurements["inseamLength"],
                        userProfile=measurements["userProfile"]
                    )
                    newMeasurement.save()

                resp_text = {
                    'status': 'ok',
                    'message': 'Measurement updated or created successfully.'
                }

            elif 'front_image_url' in body:
                front_image_url = body["front_image_url"]
                side_image_url = body["side_image_url"]
                resp_text = {
                    'status': 'ok',
                    'message': 'Image URL processed successfully.'
                }

            else:
                resp.status = falcon.HTTP_400
                resp_text = {
                    'status': 'error',
                    'message': 'Request body should contain either "measurements" or "image urls".'
                }

            resp.status = falcon.HTTP_200
            resp.text = json.dumps(resp_text)
        except Exception as ex:
            resp.status = falcon.HTTP_500
            resp.text = json.dumps({
                'status': 'error',
                'message': 'Internal server error.'
            })
