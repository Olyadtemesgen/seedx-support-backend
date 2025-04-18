from injector import singleton, provider, Module

from config import Config


class AppModule(Module):
    @provider
    @singleton
    def provide_config(self) -> Config:
        return Config()
