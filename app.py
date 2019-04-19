from flask import Flask
import flask_restful
from flask_cors import CORS

import config, search_engine

app = Flask(__name__)
CORS(app)
api = flask_restful.Api(app)


class Search(flask_restful.Resource):
    def get(self):
        return search_engine.test()


api.add_resource(Search, '/search')

if __name__ == '__main__':
    app.run(
        host=config.flask_host,
        port=config.flask_port,
        debug=True
    )
