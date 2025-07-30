
from .Application import *

class Widget(object):

    def show(self):
        Application.setWidget(self.getWidget())

    def getWidget(self):
        pass
