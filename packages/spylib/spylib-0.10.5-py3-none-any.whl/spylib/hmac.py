from base64 import b64encode
from hashlib import sha256
from hmac import compare_digest, new


def calculate_from_message(secret: str, message: str, use_base64: bool = False) -> str:
    hmac_hash = new(secret.encode('utf-8'), message.encode('utf-8'), sha256)
    if use_base64:
        # TODO fix bytes / str union issue
        return b64encode(hmac_hash.digest()).decode('utf-8')

    return hmac_hash.hexdigest()


def calculate_from_components(
    datetime: str, path: str, query_string: str, body: str, secret: str, use_base64: bool = False
) -> str:
    if query_string != '':
        path = path + '?' + query_string
    message = path + datetime + body
    return calculate_from_message(secret=secret, message=message, use_base64=use_base64)


def validate(secret: str, sent_hmac: str, message: str, use_base64: bool = False):
    hmac_calculated = calculate_from_message(secret=secret, message=message, use_base64=use_base64)

    if not compare_digest(sent_hmac, hmac_calculated):
        raise ValueError('HMAC verification failed')
