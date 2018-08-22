from providers import DefaultProvider
import importlib

import logging


class BaseAction():

    def __init__(self):
        self._provider = DefaultProvider()
        self._resource_type = self.__class__.__name__.lower()
        self._model_name = self.__class__.__name__
        self.model = getattr(importlib.import_module('models'), self._model_name)

    def get(self, resource_id):
        data, errors = self._provider.read(self._resource_type.lower(), resource_id)
        if errors is None:
            model = self.model(resource_id)
            model.load(data)
            data = model.as_json_ld()
        return data, errors


class Event(BaseAction):
    pass

class Offer(BaseAction):
    pass

class Order(BaseAction):
    pass
