import json
import falcon
from multiprocessing.pool import ThreadPool
from multiprocessing import cpu_count
from src.services.generation.image_to_image import image_to_image
import uuid
from src.utils.file_utils import download_file, get_extension_from_url
import tempfile

no_of_cpu = cpu_count()

def image_to_image_wrapper(args):
    prompt, input_path, s3_key = args
    return image_to_image(prompt, input_path, s3_key)

def scale_parallel(tasks):
    pool = ThreadPool(no_of_cpu - 1)
    results = pool.map(image_to_image_wrapper, tasks)
    pool.close()
    pool.join()
    print(f"completed scaling designs")
    return list(results)

class ScaleDesigns(object):
    def on_post(self, req, resp):  
        body = req.context['json']
        image_url = body.get("image_url")
        if image_url is None:
            resp.status = falcon.HTTP_400
            resptext = {
                'status': 'Bad Request',
                'message': 'Request body should contain either image_url.'
            }
            resp.text = json.dumps(resptext)
            return
        extension = get_extension_from_url(image_url)
        no_of_variations = body.get("no_of_variations", 3)
        _, out_filename = tempfile.mkstemp(extension)
        input_file_path = download_file(image_url, out_filename)
        prompt = "Can you suggest a diffrent fashion variation for this given dress."
        tasks = [(prompt, input_file_path, f"image_to_image/{str(uuid.uuid4())}.png") for i in range(no_of_variations)]
        variations = scale_parallel(tasks=tasks)
        resp.status = falcon.HTTP_200
        resp.text = json.dumps({
            'status': 'ok',
            'variations': variations
        })
