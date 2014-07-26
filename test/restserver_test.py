from flask import Flask
from flask import request
import __builtin__
import json
import mimerender
import time

print 'Starting rest server'
mimerender = mimerender.FlaskMimeRender()
render_xml = lambda message: '<message>%s</message>'%message
render_json = lambda **args: json.dumps(args)
render_html = lambda message: '<html><body>%s</body></html>'%message
render_txt = lambda message: message
app = Flask(__name__)

@app.route('/', methods=['GET'])
@mimerender(
    default = 'html',
    html = render_html,
    xml  = render_xml,
    json = render_json,
    # txt  = render_txt
)
def index():
    print 'here0'
    return {'message': 'Hello world!'}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
