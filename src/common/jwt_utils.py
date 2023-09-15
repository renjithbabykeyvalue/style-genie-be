import jwt
from src.common.logger import get_logger

logger = get_logger()


def parse_jwt_token(jwt_token):
    try:
        payload = jwt.decode(f'{jwt_token}', verify=False)
        client_id = int(payload.get('clientId', 0))
        user_id = int(payload.get('id', 0))
        return user_id, client_id
    except Exception as e:
        logger.info(f"Token parsing Error :{e}")
        return None, None
