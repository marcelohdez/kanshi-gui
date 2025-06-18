# kanshi-gui

GTK4 + LibAdwaita application to create output configurations for Kanshi to use.

Ever wanted to connect to a TV or monitor to your window manager setup but did
not feel like setting it up in a config, or keeping it permanently in your
dotfiles? Same. So this is my attempted solution.

## Usage

> [!IMPORTANT]
> kanshi-gui will overwrite your regular kanshi config, and track state on its
> own in `kanshi-gui.json`. This means you must choose to either edit your
> kanshi config manually or use kanshi-gui. This may change in the future, but
> would be overly complex.

- Open this GUI.
- Create a new config by dragging things and pressing buttons for current outputs
- Apply

## Dependencies

You can probably install these using your distro package manager.

#### Programs <!-- markdownlint-disable MD001 -->

- [kanshi](https://gitlab.freedesktop.org/emersion/kanshi)
- [wlr-randr](https://gitlab.freedesktop.org/emersion/wlr-randr)

#### Libraries

- [PyGObject](https://pygobject.gnome.org/)
- [GTK4](https://www.gtk.org/) (+ devel)
- [LibAdwaita](https://gnome.pages.gitlab.gnome.org/libadwaita/) (+ devel)

## License

GPLv3. See [LICENSE](LICENSE).
