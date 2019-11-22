from flask import Flask
from flask_restful import Resource, Api, reqparse

from webargs import fields, validate
from webargs.flaskparser import use_args, use_kwargs, parser, abort
import serial

app = Flask(__name__)
api = Api(app)

ser = serial.Serial(

    port='/dev/ttyAMA0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)


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

    leg_link_map = [[0, 1, 2],
                    [3, 4, 5],
                    [6, 7, 8],
                    [9, 10, 11],
                    [12, 13, 14],
                    [15, 16, 17]]

    add_args = {"angle": fields.Float(required=True)}

    def convert_angle(self, angle):
        # 0 -- 500
        # 90 -- 1500
        # 180 -- 2000
        return 500 + angle/180*2000

    @use_kwargs(add_args)
    def post(self, leg_id, link_id, angle):
        """An addition endpoint."""
        cmd = '"#%03dP0500T1000!"' % (self.leg_link_map[leg_id][link_id], self.conver_angle(angle))
        ser.write(cmd)
        return {"cmd": cmd}

    def get(self, leg_id, link_id):
        return {"leg": leg_id, "link": link_id, }

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
    ser.close()
