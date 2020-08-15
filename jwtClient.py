import datetime
import jwt


class JwtClient:
    def __init__(self, SECRET_KEY, algorithm='HS256'):
        self.SECRET_KEY = SECRET_KEY
        self.algorithm = algorithm

    def encode(self, user_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                self.SECRET_KEY,
                self.algorithm
            )
        except Exception as e:
            return e

    def decode(self, token):
        try:
            payload = jwt.decode(token, self.SECRET_KEY)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
