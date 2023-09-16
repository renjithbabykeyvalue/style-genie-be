import os

PLATFORM_ENV = os.environ.get('PLATFORM_ENV', 'development').lower()
TEST_MODE = PLATFORM_ENV == "test"

RABBIT_URL = os.environ.get(
    'RABBIT_URL', 'amqp://guest:guest@localhost:5672?heartbeat=3600')
JWT_SECRET = os.environ.get('JWT_SECRET')
JWT_TOKEN = os.environ.get('JWT_TOKEN')
CALLBACK_RABBIT_URL = RABBIT_URL  # in case we want to change this in the future
EXCHANGE_NAME = os.environ.get('EXCHANGE_NAME', 'pencil_exchange')
STABILITY_API_KEY = os.environ.get('STABILITY_API_KEY', 'API_KEY')
STUB_APIS = os.environ.get('STUB_APIS', 'true') == 'true'
STORAGE_PATH = os.environ.get('STORAGE_PATH', 'image_store')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
S3_BUCKET = os.environ.get('S3_BUCKET', "style-genie")
OPEN_AI_KEY = os.environ.get('OPEN_AI_KEY', "")
