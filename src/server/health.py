import json
import falcon


class Health(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.text = json.dumps({
            'status': 'ok'
        })
