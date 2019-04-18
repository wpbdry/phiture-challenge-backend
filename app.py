from flask import Flask
from flask_cors import CORS

import config
import search_engine

app = Flask(__name__)
CORS(app)
app.debug = True

app.add_url_rule(
    '/search',
    'search_engine',
    search_engine.test()
)

if __name__ == '__main__':
    app.run(
        host=config.flask_host,
        port=config.flask_port
    )
