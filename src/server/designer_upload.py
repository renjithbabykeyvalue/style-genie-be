import json
import falcon


from src.models.models import UserMeasurement


class DesignerUpload(object):
    def on_post(self, req, resp):
        measurement = list(UserMeasurement.objects(
            id="6502df4ea76e28f8cfcbf360"))
        print(json.dumps(measurement))
        resp.status = falcon.HTTP_200
        resp.text = json.dumps({
            'status': 'ok'
        })
