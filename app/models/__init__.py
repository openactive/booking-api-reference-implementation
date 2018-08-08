from typing import Dict
from typing import List
from typing import get_type_hints

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
    identifier: str = None
    id: str = None

    def __init__(self, _identifier=False):
        if _identifier:
            self.identifier = _identifier
            self.id = '$HOST$/' + self.type.lower() + '/' + self.identifier

    def create(self, variables):
        pass

    def update(self, variables):
        pass

    def get(self):
        pass

    def delete(self):
        pass

    def get_variables(self):
        variables = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith('__') and not attr.startswith('_')]
        return variables

    def as_dict(self):
        _as_json = {}
        for variable in self.get_variables():
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

class Order(BaseModel):

    type = "Order"
    potentialAction: List[Dict] = []
