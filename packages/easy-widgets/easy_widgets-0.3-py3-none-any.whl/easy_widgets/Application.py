
import urwid

widget = None

main = None



palette = [
    ('button', '', ''),
    ('focus', 'white', 'light blue'),
    ('button-reversed', 'white', 'light blue'),
    ("dialog", "black", "light gray"),
    ('bg', '', ''),
]
        
loop = None
parent = None

class Application(object):
    
    def init():
        global widget
        global parent
        global main
        global palette
        global loop
        widget = urwid.WidgetPlaceholder(None)
        main = urwid.Filler(urwid.Padding(widget, left=5, right=5))

        loop = urwid.MainLoop(main, palette)
        parent = None

    def run():
        loop.run()

    def addColor(name, fg, bg):
        palette.append((name, fg, bg))
        palette.append((name + "-reversed", bg, fg))

    def setWidget(w):
        widget.original_widget = w

    def exit():
       raise urwid.ExitMainLoop() 

    def getWidget():
        return widget

    def setOverlay(top):
        global main
        global parent
        parent = main
        main = urwid.Overlay(top, parent, align="center", valign="middle", width=50, height=15)
        loop.widget = main
        loop.draw_screen()

    def unsetOverlay():
        global main
        global parent
        main = parent
        loop.widget = main
