from clearskies.input_outputs.input_output import InputOutput
import json
import base64
import urllib
class LambdaAPIGateway(InputOutput):
    _event = None
    _context = None
    _request_headers = None
    _request_method = None
    _path = None
    _resource = None
    _query_parameters = None
    _path_parameters = None
    _cached_body = None
    _body_was_cached = False

    def __init__(self, event, context):
        self._event = event
        self._context = context
        self._request_method = event.get('httpMethod', '').upper()
        self._path = event.get('path')
        self._resource = event.get('resource')
        self._query_parameters = event.get('queryStringParameters', {})
        self._path_parameters = event.get('pathParameters', {})
        self._request_headers = {}
        for (key, value) in event.get('headers', {}).items():
            self._request_headers[key.lower()] = value

    def respond(self, body, status_code=200):
        if not self.has_header('content-type'):
            self.set_header('content-type', 'application/json; charset=UTF-8')

        is_base64 = False
        if type(body) == bytes:
            is_base64 = True
            final_body = base64.encodebytes(body).decode('utf8')
        elif type(body) == str:
            final_body = body
        else:
            final_body = json.dumps(body)

        return {
            "isBase64Encoded": is_base64,
            "statusCode": status_code,
            "headers": self._response_headers,
            "body": final_body,
        }

    def has_body(self):
        return bool(self.get_body())

    def get_body(self):
        if not self._body_was_cached:
            self._cached_body = self._event.get('body')
            if self._cached_body is not None and self._event.get('isBase64Encoded'):
                self._cached_body = base64.decodebytes(self._cached_body.encode('utf-8')).decode('utf-8')
        return self._cached_body

    def get_request_method(self):
        return self._request_method

    def get_script_name(self):
        return ''

    def get_path_info(self):
        return self._path

    def get_query_string(self):
        return urllib.parse.urlencode(self._query_parameters)

    def get_content_type(self):
        return self.get_request_header('content-type', True)

    def get_protocol(self):
        return 'https'

    def has_request_header(self, header_name):
        return header_name.lower() in self._request_headers

    def get_request_header(self, header_name, silent=False):
        if not header_name.lower() in self._request_headers:
            if not silent:
                raise KeyError(f"HTTP header '{header_name}' was not found in request")
            return ''
        return self._request_headers[header_name.lower()]

    def get_query_parameter(self, key):
        return self._query_parameters[key] if key in self._query_parameters else []

    def get_query_parameters(self):
        return self._query_parameters

    def context_specifics(self):
        return {
            "event": self._event,
            "context": self._context,
        }

    def get_client_ip(self):
        # I haven't actually tested with an API gateway yet to figure out which of these works...
        sourceIp = self._event.get('requestContext', {}).get('identity', {}).get('sourceIp')
        if sourceIp:
            return sourceIp

        return self.get_request_header('x-forwarded-for', silent=True)
