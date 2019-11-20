from flask import Flask
from flask_restful import Resource, Api, reqparse

from webargs import fields, validate
from webargs.flaskparser import use_args, use_kwargs, parser, abort

app = Flask(__name__)
api = Api(app)



class IndexResource(Resource):
    """A welcome page."""

    hello_args = {"name": fields.Str(missing="Friend")}

    @use_args(hello_args)
    def get(self, args):
        return {"message": "Welcome, {}!".format(args["name"])}


class RobotResource(Resource):
    leg_link_angle_map = {
      0: {0: 0, 1: 0, 2: 0},
      1: {0: 0, 1: 0, 2: 0},
      2: {0: 0, 1: 0, 2: 0},
      3: {0: 0, 1: 0, 2: 0},
      4: {0: 0, 1: 0, 2: 0},
      5: {0: 0, 1: 0, 2: 0}
    }

    add_args = {"angle": fields.Float(required=True)}

    @use_kwargs(add_args)
    def post(self, leg_id, link_id, angle):
        """An addition endpoint."""
        return {"result": "result:{},{},{}".format(leg_id, link_id, angle)}

    def get(self, leg_id, link_id):
        return {"leg":leg_id, "link": link_id,}

# This error handler is necessary for usage with Flask-RESTful
@parser.error_handler
def handle_request_parsing_error(err, req, schema, error_status_code, error_headers):
    """webargs error handler that uses Flask-RESTful's abort function to return
    a JSON error response to the client.
    """
    abort(error_status_code, errors=err.messages)


if __name__ == "__main__":
    api.add_resource(IndexResource, "/")
    api.add_resource(RobotResource, "/robot/legs/<int:leg_id>/links/<int:link_id>")
    app.run(port=5001, debug=True)
