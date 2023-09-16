import json
import falcon
from bson import json_util
import openai
import src.config as config

from src.models.models import Outfit


def get_results(prompt):
    openai.api_key = config.OPEN_AI_KEY
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Given a prompt, you are a helpful assistant responsible for generating a comma separated values of keywords which are also lowercase and contain only commas between them, no trailing or prevailing spaces"},
            {"role": "user", "content": prompt}
        ]
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content


class OutfitsSearch(object):
    def on_get(self, req, resp, prompt):
        tags = get_results(prompt).split(',')
        outfits = [outfit.to_mongo()
                   for outfit in Outfit.objects(tags__in=tags)]
        print(outfits.__len__())
        resp.status = falcon.HTTP_200
        resp.text = json.dumps({
            'status': 'ok',
            "out": json.loads(json_util.dumps(outfits))
        })
