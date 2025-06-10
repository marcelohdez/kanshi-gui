from typing import Any
import opts as o


class Output:
    def __init__(self):
        self._opts: dict[str, Any] = {}

    def set_enabled(self, enabled: bool):
        self._opts[o.ENABLED] = enabled

    def set_mode(self, width: int, height: int, rate: float | None = None):
        self._opts[o.MODE] = (width, height, rate)

    def set_position(self, x: int, y: int):
        self._opts[o.POSITION] = (x, y)

    def set_scale(self, factor: float):
        self._opts[o.SCALE] = factor

    def set_transform(self, transform: int | str):
        self._opts[o.TRANSFORM] = transform

    def set_adaptive_sync(self, enabled: bool):
        self._opts[o.ADAPTIVE_SYNC] = "on" if enabled else "off"

    def __str__(self) -> str:
        lines = []

        for opt, value in self._opts.items():
            match opt:
                case o.ENABLED:
                    lines.append("enable" if value else "disable")
                case o.MODE:
                    (w, h, r) = value
                    if r:
                        lines.append(f"{opt} {w}x{h}@{r}Hz")
                    else:
                        lines.append(f"{opt} {w}x{h}")
                case o.POSITION:
                    (x, y) = value
                    lines.append(f"{opt} {x},{y}")
                case o.SCALE:
                    lines.append(f"{opt} {value}")
                case o.TRANSFORM:
                    lines.append(f"{opt} {value}")
                case o.ADAPTIVE_SYNC:
                    lines.append(f"{opt} {value}")

        return "\n".join(lines)


class Profile:
    def __init__(self):
        self.outputs: dict[str, Output] = {}
        self.exec: str | None = None


class Config:
    def __init__(self):
        self.profiles: list[Profile] = []


def indent_text(text, tabs=1):
    """Add tabs to the beginning of each line in the text."""
    tab = "\t" * tabs
    return "\n".join(tab + line for line in text.split("\n"))


def write_config(config: Config, path: str):
    with open(path, "a") as f:
        for profile in config.profiles:
            f.write("\nprofile {\n")

            for name, output_config in profile.outputs.items():
                f.write(f'\toutput "{name}" {{\n')
                f.write(indent_text(str(output_config), 2))
                f.write("\n\t}\n")

            f.write("}\n")
