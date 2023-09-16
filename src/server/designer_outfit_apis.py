import json
import falcon
from bson import json_util
import openai
import src.config as config


from src.models.models import Outfit


def get_results(prompt):
    openai.api_key = config.OPEN_AI_KEY
    print(openai.api_key)
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Given a prompt, you are a helpful assistant responsible for generating a comma separated values of keywords which are also lowercase and contain only commas between them, no trailing or prevailing spaces"},
            {"role": "user", "content": prompt}
        ]
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content


class DesignerOutfits(object):
    def on_post(self, req, resp):
        try:
            body = req.context['json']
            tags = get_results(body['description']).split(',')
            input_array = [s.strip().lower() for s in tags]
            outfit = Outfit(
                name=body['name'],
                designer=body['designer'],
                default_price=body['default_price'],
                category=body['category'],
                description=body['description'],
                tags=input_array
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
