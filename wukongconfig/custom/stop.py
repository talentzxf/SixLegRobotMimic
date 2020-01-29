# -*- coding: utf-8-*-
from robot.sdk.AbstractPlugin import AbstractPlugin
import requests

class Plugin(AbstractPlugin):

    def handle(self, text, parsed):
        self.say('收到，小猪停止', cache=True)
        r = requests.get('http://127.0.0.1:5001/robot/move/stop')

    def isValid(self, text, parsed):
        return "停止" in text