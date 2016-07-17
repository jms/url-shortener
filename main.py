import json
from bottle import (
    route, default_app, get, request, response,
    static_file, jinja2_view, run
)
from shortener.data import DataHandle
from shortener.service import UrlShortener

conn = DataHandle()
service = UrlShortener()


@route('/')
@jinja2_view('index.html')
def index():
    return {'title': 'url-shortener home page'}


@route('/', method='POST')
def get_short_url():
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = request.json
        if data.get('long_url'):
            real_url = data.get('long_url')
            code = service.generate_short_url(real_url)


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


@get('/semantic-ui/<filename:re:.*\.css>')
def vendor_stylesheets(filename):
    return static_file(filename, root='static/vendor/semantic-ui')


@get('/semantic-ui/<filename:re:.*\.js>')
def vendor_javascripts(filename):
    return static_file(filename, root='static/vendor/semantic-ui')


@get('/semantic-ui/themes/default/assets/fonts/<filename:re:.*\.woff2>')
@get('/semantic-ui/themes/default/assets/fonts/<filename:re:.*\.woff>')
@get('/semantic-ui/themes/default/assets/fonts/<filename:re:.*\.ttf>')
def vendor_fonts(filename):
    return static_file(filename, root='static/vendor/semantic-ui/themes/default/assets/fonts')


@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='static')


# application = default_app()
# run(host='localhost', port=8080, debug=True, server='waitress')
run(host='localhost', port=8080, debug=True, reloader=True)
