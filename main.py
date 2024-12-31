from flask import Flask
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from flask_restx import Api

app = Flask(__name__)

api = Api(app,
    title='Sleep Tracker API',
    version='1.0',
    description='API para rastreamento de sono',
    doc='/swagger'
)

from app import *

if __name__ == '__main__':
    app.run(debug=True, port=2020, host='0.0.0.0')
