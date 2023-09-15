import json
import falcon
from bson import json_util
import base64


from src.models.models import UserMeasurement, UserProfile
from src.services.body_measurement import get_body_measurements
from src.common.logger import get_logger

logger = get_logger(__name__)


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

            user_profile = body["userProfile"]

            if 'measurements' in body:
                # Handle measurements
                measurements = body["measurements"]
            else:
                if body.get("front_image_url") is None:
                    resp.status = falcon.HTTP_400
                    resp_text = {
                        'status': 'error',
                        'message': 'Request body should contain either "measurements" or "image urls".'
                    }
                    return
                front_image_url = body["front_image_url"]
                measurements = get_body_measurements(front_image_url)

            existing_measurements = UserMeasurement.objects(
                userProfile=user_profile)

            measurement_obj = None
            if existing_measurements:
                measurement_obj = existing_measurements[0]

                measurement_obj.height = measurements["height"]
                measurement_obj.inseamLength = measurements["inseamLength"]
                measurement_obj.hipSize = measurements["hipSize"]
                measurement_obj.chestSize = measurements["chestSize"]
                measurement_obj.shoulder = measurements["shoulder"]

                measurement_obj.save()
            else:
                measurement_obj = UserMeasurement(
                    height=measurements["height"],
                    inseamLength=measurements["inseamLength"],
                    hipSize=measurements["hipSize"],
                    chestSize=measurements["chestSize"],
                    shoulder=measurements["shoulder"],
                    userProfile=user_profile
                )
                measurement_obj.save()

            resp_text = {
                'status': 'ok',
                'message': 'Measurement updated or created successfully.',
                "measurement": json.loads(json_util.dumps(measurement_obj.to_mongo()))
            }
            resp.status = falcon.HTTP_200
            resp.text = json.dumps(resp_text)
        except Exception as e:
            logger.error(f"Error getting measurements:{e}", exc_info=True)
            resp.status = falcon.HTTP_500
            resp.text = json.dumps({
                'status': 'error',
                'message': 'Internal server error.'
            })
