import gi
import lib as wd

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw  # noqa # type: ignore[import]


class WlrDisplays(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        win = MainWindow(application=app)
        win.present()


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = wd.get_current_state()

        self.connect("close-request", self.on_close_request)

        self.set_title("wlr-displays")
        self.root = Gtk.Box()
        self.set_child(self.root)

        self.hello = Gtk.Label(label=str(self.state))
        self.root.append(self.hello)

    def on_close_request(self, _):
        """Write state to disk"""
        config = wd.read_self_config() or wd.Config()

        # convert current state to a new profile
        profile = wd.Profile()
        for desc, tup in self.state.outputs.items():
            output, _ = tup
            profile.outputs[desc] = output

        config.profiles.add(profile)
        wd.write_configs_to_disk(config)
