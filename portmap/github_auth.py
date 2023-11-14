#!/usr/bin/env python3
import jwt
import time
from django.conf import settings
import requests

def get_github_auth_token():
    headers = {"Authorization": f"Bearer {make_jwt_for_github()}"}
    response = requests.post("https://api.github.com/app/installations/43986164/access_tokens", headers=headers)
    return response.json()['token']

def make_jwt_for_github():
    signing_key = _get_github_private_key()
    return _construct_github_jwt(signing_key, settings.GITHUB_APP_ID)


def _get_github_private_key():
    if settings.GITHUB_PRIVATE_KEY_PEM_FILE:
        with open(settings.GITHUB_PRIVATE_KEY_PEM_FILE, 'rb') as pem_file:
            return jwt.jwk_from_pem(pem_file.read())
    elif settings.GITHUB_PRIVATE_KEY:
        return settings.GITHUB_PRIVATE_KEY


def _construct_github_jwt(signing_key, app_id):
    payload = {
        # Issued at time
        'iat': int(time.time()),
        # JWT expiration time (10 minutes maximum)
        'exp': int(time.time()) + 600,
        # GitHub App's identifier
        'iss': app_id
    }

    # Create JWT
    jwt_instance = jwt.JWT()
    encoded_jwt = jwt_instance.encode(payload, signing_key, alg='RS256')

    return encoded_jwt
