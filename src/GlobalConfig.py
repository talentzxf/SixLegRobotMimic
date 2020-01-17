class RobotConfig:
    bodyLength = 1.5
    bodyWidth = 0.75
    bodyHeight = 0.25
    link1Length = 0.3
    link2Length = 0.43
    link3Length = 0.9

    # Add a static link4
    # link4Length = 1.0
    link2_3Angle_Y = -90
    # link3_4Angle_Y = -60

    defaultStretch = 0.73
    defaultLegHeight = -0.9
    defaultStepSize = 0.3

    # Only affect the view in simulator
    linkRadius = 0.1
    base_url = "http://176.122.187.37/robot/legs/{}/links/{}?angle={}"

    enable_serial = True
    enable_remote_rest = False

    camera_pitch_servo_id = 22
    camera_yaw_servo_id = 23
