import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw  # noqa # type: ignore[import]


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_title("Kanshi GUI")
        self.root = Gtk.Box()
        self.set_child(self.root)

        self.hello = Gtk.Label(label="Hello, this is not ready yet")
        self.root.append(self.hello)


class KanshiGui(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        win = MainWindow(application=app)
        win.present()
