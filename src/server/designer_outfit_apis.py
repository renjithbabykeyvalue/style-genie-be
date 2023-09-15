import json
import falcon
from bson import json_util

from src.models.models import Outfit


class DesignerOutfits(object):
    def on_post(self, req, resp):
        try:
            body = req.context['json']

            outfit = Outfit(
                name=body['name'],
                designer=body['designer'],
                default_price=body['default_price'],
                category=body['category']
            )

            outfit_saved = outfit.save()
            outfit_id = str(outfit_saved.id)
            image_url = f'https://style-genie.s3.ap-south-1.amazonaws.com/outfits/{outfit_id}'

            Outfit.objects(id=outfit_saved.id).update_one(
                set__image_url=image_url)

            resp.status = falcon.HTTP_200
            resp.text = json.dumps({
                'status': 'ok',
                'image_url': image_url
            })
        except Exception as ex:
            resp.status = falcon.HTTP_500
            resp.text = json.dumps({
                'status': 'error',
                'message': 'Internal server error.'
            })