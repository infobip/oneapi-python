import logging as mod_logging
import SimpleHTTPServer as mod_simplehttpserver
import BaseHTTPServer as mod_basehttprequesthandler
import SocketServer as mod_socketserver
import time as mod_time
import threading as mod_threading

DEFAULT_PORT = 8000

class PushListenerHandler(mod_basehttprequesthandler.BaseHTTPRequestHandler):

    def do_GET(self):
        self.save_request('GET', self.path)
        self.write_ok()

    def do_POST(self):
        self.save_request('POST', self.path, body=self.read_body())
        self.write_ok()

    def do_DELETE(self):
        self.save_request('DELETE', self.path)
        self.write_ok()

    def do_PUT(self):
        self.save_request('PUT', self.path, body=self.read_body())
        self.write_ok()

    def write_ok(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write('ok')

    def read_body(self):
        try:
            length = int(self.headers.getheader('content-length'))
            return self.rfile.read(length)
        except Exception, e:
            mod_logging.exception(e)
            return None

    def save_request(self, http_method, path, body=None):
        print 'Request:'
        print '{0} {1}'.format(http_method, path)
        if body:
            print body
        print '------------------------------------------------------------------------------------------'
        self.server.saved_requests.append((http_method, path, body, ))

class DummyWebServer(mod_socketserver.TCPServer, mod_threading.Thread):
    """ This server may be used for http push events received from the API platform. """

    allow_reuse_address = True

    def __init__(self, port=None):
        self.port = port if port else DEFAULT_PORT

        mod_socketserver.TCPServer.__init__(self, ("", self.port), PushListenerHandler)
        mod_threading.Thread.__init__(self)

        self.saved_requests = []

    def reset_requests(self):
        self.saved_requests = []

    def run(self):
        self.serve_forever(poll_interval=0.5)

    def start_wait_and_shutdown(self, sleep):
        mod_logging.debug('Starting server on port {0}'.format(self.port))
        self.start()
        mod_logging.debug('Started server on port {0}, sleeping for {1}s'.format(self.port, sleep))
        mod_time.sleep(sleep)
        mod_logging.debug('Shutdown')
        self.shutdown()
        mod_logging.debug('Shutdown OK')

    def get_requests(self):
        return self.saved_requests

if __name__ == '__main__':
    mod_logging.basicConfig(level=mod_logging.DEBUG,
                            format = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

    dummy_web_server = DummyWebServer()

    dummy_web_server.start_wait_and_shutdown(5)

    print 'Saved requests:', dummy_web_server.get_requests()
