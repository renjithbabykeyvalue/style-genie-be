import json
import falcon
from bson import json_util


class Login(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.text = json.dumps({
            'status': 'ok',
            "out": "6504ce459c8219dd7deb9afc"
        })
