"""Loads config.toml into a typed object so cogs never hardcode IDs."""

import tomllib
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class Config:
    guild_id: int
    general_channel_id: int
    owner_id: int
    enabled_cogs: list[str] = field(default_factory=list)


def load_config(path: str | Path = "config.toml") -> Config:
    with open(path, "rb") as f:
        raw = tomllib.load(f)
    return Config(
        guild_id=raw["guild"]["id"],
        general_channel_id=raw["channels"]["general"],
        owner_id=raw["users"]["owner"],
        enabled_cogs=raw["cogs"]["enabled"],
    )
