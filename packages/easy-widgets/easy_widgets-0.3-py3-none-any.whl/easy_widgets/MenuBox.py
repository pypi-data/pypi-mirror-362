

from .Dialog import * 

class MenuBox(Dialog):
    
    def __init__(self, title):
        self.title = title
        self.options = []

    def addOption(self, description, func, params=[]):
        def f(b):
            self.exit()
            func(b, params)
        self.options.append((description, f, params))
    
    def getDialog(self):
        body = []
        for o in self.options:
            c, f, params = o
            button = urwid.Button(c)
            urwid.connect_signal(button, 'click', f)
            body.append(urwid.AttrMap(button, "button", focus_map='focus'))
        l = urwid.BoxAdapter(urwid.ListBox(urwid.SimpleFocusListWalker(body)), 5)
        return urwid.Pile([
            urwid.Text(self.title),
            urwid.Divider("-"),
            l,
        ])
