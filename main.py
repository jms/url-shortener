import json
import falcon
import logging
from shortener.data import DataHandle
from shortener.service import UrlShortener


def max_body(limit):
    def hook(req, resp, resource, params):
        length = req.content_length
        if length is not None and length > limit:
            msg = 'The size of the request is too large. ' \
                  'The body must not exceed {} bytes in length.'.format(limit)

            raise falcon.HTTPRequestEntityTooLarge('Request body is too large', msg)

    return hook


class RequireJSON(object):
    def process_request(self, req, resp):
        if not req.client_accepts_json:
            raise falcon.HTTPNotAcceptable(
                'This API only supports responses encoded as JSON.',
                href='http://docs.examples.com/api/json')

        if req.method in ('POST'):
            if 'application/json' not in req.content_type:
                raise falcon.HTTPUnsupportedMediaType(
                    'This API only supports requests encoded as JSON.',
                    href='http://docs.examples.com/api/json')


class JSONTranslator(object):
    def process_request(self, req, resp):
        # req.stream corresponds to the WSGI wsgi.input environ variable,
        # and allows you to read bytes from the request body.
        #
        # See also: PEP 3333
        if req.content_length in (None, 0):
            # Nothing to do
            return

        body = req.stream.read()
        if not body:
            raise falcon.HTTPBadRequest('Empty request body', 'A valid JSON document is required.')

        try:
            req.context['doc'] = json.loads(body.decode('utf-8'))

        except (ValueError, UnicodeDecodeError):
            raise falcon.HTTPError(falcon.HTTP_753,
                                   'Malformed JSON',
                                   'Could not decode the request body. The '
                                   'JSON was incorrect or not encoded as '
                                   'UTF-8.')

    def process_response(self, req, resp, resource):
        if 'result' not in req.context:
            return

        resp.body = json.dumps(req.context['result'])


class ShortUrl(object):
    def __init__(self):
        self.logger = logging.getLogger('UrlResource.{}'.format(__name__))
        self.conn = DataHandle()
        self.service = UrlShortener()

    @falcon.before(max_body(64 * 1024))
    def on_get(self, req, resp):
        context_data = req.context.get('doc', {})
        code = context_data.get('code', None)
        data = self.resolver(code)
        req.context['result'] = data
        resp.content_type = "application/json"
        resp.set_header('X-Powered-By', 'jms-url-shortener')
        resp.status = falcon.HTTP_200

    @falcon.before(max_body(64 * 1024))
    def on_post(self, req, resp):
        try:
            doc = req.context['doc']
        except KeyError:
            raise falcon.HTTPBadRequest(
                'Missing thing',
                'A thing must be submitted in the request body.')

        real_url = doc.get('url', None)
        if real_url:
            code = self.generate_short_url(real_url)
            resp.body = 'http://localhost:8000/lnk/{}'.format(code)
            resp.status = falcon.HTTP_201
        else:
            resp.status = falcon.HTTP_400

    def resolver(self, hash_code):
        redis = self.conn.r
        # sanitize input, check for valid chars.
        valid_char_list = set(self.service.alphabet)
        input_code = set(hash_code)
        if all(c in valid_char_list for c in input_code):
            code = redis.get(hash_code)
            if code:
                data = json.loads(code)
                return data.get('real_url', None)  # default 302
            else:
                return 'Not url found'  # 404
        else:
            return 'Invalid code'  # 400

    def generate_short_url(self, real_url):
        redis = self.conn.r
        code = self.service.encode(self.conn.generate_url_id())
        exp_date = self.conn.get_expiration_date().isoformat()
        data = {
            'real_url': real_url,
            'expiration_date': exp_date
        }
        redis.set(code, json.dumps(data))
        return code


# falcon.API instances are callable WSGI apps
app = falcon.API(middleware=[
    RequireJSON(),
    JSONTranslator()
])
short_url = ShortUrl()
app.add_route('/lnk', short_url)

from wsgiref import simple_server

if __name__ == '__main__':
    httpd = simple_server.make_server('0.0.0.0', 8000, app)
    httpd.serve_forever()
