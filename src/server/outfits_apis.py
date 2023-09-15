import json
import falcon
from bson import json_util

from src.models.models import Outfit


class Outfits(object):
    def on_get(self, req, resp):
        category = req.get_param("category", default=None)
        id = req.get_param("id", default=None)
        query = {}
        if category:
            query["category"] = category
        if id:
            query["id"] = id
        outfits = [outfit.to_mongo() for outfit in Outfit.objects(**query)]
        print(outfits.__len__())
        resp.status = falcon.HTTP_200
        resp.text = json.dumps({
            'status': 'ok',
            "out": json.loads(json_util.dumps(outfits))
        })
