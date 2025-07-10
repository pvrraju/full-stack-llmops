"""
utils/config_loader.py
======================
Tiny helper that reads YAML configuration into a Python `dict`.  Centralising
this logic means other modules can simply call `load_config()` without worrying
about YAML semantics or file paths.

Default behaviour
-----------------
If no `config_path` argument is supplied we default to `config/config.yaml`
(relative to the repository root).  Feel free to pass an absolute path when
running scripts from outside the repo.
"""
import yaml
import os

def load_config(config_path: str = "config/config.yaml") -> dict:
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
        # print(config)
    return config