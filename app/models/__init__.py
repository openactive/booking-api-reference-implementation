from typing import Dict
from typing import List
from typing import get_type_hints

from providers import DefaultProvider
import importlib
import json

import logging

time_variables = ['startDate', 'endDate', 'validFrom',
                  'validThrough', 'orderDate', 'paymentDueDate', 'cancellationValidUntil']

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
            self._resource_type.lower(), self._identifier, json.dumps(self.as_json_ld(), sort_keys=True, indent=4, separators=(',', ': ')))
        return self.as_json_ld, errors

    def get(self):
        data, errors = self._provider.read(self._resource_type.lower(), self._identifier)
        if data is not None:
            self.load(data)
            return self.as_json_ld(), errors
        else:
            return None, 'resource_not_found'

    def update(self, variables):
        self.load(variables)
        errors = self._provider.write(
            self._resource_type.lower(), self._identifier, json.dumps(self.as_json_ld(), sort_keys=True, indent=4, separators=(',', ': ')))
        return self.as_json_ld, errors

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
                        _as_json[variable] = getattr(self, variable).strftime("%Y-%m-%dT%H:%M:%SZ")
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

    def __init__(self, identifier=False):
        super(ObjectModel, self).__init__()
        self._provider = DefaultProvider()
        if not identifier:
            self._identifier = self._provider.get_unique_id(self._resource_type)
        else:
            self._identifier = identifier
        self.id = '$HOST$/' + self._resource_type.lower() + 's/' + self._identifier


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
    orderLeaseDuration: str = "PT15M"

    def create(self, variables):
        super(Order, self).create(variables)
        self.potentialAction = [Action().new('Pay', url='$HOST$/orders/{order_id}')]
        pass

    def update(self, variables, cancel=False):
        super(Order, self).update(variables)
        #self.potentialAction = []
        #if not cancel:
        #    logging.warn("PAYMENT")
        pass


class Event(ObjectModel):

    type = "Event"

    name: str = ""
    startDate: str = ""
    endDate: str = ""
    offers: List[Dict] = []
    activity: str = ""
    description: str = ""
    duration: str = "PT1H"
    maximumAttendeeCapacity: int = 10
    remainingAttendeeCapacity: int = 10
    orderLeases: Dict = {}
    completedOrders: Dict = {}
    location: Dict = {
        "address": {
            "addressLocality": "Whitbury",
            "addressRegion": "Hampshire",
            "postalCode": "WH5 2CB",
            "streetAddress": "Whitbury New Town Leisure Centre, Brittas Road",
            "type": "PostalAddress"
        },
        "ammenityFeature": [
            {
                "name": "Changing Facilities",
                "type": "ChangingFacilities",
                "value": True
            },
            {
                "name": "Showers",
                "type": "Showers",
                "value": True
            },
            {
                "name": "Lockers",
                "type": "Lockers",
                "value": True
            },
            {
                "name": "Towels",
                "type": "Towels",
                "value": False
            },
            {
                "name": "Creche",
                "type": "Creche",
                "value": False
            },
            {
                "name": "Parking",
                "type": "Parking",
                "value": True
            }
        ],
        "description": "The best fictional leisure centre.",
        "geo": {
            "latitude": 50.85,
            "longitude": -1.78,
            "type": "GeoCoordinates"
        },
        "name": "Whitbury New Town Leisure Centre",
        "telephone": "01234 567890",
        "type": "Place",
        "url": "http://www.whitbury-leisure.org.uk/"
    }

    def create(self, variables):
        super(Event, self).create(variables)
        self.remainingAttendeeCapacity = self.maximumAttendeeCapacity
        pass

class Offer(ObjectModel):

    type = "Offer"
    name: str = ""
    price: float = 0.00
    priceCurrency: str = "GBP"
    validFrom: str = ""
    validThrough: str = ""
    description: str = ""
    isCancellable: bool = True
    cancellationValidUntil: str = ""
    itemOffered: Dict = {}


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
