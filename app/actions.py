from providers import Provider
import logging

class BaseAction():

    def __init__(self):
        self._provider = Provider()
        self._resource_type = self.__class__.__name__.lower()

    def get(self, resource_id):
        return self._provider.read(self._resource_type.lower(), resource_id)


class Event(BaseAction):
    pass

class Offer(BaseAction):
    pass

class Order(BaseAction):
    pass
