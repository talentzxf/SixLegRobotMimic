class NavieControl:
    def __init__(self, links):
        self.links = links
        # self.links.getLink(0).setTheta(90)
        self.links.getLink(1).setTheta(90)
        self.links.getLink(2).setTheta(90)
        self.links.getLink(3).setTheta(90)

    def update(self):
        self.links.getLink(3).addTheta()