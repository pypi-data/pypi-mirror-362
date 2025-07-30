
from .Widget import * 

class Menu(Widget):
    
    def __init__(self, title):
        self.title = title
        self.options = []
    def addOption(self, description, func, color="button", params=[]):
        self.options.append((description, func, color, params))

    def getWidget(self):
        body = [urwid.Text(self.title), urwid.Divider()]
        for o in self.options:
            c, f, color, params = o
            button = urwid.Button(c)
            urwid.connect_signal(button, 'click', f, params)
            body.append(urwid.AttrMap(button, color, focus_map=color + "-reversed"))
        return urwid.Padding(urwid.BoxAdapter(urwid.ListBox(urwid.SimpleFocusListWalker(body)), 10), left=5, right=5)
        
