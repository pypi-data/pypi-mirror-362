import os
from pathlib import Path, PosixPath, WindowsPath
from dataclasses import asdict, dataclass, field, fields
import platform
from typing import Any, Mapping, Sequence
from ruamel.yaml import YAML

_yaml = YAML()
def _represent_path(dumper, data):
    return dumper.represent_scalar("tag:yaml.org,2002:str", str(data))

_yaml.representer.add_representer(PosixPath, _represent_path)
_yaml.representer.add_representer(WindowsPath, _represent_path)

@dataclass
class _Config:
    custom_rulesets: dict[str, Path] = field(default_factory=dict)
    log_file: Path = field(default_factory=lambda: config_path() / Path("loganon.log"))
    _init_complete: bool = False

    @classmethod
    def load(cls) -> "_Config":
        try:
            with open(config_path() / Path("config.yaml"), "r") as f:
                kwargs = _yaml.load(f) or {}
                if kwargs:
                    for field in fields(cls):
                        if field.name in kwargs:
                            kwargs[field.name] = field.type(kwargs[field.name])
                return cls(**kwargs)
        except FileNotFoundError:
            return cls()
    
    def __post_init__(self) -> None:
        # Create the config directory if it doesn't exist
        config_path().mkdir(parents=True, exist_ok=True)

        # Overriding __setattr__ too early causes the dataclass initializer to fail
        self._init_complete = True

    def __setattr__(self, key: str, value: Any) -> None:
        # Use default setattr if the class is still initializing
        if not self._init_complete:
            super().__setattr__(key, value)
            return
        
        # Raise an error if there's an unknown field provided
        if key not in {field.name for field in fields(self.__class__)}:
            raise ValueError(f"Unknown config field: {key}")
            
        current_val = getattr(self, key)
        if isinstance(current_val, Sequence) and not isinstance(current_val, str):
            super().__setattr__(key, [*current_val, value])
        elif isinstance(current_val, Mapping):
            super().__setattr__(key, {**current_val, **value})
        else:
            super().__setattr__(key, value)
        
        self._save()
    
    def _save(self) -> None:
        cp = config_path() / Path("config.yaml")
        with open(cp, "w") as f:
            data = {k: v for k, v in asdict(self).items() if not k.startswith("_")}
            _yaml.dump(data, f)


def config_path() -> Path:
    if os.environ.get("LOGANON_CONFIG_PATH"):
        return Path(os.environ.get("LOGANON_CONFIG_PATH"))
    
    # Else use default locations
    if platform.system() == "Windows":
        return Path(os.path.expanduser("~\\AppData\\Local\\loganon\\"))
    else:
        return Path(os.path.expanduser("~/.config/loganon/"))

# Export the config object
config = _Config.load()