import thread, traceback
import wsgiref.simple_server

file_serve = require('file_serve')
run_code = require('run_code')

def app(environ, start_response):
    try:
        method = environ['REQUEST_METHOD'] 
        if method == 'GET':
            return file_serve.getFile(environ, start_response)
        elif method == 'POST':
            return run_code.evalInput(environ, start_response)
    except:
        start_response('500 Server Error', [
            ('Content-Type', 'text/plain')
        ])
        return [traceback.format_exc()]

def run():
    httpd = wsgiref.simple_server.make_server('', 2501, app)
    httpd.serve_forever()

thread.start_new_thread(run, ())
