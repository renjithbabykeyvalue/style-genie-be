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

    def on_post(self, req, resp):
        responses = []
        for i in range(1, 5):  # Loop four times to generate four images
            prompt = req.context['json']['prompt']
            generated_image_name = f"https://style-genie.s3.ap-south-1.amazonaws.com/designer_text_gen_design_{i}.png"
            customized_image = text_to_image(
                prompt=prompt, s3_key=generated_image_name)

            responses.append({
                "image_url": json.loads(json_util.dumps(customized_image))
            })

        resp.status = falcon.HTTP_200
        resp.text = json.dumps({
            'status': 'ok',
            'images': responses
        })
