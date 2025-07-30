
from .Dialog import * 

class MessageBox(Dialog):
    
    def __init__(self, title, text):
        self.title = title
        self.text = text

    def getDialog(self):
        return urwid.Pile([
            urwid.Text(self.title),
            urwid.Divider("-"),
            urwid.Text(self.text),
            urwid.AttrMap(urwid.Button("OK", lambda b: self.exit()), "button", "focus")
        ])
