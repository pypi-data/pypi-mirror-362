import os
import json
from dataclasses import dataclass, asdict, field


def get_config_path():
    return os.environ.get(
        "JBUSSDIEKER_CONFIG", os.path.expanduser("~/.jbussdieker.json")
    )


@dataclass
class Config:
    user_name: str = "Joshua B. Bussdieker"
    user_email: str = "jbussdieker@gmail.com"
    github_org: str = "jbussdieker"
    private: bool = True
    log_format: str = "%(levelname)s: %(message)s"
    log_level: str = "INFO"
    openai_api_key: str = ""
    custom_settings: dict = field(default_factory=dict)

    asdict = asdict

    def save(self):
        with open(get_config_path(), "w") as f:
            json.dump(self.asdict(), f, indent=2)

    @classmethod
    def load(cls):
        if os.path.exists(get_config_path()):
            with open(get_config_path()) as f:
                data = json.load(f)
            return cls(**data)
        else:
            return cls()
