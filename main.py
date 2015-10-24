from cgi import parse_qs
from subprocess import Popen, PIPE
from tempfile import mkstemp
import os

def pandoc(m, hl=None):

    ret = False

    tf, tp = mkstemp(suffix=".pdf")
    try:
        cmd = ["pandoc", 
            "-t", "latex", 
            "-o", tp]
        if hl is not None:
            cmd.insert(1, "--highlight-style")
            cmd.insert(2, hl)

        p = Popen(cmd, stdin=PIPE)
        p.stdin.write(m)
        p.stdin.close()
        p.wait()
    except Exception, e:
        ret = e
    try:
        f = open(tp,'r')
        ret = f.read()
        f.close()
    except Exception, e:
        ret = e
    try:
        os.remove(tp)
    except Exception, e:
        ret = e
    
    if ret:
        raise Exception(ret)

    return ret


def set_cors(response_headers, environ):
    response_headers.append(('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'))
    response_headers.append(('Access-Control-Allow-Origin', '*'))
    ach = environ.get('HTTP_ACCESS_CONTROL_REQUEST_HEADERS', False)
    if ach:
        response_headers.append(('Access-Control-Allow-Headers', ach))

def app(environ, start_response):
    length = int(environ.get('CONTENT_LENGTH', '0'))
    body = environ['wsgi.input'].read(length)
    p = parse_qs(body)
    m = p.get("m")[0]
    hl = p.get("hl",[None])[0]
    title = p.get("t", ["article"])[0]

    try:
        pdf = pandoc(m, hl)
    except Exception, e:
        response_headers = [('Content-Type', 'text/plain')]
        set_cors(response_headers, environ)
        start_response('500 InternalServerError', response_headers)
        return [e.message]

    response_headers = [
        ('Content-Type', 'application/pdf'),
        ('Content-Disposition', 'attachment; filename="' + title + '.pdf"')
    ]
    set_cors(response_headers, environ)
    start_response('200 OK', response_headers)
    return [pdf]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, app)
    srv.serve_forever()
