API = {
    "version": "1.0",
    "basicAuth": {
        "username": 'openactive',
        "password": 'UsingDataToHelpPeopleGetActive'
    },
    "apiKey": "rr4nlnyhi3tdoonxfysi"
}

LOCAL_PERSISTENCE = {
    "folder": "../local_data",
    "models": ['event', 'offer', 'order']
}

LOCAL_DATA = {
    'Events': [
        {
            "identifier": "1234",
            "name": "Aerobics (Week 1)",
            "startTime": "08:00:00",
            "startDateDelta": 1,
            "startDateDeltaType": "W",
            "durationDelta": 1,
            "durationDeltaType": "H",
            "description": "A fast paced Aerobics class. Leg warmers optional."
        },
        {
            "identifier": "5678",
            "name": "Aerobics (Week 2)",
            "startTime": "10:00:00",
            "startDateDelta": 2,
            "startDateDeltaType": "W",
            "durationDelta": 1,
            "durationDeltaType": "H",
            "description": "A fast paced Aerobics class. Leg warmers optional."
        }
    ],
    'Offers': [
        {
            "name": "Aerobics - early bird",
            "description": "Early bird booking for Aerobics. Cannot be cancelled",
            "validFromDelta": -1,
            "validFromDeltaType": "W",
            "validThroughDelta": -2,
            "validThroughDeltaType": "D",
            "isCancellable": False,
            "price": 7.99
        },
        {
            "name": "Aerobics - full price",
            "description": "Normal price booking for Aerobics. Can be cancelled up to the day before.",
            "validFromDelta": -1,
            "validFromDeltaType": "W",
            "validThroughDelta": -1,
            "validThroughDeltaType": "H",
            "isCancellable": True,
            "cancellationValidUntilDelta": -1,
            "cancellationValidUntilDeltaType": "D",
            "price": 9.99
        }
    ]
}
