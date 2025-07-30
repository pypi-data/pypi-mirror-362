
from .Widget import * 
import urwid

class Table(Widget):
    
    def __init__(self, title, header, data, on_select, readonly=False):
        self.title = title
        self.header = header
        self.data = data 
        self.on_select = on_select
        self.readonly = readonly
    def getWidget(self):
        buttons = [] 
        def f(btn, x):
            i,j = x
            self.on_select(i,j)
        for i in range(len(self.data)):
            row=[]
            for j in range(len(self.header)):
                button = urwid.Button(self.data[i][j])
                if not self.readonly: 
                    urwid.connect_signal(button, "click", f, (i,j))
                row.append(button)
            buttons.append(urwid.Columns(row))
        return urwid.BoxAdapter(urwid.ListBox([
            urwid.Text(self.title),
            urwid.Columns([urwid.Text(x) for x in self.header]),
            *buttons
            ]), 24)
