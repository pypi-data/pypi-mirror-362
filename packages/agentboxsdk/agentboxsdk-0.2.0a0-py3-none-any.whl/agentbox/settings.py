import os
from pathlib import Path
import yaml
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """SOT settings for AgentBox runtime options."""

    engine: str = "dummy"
    model: str = "na"

    # Engine specific settings
    open_api_key: str | None = None
    ollama_host: str = "http://localhost:11434"

    # General
    request_timeout: float = 60.0

    model_config = SettingsConfigDict(env_prefix="AGENTBOX_", extra="ignore")

    # ───────────────────────── helpers ────────────────────────── #

    @classmethod
    def locate_yaml(cls) -> Path | None:
        """Return the first existing .agentbox.yaml (cwd -> $HOME)."""
        for path in (Path.cwd(), Path.home()):
            yml = path / ".agentbox.yaml"
            if yml.exists():
                return yml
        return None

    @classmethod
    def load(cls) -> "Settings":
        """Merge YAML (if any) + env vars -> Settings object."""
        yml_path = cls.locate_yaml()

        # If YAML exists, update only non-env-overridden values
        if yml_path:
            file_data = yaml.safe_load(yml_path.read_text()) or {}
            filtered_data = {
                k: v
                for k, v in file_data.items()
                if f"AGENTBOX_{k.upper()}" not in os.environ
            }
            return cls(**filtered_data)

        return cls()

    def save(self, path: Path | None = None) -> None:
        """Write current settings to YAML file."""
        if path is None:
            path = self.locate_yaml()
        if path is None:
            raise RuntimeError("No .agentbox.yaml found in current dir or home dir.")
        path.write_text(yaml.safe_dump(self.model_dump(mode="python"), sort_keys=False))

    def __str__(self) -> str:
        # TODO: Add a string representation of the settings.
        """A string representation of the Settings object."""
        return f"Settings(engine={self.engine}, model={self.model})"
