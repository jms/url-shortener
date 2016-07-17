import json
from bottle import (
    route, default_app, get, request, response, redirect,
    static_file, jinja2_view, run
)
from shortener.data import DataHandle
from shortener.service import UrlShortener

conn = DataHandle()
service = UrlShortener()


def generate_short_url(real_url):
    redis = conn.r
    code = service.encode(conn.generate_url_id())
    exp_date = conn.get_expiration_date().isoformat()
    data = {
        'real_url': real_url,
        'expiration_date': exp_date
    }
    redis.set(code, json.dumps(data))
    return code


def resolver(hash_code):
    redis = conn.r
    # sanitize input, check for valid chars.
    valid_char_list = set(service.alphabet)
    input_code = set(hash_code)
    if all(c in valid_char_list for c in input_code):
        code = redis.get(hash_code)
        if code:
            data = json.loads(code)
            return data.get('real_url', None)


@route('/')
@jinja2_view('index.html')
def index():
    return {'title': 'url-shortener home page'}


@route('/process_url', method='POST')
def get_short_url():
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = request.json
        if data.get('long_url'):
            real_url = data.get('long_url')
            code = generate_short_url(real_url)
            response.headers['Content-Type'] = 'application/json'
            response.headers['Cache-Control'] = 'no-cache'
            return json.dumps({
                'code': code,
                'success': True
            })
    else:
        return 'No data received'


@route('/:hash_code')
@jinja2_view('error.html')
def resolve_url(hash_code):
    print hash_code
    real_url = resolver(hash_code)
    if real_url:
        redirect(real_url, 302)
    else:
        return {'title': '404'}


@route('/my_ip')
def show_ip():
    ip = request.environ.get('REMOTE_ADDR')
    server_name = request.get('SERVER_NAME')
    # or ip = request['REMOTE_ADDR']
    return "Your IP is: {}, server name is {}".format(ip, server_name)


# static files handle
@route('/images/<filename:re:.*\.png>')
def send_image(filename):
    return static_file(filename, root='/static/images', mimetype='image/png')


@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='static/js')


@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='static/css')


@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='static')


# application = default_app()
# run(host='localhost', port=8080, debug=True, server='waitress')
run(host='localhost', port=8080, debug=True, reloader=True)
