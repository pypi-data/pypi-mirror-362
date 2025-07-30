
from .Widget import *

class TextInput(Widget):
    
    def __init__(self, title, on_submit):
        self.title = title
        self.on_submit = on_submit 

    def getWidget(self):
        e = urwid.Edit("",align="center")
        l = [
            urwid.Text(self.title, align="center"),
            urwid.AttrMap(e, "", focus_map="focus"),
            urwid.Padding(urwid.AttrMap(urwid.Button("OK", self.__on_submit, e), "", focus_map="focus"), align="center", left=10, right=10)
        ]
        return urwid.Pile(l)

    def __on_submit(self, btn, edit):
        self.on_submit(edit.edit_text)
