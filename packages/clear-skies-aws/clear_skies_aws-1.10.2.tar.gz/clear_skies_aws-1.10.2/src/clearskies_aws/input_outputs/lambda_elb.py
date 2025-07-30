from .lambda_api_gateway import LambdaAPIGateway
class LambdaELB(LambdaAPIGateway):
    _event = None
    _context = None
    _request_headers = None
    _request_method = None
    _path = None
    _query_parameters = None

    def __init__(self, event, context):
        self._event = event
        self._context = context
        self._request_method = event.get('httpMethod', 'GET').upper()
        self._path = event.get('path', '/')
        self._query_parameters = event.get('queryStringParameters', {})
        self._request_headers = {}
        for (key, value) in event.get('headers', {}).items():
            self._request_headers[key.lower()] = value

    def get_client_ip(self):
        return self.get_request_header('x-forwarded-for')
