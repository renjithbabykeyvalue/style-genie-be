import json
import falcon


from src.models.models import UserMeasurement


class ImageGeneration(object):
    def on_post(self, req, resp):
        
        body = req.context['json']
        
        if body.get("prompt") is None:
            resp.status = falcon.HTTP_400
            resp_text = {
                'status': 'error',
                'message': 'Request body should contain either "measurements" or "image urls".'
            }
            return
        resp.status = falcon.HTTP_200
        resp.text = json.dumps({
            'status': 'ok'
        })
