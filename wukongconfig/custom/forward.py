# -*- coding: utf-8-*-
from robot.sdk.AbstractPlugin import AbstractPlugin
import requests

class Plugin(AbstractPlugin):

    def handle(self, text, parsed):
        self.say('收到，小猪前进', cache=True)
        r = requests.get('http://127.0.0.1:5001/robot/move/go')

    def isValid(self, text, parsed):
        return "前进" in text