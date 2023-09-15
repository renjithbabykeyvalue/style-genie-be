import json
import falcon
from bson import json_util
from src.services.generation.text_to_image import text_to_image

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

    def on_post_design_from_text(self, req, resp):
        id = "6504257f3914baa6e1a6e147"
        # id = req.params["id"]
        prompt = req.body["prompt"]
        generated_image_name = f"designer_text_gen_design_{id}.png"
        customized_image = text_to_image(prompt=prompt, s3_key=generated_image_name)

        resp.status = falcon.HTTP_200
        resp.text = json.dumps({
            'status': 'ok',
            "image_url": json.loads(json_util.dumps(customized_image))
        })
