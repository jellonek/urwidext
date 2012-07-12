import urwid
from twisted.internet import epollreactor
epollreactor.install()

from twisted.python import log
log.startLogging(open('/dev/null', 'w'), setStdout=False)

from widgets import CompletingEdit

class View(object):
    palette = [
        ('body', 'default', 'default'),
        ('edit', 'white', 'dark blue')
    ]

    # command name: command parameters completing function
    completing_dict = {
        'help': None,
        'quit': None,
        'hakumamatata': None,
        'tataramamama': None,
        'tatarasratara': None
    }

    def __init__(self):
        self.walker = urwid.SimpleListWalker([])
        self.listbox = urwid.ListBox(self.walker)
        self.edit = CompletingEdit(' > ', completing_dict=self.completing_dict)
        self.frame = urwid.Frame(self._wrap(self.listbox, 'body'),
            footer=self._wrap(self.edit, 'edit'), focus_part='footer')

    @staticmethod
    def _wrap(widget, attr_map):
        return urwid.AttrMap(widget, attr_map)

    def write(self, text):
        self.walker.append(urwid.Text(unicode(text)))
        self.walker.set_focus(len(self.walker.contents))


class TestApplication(object):
    def __init__(self):
        self.view = View()

    def run(self):
        self.loop = urwid.MainLoop(self.view.frame, self.view.palette,
                                   unhandled_input=self.handle_keys,
                                   event_loop=urwid.TwistedEventLoop(),
                                   handle_mouse=False)

        self.loop.run()

    def handle_keys(self, key):
        if key == 'enter':
            self.view.write(self.view.edit.edit_text)
            self.loop.draw_screen()
            if self.view.edit.edit_text.startswith('quit'):
                raise urwid.ExitMainLoop()
            self.view.edit.set_edit_text(u'')
        else:
            return
        return True

if __name__ == '__main__':
    app = TestApplication()
    app.run()
