import json
import os
import subprocess
from typing import Any
from pathlib import Path
import opts as o

SELF_CONFIG_NAME = "wlr-displays.json"
KANSHI_CONFIG_NAME = "config-wlr-displays"

KANSHI_DESC_UNKNOWN = "Unkown"


class Mode:
    """Represents an available mode for a given output"""

    def __init__(self, width: int, height: int, refresh: float, preferred: bool):
        self.width = width
        self.height = height
        self.refresh = refresh
        self.preferred = preferred

    def __str__(self) -> str:
        return f"{self.width}x{self.height}@{self.refresh}Hz {'(preferred)' if self.preferred else ''}"

    def __eq__(self, o) -> bool:
        if not isinstance(o, Mode):
            raise NotImplementedError

        return (
            self.width == o.width
            and self.height == o.height
            and self.refresh == o.refresh
        )


class Output:
    """Represents a Kanshi output configuration."""

    def __init__(self):
        self._opts: dict[str, Any] = {}
        self.set_enabled(True)  # default to enabled

    def set_enabled(self, enabled: bool):
        self._opts[o.ENABLED] = enabled

    def set_mode(self, mode: Mode):
        self._opts[o.MODE] = [mode.width, mode.height, mode.refresh]

    def set_position(self, x: int, y: int):
        self._opts[o.POSITION] = [x, y]

    def set_scale(self, factor: float):
        self._opts[o.SCALE] = factor

    def set_transform(self, transform: int | str):
        self._opts[o.TRANSFORM] = transform

    def set_adaptive_sync(self, enabled: bool):
        self._opts[o.ADAPTIVE_SYNC] = "on" if enabled else "off"

    def to_dict(self) -> dict:
        return self._opts.copy()

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

    def to_dict(self) -> dict:
        return {
            "outputs": {name: opts.to_dict() for name, opts in self.outputs.items()},
            "exec": self.exec,
        }

    def __str__(self) -> str:
        def indent_text(text, tabs=1):
            """Add tabs to the beginning of each line in the text."""
            tab = "\t" * tabs
            return "\n".join(tab + line for line in text.split("\n"))

        output = []

        for name, output_config in self.outputs.items():
            output.append(f'\toutput "{name}" {{')
            output.append(indent_text(str(output_config), 2))
            output.append("\t}")

        return "\n".join(output)

    def __hash__(self) -> int:
        result = 0
        for desc in self.outputs.keys():
            result += hash(desc)

        return result


class Config:
    def __init__(self):
        self.profiles: set[Profile] = set()

    def to_dict(self) -> dict:
        return {"profiles": [p.to_dict() for p in self.profiles]}

    def __str__(self) -> str:
        output = []

        for profile in self.profiles:
            output.append("profile {")
            output.append(f"{profile}")
            output.append("}\n")

        return "\n".join(output)


class OutputStates:
    """
    Stores the state of outputs, including their available modes. Does not
    directly translate to a Kanshi profile
    """

    def __init__(self):
        self.outputs: dict[str, tuple[Output, list[Mode]]] = {}

    def __str__(self) -> str:
        lines = []

        for desc, tup in self.outputs.items():
            output, modes = tup
            lines.append(desc)
            lines.append(str(output))

            for mode in modes:
                lines.append(str(mode))

        return "\n".join(lines)


def get_current_state() -> OutputStates:
    """Will return the current state of all outputs using wlr-randr"""
    state = OutputStates()

    cmd = ["wlr-randr", "--json"]
    state_json = json.loads(subprocess.run(cmd, capture_output=True, check=True).stdout)

    for output_json in state_json:
        output_state = Output()
        modes = []

        # collect basic output state
        output_state.set_adaptive_sync(output_json["adaptive_sync"])
        output_state.set_enabled(output_json["enabled"])
        output_state.set_transform(output_json["transform"])
        output_state.set_scale(output_json["scale"])
        output_state.set_position(
            output_json["position"]["x"], output_json["position"]["y"]
        )

        # collect all modes
        for mode_json in output_json["modes"]:
            width = mode_json["width"]
            height = mode_json["height"]
            refresh = mode_json["refresh"]
            preferred = mode_json["preferred"]
            current = mode_json["current"]

            this_mode = Mode(width, height, refresh, preferred)
            modes.append(this_mode)

            if current:
                output_state.set_mode(this_mode)

        # get output description for kanshi
        if output_json["name"].startswith("eDP-"):
            description = output_json["name"]
        else:
            make = output_json["make"] or KANSHI_DESC_UNKNOWN
            model = output_json["model"] or KANSHI_DESC_UNKNOWN
            serial = output_json["serial"] or KANSHI_DESC_UNKNOWN
            description = f"{make} {model} {serial}"

        state.outputs[description] = (output_state, modes)

    return state


def get_config_home() -> Path:
    config_home_str = os.getenv("XDG_CONFIG_HOME") or "~/.config"
    return Path(config_home_str).expanduser()


def write_configs_to_disk(config: Config):
    """
    Will write the given config into our state, wlr-displays.json as well as overwriting
    the user's current kanshi config.
    """
    # write kanshi config
    kanshi_dir = get_config_home() / "kanshi"
    kanshi_dir.mkdir(parents=True, exist_ok=True)

    with open(kanshi_dir / KANSHI_CONFIG_NAME, "w") as f:
        f.write("# This config was automatically generated by wlr-displays. Any\n")
        f.write("# modifications will be overriden next time you use it.\n")
        f.write(f"{config}\n")

    # write wlr-displays config
    with open(get_config_home() / SELF_CONFIG_NAME, "w") as f:
        f.write(json.dumps(config.to_dict()))


def read_self_config() -> Config | None:
    """
    Will attempt to read wlr-displays.json, and turn it into a usable kanshi config,
    however if unsuccessful it will instead return None.
    """
    try:
        with open(get_config_home() / SELF_CONFIG_NAME, "r") as f:
            config = Config()
            config_json = json.loads(f.read())

            for profile_json in config_json["profiles"]:
                profile = Profile()

                for name, opts in profile_json["outputs"].items():
                    output = Output()
                    output._opts = opts
                    profile.outputs[name] = output

                if profile_json["exec"]:
                    profile.exec = profile_json["exec"]

                config.profiles.add(profile)

            return config
    except Exception:
        return None
