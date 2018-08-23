from typing import Dict
from typing import List
from typing import get_type_hints

from providers import DefaultProvider
import importlib
import json

import logging

time_variables = []

"""
    BaseModel has some standard variables and some commonly used functions
    to make individual models significantly slimmer.
    The dictionary representation of the model is based on the model's structure.
    Adding fields to the model automatically adds those fields to the representation
    of the model.
"""


class BaseModel():

    type: str = None

    def __init__(self):
        self._resource_type = self.__class__.__name__.lower()

    def create(self, variables):
        self.load(variables)
        errors = self._provider.write(
            self._resource_type.lower(), self.identifier, json.dumps(self.as_json_ld(), sort_keys=True, indent=4, separators=(',', ': ')))
        return self.as_json_ld, errors

    def get(self):
        data, errors = self._provider.read(self._resource_type.lower(), self.identifier)
        if data is not None:
            self.load(data)
            return self.as_json_ld(), errors
        else:
            return None, 'resource_not_found'

    def update(self, variables):
        pass

    def load(self, variables):
        for attr in variables:
            if attr in self.get_attrs():
                setattr(self, attr, variables[attr])
        pass

    def delete(self):
        pass

    def get_attrs(self):
        attrs = [attr for attr in dir(self) if not callable(
            getattr(self, attr)) and not attr.startswith('__') and not attr.startswith('_')]
        return attrs

    def set_attr(self):
        pass

    def as_dict(self):
        _as_json = {}
        for variable in self.get_attrs():
            if variable in time_variables:
                if getattr(self, variable) is not None:
                    try:
                        _as_json[variable] = getattr(self, variable).strftime("%Y-%m-%dT%H:%M:%S")
                    except:
                        _as_json[variable] = getattr(self, variable)
                else:
                    _as_json[variable] = None
            else:
                _as_json[variable] = getattr(self, variable)
        return _as_json

    def as_json_ld(self):
        _as_json_ld = self.as_dict()
        _as_json_ld['@context'] = 'https://openactive.io/ns/oa.jsonld'
        return _as_json_ld


class ObjectModel(BaseModel):

    identifier: str = None
    id: str = None

    def __init__(self, _identifier=False):
        super(ObjectModel, self).__init__()
        self._provider = DefaultProvider()
        if not _identifier:
            self.identifier = self._provider.get_unique_id(self._resource_type)
        else:
            self.identifier = _identifier
        self.id = '$HOST$/' + self._resource_type.lower() + '/' + self.identifier
        logging.warn("IDENTIFIER = " + str(self.identifier))


class Order(ObjectModel):

    type = "Order"
    acceptedOffer: List[Dict] = []
    broker: Dict = {}
    customer: Dict = {}
    orderDate: str = ""
    orderedItem: List[Dict] = {}
    orderLeaseDuration: str = "PT15M"
    orderStatus: str = "https://schema.org/OrderPaymentDue"
    partOfInvoice: Dict = {}
    paymentDueDate: str = ""
    potentialAction: List[Dict] = []

    def create(self, variables):
        super(Order, self).create(variables)
        self.potentialAction.append(Action().new('Pay', url='$HOST$/orders/{order_id}'))
        pass

    def update(self, variables, cancel=False):
        super(Order, self).update(variables)
        self.potentialAction = []
        if not cancel:
            logging.warn("PAYMENT")
        pass


class Action(BaseModel):

    name: str = None
    target: Dict = {
        "type": "EntryPoint",
        "urlTemplate": "$HOST$/{order_id}",
        "encodingType": "application/vnd.openactive.v$VERSION$+json",
        "httpMethod": "PATCH"
    }

    def new(self, name, url=False):
        self.name = name
        self.type = name + 'Action'
        if url:
            self.target['urlTemplate'] = url
        return self.as_json_ld()
