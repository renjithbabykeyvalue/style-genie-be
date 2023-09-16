import os
import falcon
from concurrent.futures import ThreadPoolExecutor
from falcon_marshmallow import Marshmallow
from pymongo import MongoClient
from src.server.health import Health
from src.server.outfits_apis import Outfits
from src.server.measurement_apis import Measurements
from src.server.designer_outfit_apis import DesignerOutfits
from src.server.user_customization_api import UserCustomization
from src.server.designer_apis import Designers
from src.server.scale_design import ScaleDesigns
from src.server.default_options_apis import DefaultOptions
from src.server.login_apis import Login
from src.server.user_profiles_api import UserProfiles
from src.server.jwt_middleware import DummyJWTMiddleware, JWTMiddleware
import mongoengine as mongo
from src.server.serve_images import ImageStore, Item
from src.config import STORAGE_PATH

import settings

jwt_secret = os.environ.get('JWT_SECRET')


def create_app(test_mode=False):

    image_store = ImageStore(STORAGE_PATH)
    if test_mode is False:
        _app = falcon.App(middleware=[
            # JWTMiddleware(jwt_secret),
            Marshmallow(),
            falcon.CORSMiddleware(allow_origins='*', allow_credentials='*'),
        ])
    else:
        _app = falcon.App(middleware=[
            # DummyJWTMiddleware(),
            Marshmallow(),
            falcon.CORSMiddleware(allow_origins='*', allow_credentials='*')
        ])

    global executor
    max_workers = os.environ.get('THREADPOOL_MAX_WORKERS', 2)
    workers = int(max_workers)
    executor = ThreadPoolExecutor(workers)

    _app.add_route('/api/health', Health())
    _app.add_route('/api/outfit', Outfits())
    _app.add_route('/api/user-measurement', Measurements())
    _app.add_route('/images/{name}', Item(image_store))
    _app.add_route('/api/designer', Designers())
    _app.add_route('/api/variations', ScaleDesigns())
    _app.add_route('/api/default-options', DefaultOptions())
    _app.add_route('/api/designer-outfits', DesignerOutfits())
    _app.add_route('/api/user-profiles', UserProfiles())
    _app.add_route('/api/user/customize/{id}', UserCustomization())
    _app.add_route('/api/designer/generate-from-text', Designers())
    _app.add_route('/api/login', Login())

    mongo.connect(
        host=settings.MONGO['HOST'],
        db=settings.MONGO['DATABASE']
    )

    return _app


app = create_app()
