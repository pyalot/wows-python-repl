import thread, traceback, sys
from wsgiref import simple_server
import wsgiref.simple_server

file_serve = mapi.require('file_serve')
run_code = mapi.require('run_code')

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

class RequestHandler(simple_server.WSGIRequestHandler):
    def address_string(self):
        return self.client_address[0]

    def log_request(*args, **kwargs):
        pass

def run():
    threadID = thread.get_ident()
    httpd = simple_server.make_server('', 2501, app, handler_class=RequestHandler)
    httpd.serve_forever()

thread.start_new_thread(run, ())