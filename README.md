# kanshi-gui

GTK4 + LibAdwaita application to create output configurations for Kanshi to use.

Ever wanted to connect to a TV or monitor to your window manager setup but did
not feel like setting it up in a config, or keeping it permanently in your
dotfiles? Same. So this is my attempted solution.

## Usage

> [!WARNING]
> Not done, however this is how it is planned to go

- Add `include config-kanshi-gui` to your [kanshi config](https://man.archlinux.org/man/kanshi.5.en)
  (and ignore that file in your `.gitignore` if wanted)
- Open this GUI.
- Create a new config by dragging things and pressing buttons for current outputs
- Reload

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
