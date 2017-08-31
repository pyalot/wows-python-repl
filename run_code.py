import traceback, json, StringIO, contextlib, sys

namespace = {}

@contextlib.contextmanager
def stdoutCapture(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO.StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

def isStatement(code):
    try:
        compile(code, '<stdin>', 'eval')
        return False
    except SyntaxError:
        return True

def evalInput(environ, start_response):
    length = int(environ.get('CONTENT_LENGTH'))
    content = environ['wsgi.input'].read(length)
    content = json.loads(content)
    
    code = content['text']
    
    try:
        if isStatement(code):
            with stdoutCapture() as out:
                exec code in namespace
            out = out.getvalue()
            if out:
                reply = {'text':out}
            else:
                reply = {}
        else:
            with stdoutCapture() as out:
                value = str(eval(code, namespace, namespace))
            out = out.getvalue()
            reply = {'text':out+value}
    except:
        reply = {'text':traceback.format_exc(), 'isError':True}

    reply = json.dumps(reply)

    start_response('200 OK', [
        ('Content-Type', 'application/json'),
        ('Content-Length', str(len(reply)))
    ])
    return [reply]