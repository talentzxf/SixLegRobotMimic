from src.GlobalConfig import RobotConfig
from src.RobotControl.Leg import RoboLeg

if __name__ == '__main__':
    print("Running cases")
    leg = RoboLeg([RobotConfig.bodyWidth/2, RobotConfig.bodyHeight/2, 0], [[-135, 0.0, 0.0, 1.0], [-90, 0.0, 1.0, 0.0]])
    leg.add_link(0.1, [1.0, 0.0, 0.0])
    leg.add_link(0.2, [0.0, 1.0, 0.0])
    leg.add_link(0.3, [0.0, 1.0, 0.0])

    print("Leg end point:", leg.get_target_pos())

    # set world pos
    leg.set_end_pos([0.31213203435596426, 0.4621320343559643, -0.09999999999999999])
    print("Leg end pos:", leg.get_target_pos())
