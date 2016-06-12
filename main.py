from bottle import (
    route, default_app, get, request, response,
    static_file, jinja2_view
)


@route('/')
@jinja2_view('index.html', template_lookup=['views'])
def index():
    return {'title': 'url-shortener test page'}


# static files handle
@route('/images/<filename:re:.*\.png>')
def send_image(filename):
    return static_file(filename, root='/static/images', mimetype='image/png')


@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='/static')


@get('/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='static/js')


@get('/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='static/css')


application = default_app()
# run(host='localhost', port=8080, debug=True)
