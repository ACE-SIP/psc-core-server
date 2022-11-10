from pydantic import BaseSettings


class Config(BaseSettings):
    service_name: str = 'pharmaceutical_supply_chain'
    secret_key: str = 'algorand_pharmaceutical_supply_chain'


config = Config()

