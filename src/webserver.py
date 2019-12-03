from flask import Flask
from flask_restful import Resource, Api, reqparse

from webargs import fields, validate
from webargs.flaskparser import use_args, use_kwargs, parser, abort

from GlobalContext import GlobalContext

from threading import Thread

app = Flask(__name__)
api = Api(app)


class IndexResource(Resource):
    """A welcome page."""

    hello_args = {"name": fields.Str(missing="Friend")}

    @use_args(hello_args)
    def get(self, args):
        return {"message": "Welcome, {}!".format(args["name"])}


class RobotResource(Resource):
    add_args = {"angle": fields.Float(required=True)}

    def convert_angle(self, angle):
        # 0 -- 500
        # 90 -- 1500
        # 180 -- 2000
        return 1500 + angle / 180 * 2000

    @use_kwargs(add_args)
    def post(self, leg_id, link_id, angle):
        # Hack to make the mimic robot same as the real robot
        if link_id == 1 or link_id == 0:
            angle = -angle
        cmd = '"#%03dP%04dT0100!"' % (self.leg_link_map[leg_id][link_id], self.convert_angle(angle))
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


class RobotMoveResource(Resource):
    def get(self, action):
        if action == 'go':
            GlobalContext.getRobot().getController().robotGo()
        elif action == 'left':
            GlobalContext.getRobot().getController().robotLeft()
        elif action == 'right':
            GlobalContext.getRobot().getController().robotRight()
        elif action == 'stop':
            GlobalContext.getRobot().getController().robotStop()
        return "OK"


class RobotHeightResource(Resource):
    add_args = {"height": fields.Float(required=True)}

    def get(self):
        return GlobalContext.getRobot().getController().getLegHeight()

    @use_kwargs(add_args)
    def put(self, height):
        GlobalContext.getRobot().getController().setLegHeight(height)
        GlobalContext.getRobot().getController().robotStop()
        return "OK"


def robot_update_function():
    while True:
        GlobalContext.getRobot().getController().update()


if __name__ == "__main__":
    x = Thread(target=robot_update_function)
    x.start()

    api.add_resource(IndexResource, "/")
    api.add_resource(RobotResource, "/robot/legs/<int:leg_id>/links/<int:link_id>")
    api.add_resource(RobotMoveResource, "/robot/move/<string:action>")
    api.add_resource(RobotHeightResource, "/robot/height")
    app.run(port=5001, debug=True, host='0.0.0.0')
