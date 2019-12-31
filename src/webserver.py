import sys
import time

from flask import Flask
from flask_restful import Resource, Api, reqparse

from webargs import fields, validate
from webargs.flaskparser import use_args, use_kwargs, parser, abort

from GlobalContext import GlobalContext

from threading import Thread
import socket

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


class LegHeightResource(Resource):
    add_args = {"height": fields.Float(required=True)}

    @use_kwargs(add_args)
    def put(self, leg_id, height):
        GlobalContext.getRobot().getController().setLegHeight(leg_id, height)
        return "OK"


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
        elif action == 'back':
            GlobalContext.getRobot().getController().robotBack()
        return "OK"


class RobotHeightResource(Resource):
    add_args = {"height": fields.Float(required=True)}

    def get(self):
        return GlobalContext.getRobot().getController().getLegHeight()

    @use_kwargs(add_args)
    def put(self, height):
        GlobalContext.getRobot().getController().setLegHeight(height)
        GlobalContext.getRobot().getController().robotStop()
        return "Current height:" + str(GlobalContext.getRobot().getController().getLegHeight())


class RobotStretchResource(Resource):
    add_args = {"stretch": fields.Float(required=True)}

    def get(self):
        return GlobalContext.getRobot().getController().getLegStretch()

    @use_kwargs(add_args)
    def put(self, stretch):
        GlobalContext.getRobot().getController().setLegStretch(stretch)
        GlobalContext.getRobot().getController().robotStop()
        return "Current stretch:" + str(GlobalContext.getRobot().getController().getLegStretch())


class CameraYawResource(Resource):
    add_args = {"degree": fields.Float(required=True)}

    @use_kwargs(add_args)
    def put(self, degree):
        GlobalContext.setCameraYaw(degree)


class CameraPitchResource(Resource):
    add_args = {"degree": fields.Float(required=True)}

    @use_kwargs(add_args)
    def put(self, degree):
        GlobalContext.setCameraPitch(degree)


def robot_update_function():
    print("Updating robot")
    while True:
        try:
            GlobalContext.getRobot().getController().update()
        except Exception as e:
            print("Oops!", sys.exc_info()[0], " occurred.")
            print("Exception is:", e)
    print("Main update thread stopped!!")


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def multicast_ip_function():
    import struct
    # get ip address
    ip_address = get_ip_address()
    print("Begin to multicast:" + ip_address)

    GROUP = "224.1.1.1"
    PORT = 6666

    # create socket, prepare to multicast
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.bind((ip_address, 0))

    ttl_bin = struct.pack('@i', 255)  # 255 is ttl
    s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl_bin)
    status = s.setsockopt(socket.IPPROTO_IP,
                          socket.IP_ADD_MEMBERSHIP,
                          socket.inet_aton(GROUP) + socket.inet_aton(ip_address))  # 加入到组播组

    if status != None:
        print("Add multicast group:" + status)

    while True:
        data = 'Robot:' + ip_address + ':' + '\r\n'
        s.sendto(data.encode(), (GROUP, PORT))
        print("send data:" + data + "OK")
        time.sleep(10)
        sys.stdout.flush()


# Broadcast this address


if __name__ == "__main__":
    x = Thread(target=robot_update_function)
    x.start()

    y = Thread(target=multicast_ip_function)
    print("Start multicast thread")
    y.start()

    api.add_resource(IndexResource, "/")
    api.add_resource(RobotResource, "/robot/legs/<int:leg_id>/links/<int:link_id>")
    api.add_resource(LegHeightResource, "/robot/legs/<int:leg_id>/height")
    api.add_resource(RobotMoveResource, "/robot/move/<string:action>")
    api.add_resource(RobotHeightResource, "/robot/height")
    api.add_resource(RobotStretchResource, "/robot/stretch")
    api.add_resource(CameraYawResource, "/camera/yaw")
    api.add_resource(CameraPitchResource, "/camera/pitch")
    app.run(port=5001, debug=True, host='0.0.0.0')
