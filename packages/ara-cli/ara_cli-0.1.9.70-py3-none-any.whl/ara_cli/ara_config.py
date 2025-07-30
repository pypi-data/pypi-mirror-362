from typing import List, Dict, Optional
from pydantic import BaseModel
import json
import os
from os.path import exists, dirname
from os import makedirs
from functools import lru_cache


DEFAULT_CONFIG_LOCATION = "./ara/.araconfig/ara_config.json"


class LLMConfigItem(BaseModel):
    provider: str
    model: str
    temperature: float
    max_tokens: Optional[int] = None


class ARAconfig(BaseModel):
    ext_code_dirs: List[Dict[str, str]] = [
        {"source_dir_1": "./src"},
        {"source_dir_2": "./tests"},
    ]
    glossary_dir: str = "./glossary"
    doc_dir: str = "./docs"
    local_prompt_templates_dir: str = "./ara/.araconfig"
    custom_prompt_templates_subdir: Optional[str] = "custom-prompt-modules"
    local_ara_templates_dir: str = "./ara/.araconfig/templates/"
    ara_prompt_given_list_includes: List[str] = [
        "*.businessgoal",
        "*.vision",
        "*.capability",
        "*.keyfeature",
        "*.epic",
        "*.userstory",
        "*.example",
        "*.feature",
        "*.task",
        "*.py",
        "*.md",
        "*.png",
        "*.jpg",
        "*.jpeg",
    ]
    llm_config: Dict[str, LLMConfigItem] = {
        "gpt-4o": {
            "provider": "openai",
            "model": "openai/gpt-4o",
            "temperature": 0.8,
            "max_tokens": 16384
        },
        "gpt-4.1": {
            "provider": "openai",
            "model": "openai/gpt-4.1",
            "temperature": 0.8,
            "max_tokens": 1024
        },
        "o3-mini": {
            "provider": "openai",
            "model": "openai/o3-mini",
            "temperature": 1.0,
            "max_tokens": 1024
        },
        "opus-4": {
            "provider": "anthropic",
            "model": "anthropic/claude-opus-4-20250514",
            "temperature": 0.8,
            "max_tokens": 32000
        },
        "sonnet-4": {
            "provider": "anthropic",
            "model": "anthropic/claude-sonnet-4-20250514",
            "temperature": 0.8,
            "max_tokens": 1024
        },
        "together-ai-llama-2": {
            "provider": "together_ai",
            "model": "together_ai/togethercomputer/llama-2-70b",
            "temperature": 0.8,
            "max_tokens": 1024
        },
        "groq-llama-3": {
            "provider": "groq",
            "model": "groq/llama3-70b-8192",
            "temperature": 0.8,
            "max_tokens": 1024
        }
    }
    default_llm: Optional[str] = "gpt-4o"


# Function to ensure the necessary directories exist
@lru_cache(maxsize=None)
def ensure_directory_exists(directory: str):
    if not exists(directory):
        os.makedirs(directory)
        print(f"New directory created at {directory}")
    return directory


def validate_config_data(filepath: str):
    with open(filepath, "r") as file:
        data = json.load(file)
    return data


# Function to read the JSON file and return an ARAconfig model
@lru_cache(maxsize=1)
def read_data(filepath: str) -> ARAconfig:
    if not exists(filepath):
        # If file does not exist, create it with default values
        default_config = ARAconfig()

        with open(filepath, "w") as file:
            json.dump(default_config.model_dump(mode='json'), file, indent=4)

        print(
            f"ara-cli configuration file '{filepath}' created with default configuration. Please modify it as needed and re-run your command"
        )
        exit()  # Exit the application

    data = validate_config_data(filepath)
    return ARAconfig(**data)


# Function to save the modified configuration back to the JSON file
def save_data(filepath: str, config: ARAconfig):
    with open(filepath, "w") as file:
        json.dump(config.model_dump(mode='json'), file, indent=4)


# Singleton for configuration management
class ConfigManager:
    _config_instance = None

    @classmethod
    def get_config(cls, filepath=DEFAULT_CONFIG_LOCATION):
        if cls._config_instance is None:
            config_dir = dirname(filepath)

            if not exists(config_dir):
                makedirs(config_dir)

            cls._config_instance = read_data(filepath)
        return cls._config_instance