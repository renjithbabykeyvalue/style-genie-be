import json
import falcon
from bson import json_util

from src.models.models import DefaultOption


class DesignerOutfitsCustomOptions(object):
    def on_post(self, req, resp):
        try:
            body = req.context['json']
            outfit = body['outfit']
            combinations = body.get('combinations', [])

            for combination in combinations:
                option = DefaultOption(
                    outfit=outfit,
                    fabric=combination.get('fabric', ''),
                    neckPattern=combination.get('neckPattern', ''),
                    sleevePattern=combination.get('sleevePattern', ''),
                    dyeable=combination.get('dyeable', '')
                )
                option.save()
            resp.status = falcon.HTTP_200
            resp.text = json.dumps({
                'status': 'ok',
            })
        except Exception as ex:
            resp.status = falcon.HTTP_500
            resp.text = json.dumps({
                'status': 'error',
                'message': 'Internal server error.'
            })
