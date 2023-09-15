import json
import falcon
from bson import json_util
from src.services.generation.image_to_image import image_to_image


from src.models.models import UserProfile
from src.services.body_measurement import get_body_measurements
from src.common.logger import get_logger

logger = get_logger(__name__)


class UserCustomization(object):
    def on_get_customize(self, req, resp):
        id = "6504257f3914baa6e1a6e147"
        # id = req.params["id"]
        neckline = req.query["neckline"]
        if(neckline == "turtleneck"):
            prompt = '''Produce a full-length image of a mannequin wearing the provided dress, but with a distinct alteration: change the existing neckline to a turtleneck design. Maintain a well-lit scene with a dark gray background, position the mannequin at the center, standing upright with relaxed arms by its side. Pay close attention to the dress's original details, ensuring a perfect fit on the mannequin. Exclude any facial features from the mannequin, concentrating solely on showcasing the new turtleneck design, seamlessly integrated with the garment's existing style.'''
        elif(neckline == "u-neck"):
            prompt = '''Produce a full-length image of a mannequin wearing the provided dress, with a distinct alteration: create an attractive scoop neck design for the dress, giving it a stylish and flattering appearance. Maintain a well-lit scene with a dark gray background, position the mannequin at the center, standing upright with relaxed arms by its side. Pay close attention to the dress's original details, ensuring a perfect fit on the mannequin. Exclude any facial features from the mannequin, focusing solely on showcasing the new scoop neck design, seamlessly integrated with the garment's existing style.'''
        elif(neckline == "v-neck"):
            prompt = '''Generate a full-length image of a mannequin wearing the provided dress, but with a distinct alteration: change the existing neckline to a (v-neck). Maintain a well-lit scene with a dark gray background, position the mannequin at the center, standing upright with relaxed arms by its side. Pay close attention to the dress's original details, ensuring a perfect fit on the mannequin. Exclude any facial features from the mannequin, focusing solely on showcasing the new v-neck design, seamlessly integrated with the garment's existing style'''

        image_to_customize = f"https://style-genie.s3.ap-south-1.amazonaws.com/custom_image_{id}"
        customized_image_name = f"customized_image_{neckline}_{id}.png"
        customized_image = image_to_image(prompt=prompt, input_image_path=image_to_customize, s3_key=customized_image_name)

        resp.status = falcon.HTTP_200
        resp.text = json.dumps({
            'status': 'ok',
            "image_url": json.loads(json_util.dumps(customized_image))
        })