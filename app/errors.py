ERRORS = {
    "unauthenticated": {
        "@context": "https://openactive.io/ns/oa.jsonld",
        "type": "Error",
        "errorType": "https://openactive.io/errors/unauthenticated",
        "title": "No API token or authentication provided",
        "details": "The broker did not provide an API token or basic authentication.",
        "status": 403,
        "instance": "",
        "method": ""
    },
    "no_api_token_provided": {
        "@context": "https://openactive.io/ns/oa.jsonld",
        "type": "Error",
        "errorType": "https://openactive.io/errors/no_api_token_provided",
        "title": "No API token provided",
        "details": "The broker did not provide an API token in the x-api-key request header.",
        "status": 401,
        "instance": "",
        "method": ""
    },
    "invalid_api_token_provided": {
        "@context": "https://openactive.io/ns/oa.jsonld",
        "type": "Error",
        "errorType": "https://openactive.io/errors/invalid_api_token_provided",
        "title": "Incorrect API token provided",
        "details": "The broker provided an invalid API token in the x-api-key request header.",
        "status": 401,
        "instance": "",
        "method": ""
    },
    "invalid_authorization_details": {
        "@context": "https://openactive.io/ns/oa.jsonld",
        "type": "Error",
        "errorType": "https://openactive.io/errors/invalid_authorization_details",
        "title": "Incorrect basic authentication credentials provided",
        "details": "The broker provided invalid basic authentication credentials.",
        "status": 401,
        "instance": "",
        "method": ""
    },
    "not_found": {
        "@context": "https://openactive.io/ns/oa.jsonld",
        "type": "Error",
        "errorType": "https://openactive.io/errors/not_found",
        "title": "Not found",
        "details": "The endpoint or resource you requested can not been found.",
        "status": 404,
        "instance": "",
        "method": ""
    },
    "gone": {
        "@context": "https://openactive.io/ns/oa.jsonld",
        "type": "Error",
        "errorType": "https://openactive.io/errors/gone",
        "title": "Gone",
        "details": "The endpoint or resource you requested is no longer available",
        "status": 410,
        "instance": "",
        "method": ""
    },
    "method_not_allowed": {
        "@context": "https://openactive.io/ns/oa.jsonld",
        "type": "Error",
        "errorType": "https://openactive.io/errors/method_not_allowed",
        "title": "Method not allowed",
        "details": "The endpoint or resource you requested does not respond to the HTTP verb you supplied",
        "status": 405,
        "instance": "",
        "method": ""
    }
}
