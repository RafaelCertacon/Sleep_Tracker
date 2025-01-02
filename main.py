import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from app import *


if __name__ == '__main__':
    app.run(debug=True, port=2020, host='0.0.0.0')
