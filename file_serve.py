import mimetypes, os

def notFound(environ, start_response):
    start_response('404 Not Found', [
        ('Content-Type', 'text/plain')
    ])
    return ['Not Found']

def readFile(path, environ, start_response):
    (type, encoding) = mimetypes.guess_type(path)
    type = type if type else 'text/plain'
    content = open(path, 'rb').read()
    start_response('200 OK', [
        ('Content-Type', type),
        ('Content-Length', str(len(content))),
    ])
    return [content]

def getFile(environ, start_response):
    path = environ['PATH_INFO']
    path = path.rstrip('/')[1:]

    if path == '':
        path = 'index.html'

    path = os.path.join(__dir__, 'www', path)

    if os.path.exists(path):
        if os.path.isdir(path):
            path = os.path.join(path, 'index.html')
            if path.exists(path):
                return readFile(path, environ, start_response)
            else:
                return notFound(environ, start_response)
        else:
            return readFile(path, environ, start_response)
    else:
        return notFound(environ, start_response)