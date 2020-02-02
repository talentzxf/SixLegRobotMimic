class RobotConfig:
    bodyLength = 2.23
    bodyWidth = 1.19
    bodyHeight = 0.25
    link1Length = 0.5
    link2Length = 0.55
    link2_arm_length = 0.16
    link2_arm_angle = -60
    link3Length = 0.72

    angle_min = -90
    angle_max = 90

    # Add a static link4
    link4Length = 0.72
    link3_4Angle_Y = -75

    defaultStretch = 1.3
    defaultLegHeight = -1.0

    # defaultStretch = 2.2082
    # defaultLegHeight = 0.0
    defaultStepSize = 0.8

    # Only affect the view in simulator
    linkRadius = 0.1
    base_url = "http://176.122.187.37/robot/legs/{}/links/{}?angle={}"

    enable_serial = True
    enable_remote_rest = False

    camera_pitch_servo_id = 22
    camera_yaw_servo_id = 23
