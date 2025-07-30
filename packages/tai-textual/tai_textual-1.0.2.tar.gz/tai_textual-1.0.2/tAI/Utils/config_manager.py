"""
This module handles reading and writing configuration from config.json.
"""
import json
import os
from typing import Dict, Any

class ConfigManager:
    """
    This class handles reading and writing configuration from config.json.
    It loads the configuration once and provides methods to access and modify it.
    """
    def __init__(self, config_file: str = "config.json"):
        APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_file = os.path.join(APP_ROOT, config_file)
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Loads the configuration from the JSON file."""
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError as e:
                    raise Exception(f"Error loading config.json: {e}")
        raise Exception(f"config.json not found in {self.config_file}")

    def _save_config(self):
        """Saves the current configuration to the JSON file."""
        with open(self.config_file, "w") as f:
            json.dump(self.config, f, indent=2)

    def get_default_model(self) -> str:
        """Gets the default model from the configuration."""
        return self.config.get("default_model", "openrouter/mistralai/devstral-small:free")

    def set_default_model(self, model_id: str):
        """Sets the default model in the configuration."""
        self.config["default_model"] = model_id
        self._save_config()

    def get_models(self) -> Dict[str, str]:
        """Gets the available models from the configuration."""
        return self.config.get("models", {})

    def get_prompt(self) -> str:
        """Gets the prompt from the configuration."""
        return self.config.get("prompt", "")

    def set_prompt(self, prompt: str):
        """Sets the prompt in the configuration."""
        self.config["prompt"] = prompt
        self._save_config()

    def get_set_full_screen(self) -> bool:
        """Gets the full screen setting from the configuration."""
        return self.config.get("set_full_screen", False)

    def set_set_full_screen(self, full_screen: bool):
        """Sets the full screen setting in the configuration."""
        self.config["set_full_screen"] = full_screen
        self._save_config()

    def get_set_openrouter_for_all(self) -> bool:
        """Gets the openrouter for all setting from the configuration."""
        return self.config.get("set_openrouter_for_all", False)

    def set_set_openrouter_for_all(self, openrouter_for_all: bool):
        """Sets the openrouter for all setting in the configuration."""
        self.config["set_openrouter_for_all"] = openrouter_for_all
        self._save_config()

config_manager = ConfigManager() 