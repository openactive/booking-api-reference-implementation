from typing import Dict
from typing import List
from typing import get_type_hints

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

    def __init__(self, _identifier=False):
        if _identifier:
            self.identifier = _identifier
            self.id = '$HOST$/' + self.type.lower() + '/' + self.identifier

    def create(self, variables):
        self.load(variables)
        pass

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
        attrs = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith('__') and not attr.startswith('_')]
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


class Order(ObjectModel):

    type = "Order"
    broker: Dict = {}
    customer: Dict = {}
    orderedItem: List[Dict] = {}
    potentialAction: List[Dict] = []

    def create(self, variables):
        super(Order, self).create(variables)
        self.potentialAction.append(Action().new('Pay'))
        pass


class Action(BaseModel):

    name: str = None
    target: Dict = {
        "type": "EntryPoint",
        "urlTemplate": "$HOST$/{order_id}",
        "encodingType": "application/vnd.openactive.v$VERSION$+json",
        "httpMethod": "PATCH"
    }

    def new(self, name,):
        self.name = name
        self.type = name + 'Action'
        return self.as_json_ld()
