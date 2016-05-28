import logging
import os
import shutil
import tarfile
from cgi import FieldStorage
from subprocess import PIPE, Popen
from tempfile import mkdtemp, mkstemp


def pandoc(m, hl=None, tar=None, template=None):


    td = None
    if tar and template is None:
        raise Exception("tar given but no template name")
    if template and tar is None:
        raise Exception("template given but no tar")
    if tar.file:
        td = mkdtemp()
        os.chdir(td)
        tgz = tarfile.open(fileobj=tar.file, mode='r:gz')
        tgz.extractall('.')
        tgz.close()

    ret = False
    tf, tp = mkstemp(suffix=".pdf")
    try:
        cmd = ["pandoc", 
            "-t", "latex", 
            "-o", tp]
        if hl is not None:
            cmd.insert(1, "--highlight-style")
            cmd.insert(2, hl)
        if template:
            cmd.insert(1, "--template")
            cmd.insert(2, template)

        p = Popen(cmd, stdin=PIPE)
        p.stdin.write(m)
        p.stdin.close()
        p.wait()
        f = open(tp,'r')
        ret = f.read()
        f.close()
    except Exception, e:
        logging.exception(e)
        raise Exception(e)
    finally:
        if td:
            try:
                shutil.rmtree(td)
            except Exception as e:
                logging.exception(e)
        try:
            os.remove(tp)
        except:
            pass


    return ret

def set_cors(response_headers, environ):
    response_headers.append(('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'))
    response_headers.append(('Access-Control-Allow-Origin', '*'))
    ach = environ.get('HTTP_ACCESS_CONTROL_REQUEST_HEADERS', False)
    if ach:
        response_headers.append(('Access-Control-Allow-Headers', ach))

def app(environ, start_response):
    post = FieldStorage(
            fp = environ['wsgi.input'],
            environ = environ,
            keep_blank_values = True)

    # Get post vars
    m = post['m'] if 'm' in post else None
    if m is None:
        response_headers = [('Content-Type', 'text/plain')]
        set_cors(response_headers, environ)
        start_response('500 InternalServerError', response_headers)
        return ["You must provide content !"]

    if m.file:
        m = m.file.read()
    else:
        m = m.value

    hl = post['hl'].value if 'hl' in post else None
    title = post['t'].value if 't' in post else 'pandoc_generated'
    template = post['tpl'].value if 'tpl' in post else None
    tar = post['tar'] if 'tar' in post else None

    try:
        pdf = pandoc(m, hl, tar, template)
    except Exception, e:
        response_headers = [('Content-Type', 'text/plain')]
        set_cors(response_headers, environ)
        start_response('500 InternalServerError', response_headers)
        return ["Something went wrong...",e.message]

    response_headers = [
        ('Content-Type', 'application/pdf'),
        ('Content-Disposition', 'attachment; filename=' + title + '.pdf'),
        ('Content-Transfer-Encoding', 'binary')
    ]
    set_cors(response_headers, environ)
    start_response('200 OK', response_headers)
    return [pdf]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, app)
    logging.info("Listening 8080")
    srv.serve_forever()
