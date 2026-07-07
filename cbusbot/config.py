"""Loads config.toml into a typed object so cogs never hardcode IDs."""

import tomllib
from dataclasses import dataclass, field
from pathlib import Path

# Repo root — asset files (vore.png, inspirePics/, ...) live here.
ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Rename:
    month: int
    day: int
    name: str


@dataclass(frozen=True)
class Config:
    guild_id: int
    general_channel_id: int
    food_channel_id: int
    owner_id: int
    kiwi_id: int
    elle_id: int
    admin_role_id: int
    birthday_role_id: int
    staff_role_id: int
    unverified_role_id: int
    columbusites_role_id: int
    renames: list[Rename] = field(default_factory=list)
    enabled_cogs: list[str] = field(default_factory=list)


def load_config(path: str | Path = ROOT / "config.toml") -> Config:
    with open(path, "rb") as f:
        raw = tomllib.load(f)
    return Config(
        guild_id=raw["guild"]["id"],
        general_channel_id=raw["channels"]["general"],
        food_channel_id=raw["channels"]["food"],
        owner_id=raw["users"]["owner"],
        kiwi_id=raw["users"]["kiwi"],
        elle_id=raw["users"]["elle"],
        admin_role_id=raw["roles"]["admin"],
        birthday_role_id=raw["roles"]["birthday"],
        staff_role_id=raw["roles"]["staff"],
        unverified_role_id=raw["roles"]["unverified"],
        columbusites_role_id=raw["roles"]["columbusites"],
        renames=[Rename(**r) for r in raw.get("renames", [])],
        enabled_cogs=raw["cogs"]["enabled"],
    )
