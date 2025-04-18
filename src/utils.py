from injector import Injector

from seedx_support_backend.infrastructure.app import AppModule
from seedx_support_backend.infrastructure.json import JsonModule


def create_injector():
    return Injector(modules=create_modules())


def create_modules():
    modules = [
        AppModule(),
        JsonModule(),
    ]
    return modules
