from flask import Flask
from flask import request
import __builtin__
import json
import mimerender
import time
from Queue import Queue

class CaptureRestServer():

    def __init__(self, sharedqueue):
        self.sharedqueue = sharedqueue

    def run(self):
        print 'Starting rest server'
        self.mimerender = mimerender.FlaskMimeRender()
        render_xml = lambda message: '<message>%s</message>'%message
        render_json = lambda **args: json.dumps(args)
        render_html = lambda message: '<html><body>%s</body></html>'%message
        render_txt = lambda message: message
        app = Flask(__name__)

        @app.route('/', methods=['GET'])
        @self.mimerender(
            default = 'html',
            html = render_html,
            xml  = render_xml,
            json = render_json,
            txt  = render_txt
        )
        def index():
            return {'message': 'Welcome to the Bird Photo Booth!'}

        @app.route('/bird', methods=['GET'])
        @self.mimerender(
            default = 'html',
            html = render_html,
            xml  = render_xml,
            json = render_json,
            txt  = render_txt
        )
        def bird():

            '''
            Takes URLS in form /bird?confidence=N
            '''
            self.sharedqueue.put({'bird':int(request.args['confidence'])})
            return {'message': 'Triggering bird camera with confidence: ' + \
                str(request.args['confidence']) + '%'}

        app.run(host='0.0.0.0', port=80)