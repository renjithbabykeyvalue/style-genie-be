import os

PLATFORM_ENV = os.environ.get('PLATFORM_ENV', 'development').lower()
TEST_MODE = PLATFORM_ENV == "test"

RABBIT_URL = os.environ.get('RABBIT_URL', 'amqp://guest:guest@localhost:5672?heartbeat=3600')
JWT_SECRET = os.environ.get('JWT_SECRET')
JWT_TOKEN = os.environ.get('JWT_TOKEN')
CALLBACK_RABBIT_URL = RABBIT_URL  # in case we want to change this in the future
EXCHANGE_NAME = os.environ.get('EXCHANGE_NAME', 'pencil_exchange')
