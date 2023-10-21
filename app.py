from flask import Flask
from gevent.pywsgi import WSGIServer

app = Flask(__name__)


@app.route('/buyer-info')
@app.route('/buyer')
def index():
    return 'This is buyer\'s info'


if __name__ == "__main__":
    http_server = WSGIServer(('', 8080), app)
    http_server.serve_forever()
