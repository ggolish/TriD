
import sys
import tornado.web
import tornado.ioloop
import tornado.websocket

class TriDSocket(tornado.websocket.WebSocketHandler):

    def open(self):
        pass

    def on_close(self):
        pass

    def on_message(self, message):
        pass

def make_app():
    return tornado.web.Application([
        (r"/", TriDSocket)
    ])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: {} <port>\n".format(sys.argv[0]))
        sys.exit(1)
    port = int(sys.argv[1])
    app = make_app()
    try:
        app.listen(port)
        print("Listening on port {}".format(port))
    except:
        print("Failed to open connection on port {}".format(port))
    tornado.ioloop.IOLoop.current().start()
