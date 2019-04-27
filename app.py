from flask import Flask
import flask_restful
from flask_restful import reqparse as flask_restful_reqparse
from flask_cors import CORS

import config, search_engine, build_team

app = Flask(__name__)
api = flask_restful.Api(app)

search_parser = flask_restful_reqparse.RequestParser()
search_parser.add_argument('searchterm')


class Search(flask_restful.Resource):
    def get(self):
        return "Error: please only send POST requests"

    def post(self):
        args = search_parser.parse_args()
        try:
            return search_engine.return_results(args.searchterm)
        except AssertionError as e:
            return str(e)


team_parser = flask_restful_reqparse.RequestParser()
team_parser.add_argument('budget')


class TeamBuilder(flask_restful.Resource):
    def get(self):
        return "Error: please only send POST requests"

    def post(self):
        args = team_parser.parse_args()
        try:
            return build_team.provide_team(int(args.budget))
        except Exception as e:
            print(str(e))


api.add_resource(Search, '/search')
api.add_resource(TeamBuilder, '/team-builder')

if __name__ == '__main__':
    app.run(
        host=config.flask_host,
        port=config.flask_port,
        debug=False
    )
