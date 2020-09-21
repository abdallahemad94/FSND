import json
from flask import request, session
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from os import environ as env


AUTH0_DOMAIN = env['AUTH0_DOMAIN']
ALGORITHMS = ['RS256']
API_AUDIENCE = env['API_AUDIENCE']

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header
def get_token_auth_header():
    authorization = request.headers.get("Authorization", None)
    if not authorization:
        raise AuthError({"code": "not_permitted",
                         "description": "no header is present"}, 401)
    parts = authorization.split(" ")
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        raise AuthError({"code": "not_permitted",
                         "description": "the header is malformed"}, 401)

    return authorization.split(" ")[1]


def check_permissions(permission, payload):
    if permission in payload.get('permissions', []):
        return True
    else:
        raise AuthError({"code": "not_permitted",
                         "description": "endpoint not permitted"}, 403)


def verify_decode_jwt(token):
    json_url = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(json_url.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    payload = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f"https://{AUTH0_DOMAIN}/"
            )
        except jwt.ExpiredSignatureError:
            raise AuthError({"code": "token_expired",
                             "description": "token is expired"}, 401)
        except jwt.JWTClaimsError:
            raise AuthError({"code": "invalid_claims",
                             "description":
                                 "incorrect claims,"
                                 "please check the audience and issuer"}, 401)
        except Exception:
            raise AuthError({"code": "invalid_header",
                             "description":
                                 "Unable to parse authentication"
                                 " token."}, 401)

    return payload


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if env['FLASK_ENV'] == 'testing':
                payload = {'permissions': env[f"{request.args.get('role')}_role_permissions"].split(',')}
                check_permissions(permission, payload)
                return f(*args, **kwargs)
            else:
                token = get_token_auth_header()
                payload = verify_decode_jwt(token)
                check_permissions(permission, payload)
                return f(*args, **kwargs)

        return wrapper

    return requires_auth_decorator


def get_permissions(token):
    payload = verify_decode_jwt(token)
    return payload.get('permissions', [])
