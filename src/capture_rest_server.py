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
        my_mimerender = mimerender.FlaskMimeRender()
        render_xml = lambda message: '<message>%s</message>'%message
        render_json = lambda **args: json.dumps(args)
        render_html = lambda message: '<html><body>%s</body></html>'%message
        render_txt = lambda message: message
        app = Flask(__name__)
        try:
            app.run(host='0.0.0.0', port=80)
        except:
            pass

        @app.route('/bird', methods=['GET'])
        @mimerender(
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
            print 'here0'
            self.sharedqueue.put({
                'msg':'bird', \
                'msg_payload': \
                    {'confidence' : int(request.args['confidence'])} \
                    })
            return {'message': ' Bird confidence: ' + int(request.args['confidence'])}


# @app.route('/sequence', methods=['GET'])
# @mimerender(
#     default = 'html',
#     html = render_html,
#     xml  = render_xml,
#     json = render_json,
#     txt  = render_txt
# )
# def sequence():

#     '''
#     URL form: /sequence?id=N&intensity=O&tempo=P
#     '''

#     # TODO: Call a flash sequence

#     cmd = ArduinoCommand(int(request.args['id']), int(request.args['intensity']), int(request.args['tempo']))
#     cmd.execute()
#     return {'message': 'using sequence id ' + request.args['id']}

# if __name__ == "__main__":
#     __builtin__.arduino_ser = serial.Serial("/dev/ttyACM0",9600)
#     try:
#         app.run(host='0.0.0.0', port=80)
#     except:
#         pass