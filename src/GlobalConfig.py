class RobotConfig:
    bodyLength = 1.6
    bodyWidth = 0.8
    bodyHeight = 0.5
    link1Length = 0.5
    link2Length = 0.75
    link3Length = 1.4

    defaultStretch = 2.0
    defaultLegHeight = -1.0
    defaultStepSize = 1.0

    # Only affect the view in simulator
    linkRadius = 0.1
    base_url = "http://176.122.187.37/robot/legs/{}/links/{}?angle={}"