import os
import falcon
from concurrent.futures import ThreadPoolExecutor
from falcon_marshmallow import Marshmallow
from pymongo import MongoClient
from src.server.health import Health
from src.server.jwt_middleware import DummyJWTMiddleware, JWTMiddleware
import mongoengine as mongo


jwt_secret = os.environ.get('JWT_SECRET')
mongodb_uri = 'mongodb+srv://style-genie:zsDbl2Npqiqd2inf@cluster0.ocf9ot0.mongodb.net/?retryWrites=true&w=majority'

client = MongoClient(mongodb_uri)
db = client.get_database(name="style-genie")

print(db["users"].count_documents(filter={}))


def create_app(test_mode=False):
    if test_mode is False:
        _app = falcon.App(middleware=[
            JWTMiddleware(jwt_secret),
            Marshmallow(),
            falcon.CORSMiddleware(allow_origins='*', allow_credentials='*')
        ])
    else:
        _app = falcon.App(middleware=[
            DummyJWTMiddleware(),
            Marshmallow(),
            falcon.CORSMiddleware(allow_origins='*', allow_credentials='*')
        ])

    global executor
    max_workers = os.environ.get('THREADPOOL_MAX_WORKERS', 2)
    workers = int(max_workers)
    executor = ThreadPoolExecutor(workers)

    _app.add_route('/api/health', Health())

    return _app


app = create_app()
