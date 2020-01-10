from json import dumps

from assets.bottle import HTTPResponse
from helpers.SerializerHelper import serialize


def getHTTPResponse(code, content, to_encode=True):
    """Get an HTTP response """
    body = dumps(content, default=serialize) if to_encode else content
    return HTTPResponse(code=code, body=body)
