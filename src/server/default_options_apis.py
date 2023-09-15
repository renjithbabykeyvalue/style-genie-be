import json
import falcon
from bson import json_util

from src.models.models import DefaultOption


class DefaultOptions(object):
    def on_get(self, req, resp):
        id = req.get_param("id", default=None)
        query = {}
        if id:
            query["outfit"] = id
        defaultOptions = [defaultOption.to_mongo()
                          for defaultOption in DefaultOption.objects(**query)]
        print(defaultOptions.__len__())
        resp.status = falcon.HTTP_200
        resp.text = json.dumps({
            'status': 'ok',
            "out": json.loads(json_util.dumps(defaultOptions))
        })
