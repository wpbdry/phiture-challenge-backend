from flask import Flask
import flask_restful
from flask_restful import reqparse
from flask_cors import CORS

import config, search_engine

app = Flask(__name__)
CORS(app)
api = flask_restful.Api(app)

parser = reqparse.RequestParser()
parser.add_argument('searchterm')


class Search(flask_restful.Resource):
    def get(self):
        return "Error: please only send POST requests"

    def post(self):
        args = parser.parse_args()
        return search_engine.return_results(args.searchterm)


api.add_resource(Search, '/search')

if __name__ == '__main__':
    app.run(
        host=config.flask_host,
        port=config.flask_port,
        debug=True
    )
