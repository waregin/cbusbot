"""Loads config.toml into a typed object so cogs never hardcode IDs."""

import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from zoneinfo import ZoneInfo

# Repo root — asset files (vore.png, inspirePics/, ...) live here.
ROOT = Path(__file__).resolve().parents[1]

# Mutable state (counters, etc). In Docker this is a mounted volume so state
# survives image updates.
DATA_DIR = ROOT / "data"


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
    admin_channel_id: int
    owner_id: int
    kiwi_id: int
    elle_id: int
    admin_role_id: int
    birthday_role_id: int
    staff_role_id: int
    unverified_role_id: int
    columbusites_role_id: int
    lvl10_role_id: int
    lvl15_role_id: int
    aged_role_id: int
    after_dark_role_id: int
    caterpillar_role_id: int
    butterfly_role_id: int
    timezone: str = "America/New_York"
    renames: list[Rename] = field(default_factory=list)
    enabled_cogs: list[str] = field(default_factory=list)

    @property
    def tz(self) -> ZoneInfo:
        return ZoneInfo(self.timezone)


def load_config(path: str | Path = ROOT / "config.toml") -> Config:
    with open(path, "rb") as f:
        raw = tomllib.load(f)
    return Config(
        guild_id=raw["guild"]["id"],
        general_channel_id=raw["channels"]["general"],
        food_channel_id=raw["channels"]["food"],
        admin_channel_id=raw["channels"]["admin"],
        owner_id=raw["users"]["owner"],
        kiwi_id=raw["users"]["kiwi"],
        elle_id=raw["users"]["elle"],
        admin_role_id=raw["roles"]["admin"],
        birthday_role_id=raw["roles"]["birthday"],
        staff_role_id=raw["roles"]["staff"],
        unverified_role_id=raw["roles"]["unverified"],
        columbusites_role_id=raw["roles"]["columbusites"],
        lvl10_role_id=raw["roles"]["lvl10"],
        lvl15_role_id=raw["roles"]["lvl15"],
        aged_role_id=raw["roles"]["aged"],
        after_dark_role_id=raw["roles"]["after_dark"],
        caterpillar_role_id=raw["roles"]["caterpillar"],
        butterfly_role_id=raw["roles"]["butterfly"],
        timezone=raw["schedule"]["timezone"],
        renames=[Rename(**r) for r in raw.get("renames", [])],
        enabled_cogs=raw["cogs"]["enabled"],
    )
