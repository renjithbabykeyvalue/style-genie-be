import json
import falcon
from bson import json_util


from src.models.models import UserProfile
from src.services.body_measurement import get_body_measurements
from src.common.logger import get_logger

logger = get_logger(__name__)


class UserProfiles(object):
    def on_get(self, req, resp):
        id = req.get_param("id", default=None)
        query = {}
        if id:
            query["user"] = id
        userProfile = [userProfile.to_mongo()
                       for userProfile in UserProfile.objects(**query)]

        resp.status = falcon.HTTP_200
        resp.text = json.dumps({
            'status': 'ok',
            "measurement": json.loads(json_util.dumps(userProfile))
        })
