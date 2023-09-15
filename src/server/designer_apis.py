import json
import falcon
from bson import json_util

from src.models.models import Designer


class Designers(object):
    def on_get(self, req, resp):
        id = req.get_param("id", default=None)
        query = {}
        if id:
            query["id"] = id
        designer = [designer.to_mongo()
                    for designer in Designer.objects(**query)]
        resp.status = falcon.HTTP_200
        resp.text = json.dumps({
            'status': 'ok',
            "out": json.loads(json_util.dumps(designer))
        })
