from dataclasses import dataclass
from environs import Env


@dataclass
class BotConfig:
    token: str


@dataclass
class DbConfig:
    dns: str
    is_echo: bool


@dataclass
class Config:
    tg_bot: BotConfig
    db: DbConfig


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=BotConfig(
            token=env('BOT_TOKEN'),
        ),
        db=DbConfig(
            dns=env('DNS'),
            is_echo=env.bool('IS_ECHO')
        )
    )
