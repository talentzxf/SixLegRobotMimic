class RobotConfig:
    bodyLength = 1.9
    bodyWidth = 0.9
    bodyHeight = 0.25
    link1Length = 0.5
    link2Length = 0.5
    link3Length = 0.7

    # Add a static link4
    link2_3Angle_Y = -60
    link3_4Angle_Y = -60
    link4Length = 1.0

    defaultStretch = 1.5
    defaultLegHeight = -1.5
    defaultStepSize = 1.2

    # Only affect the view in simulator
    linkRadius = 0.1
    base_url = "http://176.122.187.37/robot/legs/{}/links/{}?angle={}"

    enable_serial = False
    enable_remote_rest = False

    camera_pitch_servo_id = 30
    camera_yaw_servo_id = 31
