
from .Application import *
import urwid


class Dialog():
    
    def exec(self):
        f = urwid.Filler(urwid.Padding(self.getDialog(), left=5, right=5))
        Application.setOverlay(urwid.AttrMap(f, "dialog"))

    def exit(self):
        Application.unsetOverlay()

    def getDialog(self):
        pass
