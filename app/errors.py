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
        "details": "The endpoint you requested can not been found.",
        "status": 404,
        "instance": "",
        "method": ""
    },
    "resource_not_found": {
        "@context": "https://openactive.io/ns/oa.jsonld",
        "type": "Error",
        "errorType": "https://openactive.io/errors/not_found",
        "title": "Not found",
        "details": "The resource you requested can not been found.",
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
    },
    "no_data_supplied": {
        "@context": "https://openactive.io/ns/oa.jsonld",
        "type": "Error",
        "errorType": "https://openactive.io/errors/no_data_supplied",
        "title": "No data supplied",
        "details": "The client supplied no data",
        "status": 400,
        "instance": "",
        "method": ""
    },
    "not_valid_json": {
        "@context": "https://openactive.io/ns/oa.jsonld",
        "type": "Error",
        "errorType": "https://openactive.io/errors/not_json",
        "title": "Not valid JSON",
        "details": "The data supplied was not correctly formatted as json",
        "status": 400,
        "instance": "",
        "method": ""
    },
    "incomplete_event_details": {
        "@context": "https://openactive.io/ns/oa.jsonld",
        "type": "Error",
        "errorType": "https://openactive.io/errors/incomplete_event_details",
        "title": "Incomplete Event Details",
        "details": "No event details, or incomplete event details supplied.",
        "status": 400,
        "instance": "",
        "method": ""
    },
    "incomplete_offer_details": {
        "@context": "https://openactive.io/ns/oa.jsonld",
        "type": "Error",
        "errorType": "https://openactive.io/errors/incomplete_offer_details",
        "title": "Incomplete Offer Details",
        "details": "No offer details, or incomplete offer details supplied.",
        "status": 400,
        "instance": "",
        "method": ""
    },
    "incomplete_customer_details": {
        "@context": "https://openactive.io/ns/oa.jsonld",
        "type": "Error",
        "errorType": "https://openactive.io/errors/incomplete_customer_details",
        "title": "Incomplete Customer Details",
        "details": "No customer details, or incomplete customer details supplied.",
        "status": 400,
        "instance": "",
        "method": ""
    },
    "incomplete_broker_details": {
        "@context": "https://openactive.io/ns/oa.jsonld",
        "type": "Error",
        "errorType": "https://openactive.io/errors/incomplete_broker_details",
        "title": "Incomplete Broker Details",
        "details": "No broker details, or incomplete broker details supplied.",
        "status": 400,
        "instance": "",
        "method": ""
    },
    "unavailable_offer": {
        "@context": "https://openactive.io/ns/oa.jsonld",
        "type": "Error",
        "errorType": "https://openactive.io/errors/unavailable_offer",
        "title": "Unavailable Offer",
        "details": "The offer specified does not exist.",
        "status": 400,
        "instance": "",
        "method": ""
    },
    "offer_expired": {
        "@context": "https://openactive.io/ns/oa.jsonld",
        "type": "Error",
        "errorType": "https://openactive.io/errors/offer_expired",
        "title": "Offer Expired",
        "details": "The offer specified has expired.",
        "status": 400,
        "instance": "",
        "method": ""
    },
    "offer_not_yet_valid": {
        "@context": "https://openactive.io/ns/oa.jsonld",
        "type": "Error",
        "errorType": "https://openactive.io/errors/offer_not_yet_valid",
        "title": "Offer Not Yet Valid",
        "details": "The offer specified is not yet valid.",
        "status": 400,
        "instance": "",
        "method": ""
    },
    "offer_not_valid": {
        "@context": "https://openactive.io/ns/oa.jsonld",
        "type": "Error",
        "errorType": "https://openactive.io/errors/offer_not_valid",
        "title": "Offer Not Valid for Opportunity",
        "details": "The offer specified is not valid for this event.",
        "status": 400,
        "instance": "",
        "method": ""
    },
    "unavailable_order": {
        "@context": "https://openactive.io/ns/oa.jsonld",
        "type": "Error",
        "errorType": "https://openactive.io/errors/unavailable_order",
        "title": "Unavailable Order",
        "details": "The order specified does not exist or had expired.",
        "status": 400,
        "instance": "",
        "method": ""
    },
    "unavailable_event": {
        "@context": "https://openactive.io/ns/oa.jsonld",
        "type": "Error",
        "errorType": "https://openactive.io/errors/unavailable_event",
        "title": "Unavailable Event",
        "details": "The event specified does not exist or had expired.",
        "status": 400,
        "instance": "",
        "method": ""
    },
    "event_is_full": {
        "@context": "https://openactive.io/ns/oa.jsonld",
        "type": "Error",
        "errorType": "https://openactive.io/errors/event_is_full",
        "title": "Event is Full",
        "details": "The event specified is full.",
        "status": 400,
        "instance": "",
        "method": ""
    },
    "event_has_insufficient_spaces": {
        "@context": "https://openactive.io/ns/oa.jsonld",
        "type": "Error",
        "errorType": "https://openactive.io/errors/event_has_insufficient_spaces",
        "title": "Insufficient Spaces",
        "details": "The event has less available spaces than the amount requested.",
        "status": 400,
        "instance": "",
        "method": ""
    },
    "insufficient_information": {
        "@context": "https://openactive.io/ns/oa.jsonld",
        "type": "Error",
        "errorType": "https://openactive.io/errors/insufficient_information",
        "title": "Insufficient Information",
        "details": "Insufficient information has been provided to carry out your request.",
        "status": 400,
        "instance": "",
        "method": ""
    },
    "too_much_information": {
        "@context": "https://openactive.io/ns/oa.jsonld",
        "type": "Error",
        "errorType": "https://openactive.io/errors/too_much_information",
        "title": "Too Much Information",
        "details": "Too much information has been provided to carry out your request.",
        "status": 400,
        "instance": "",
        "method": ""
    },
    "anonymous_lease_expired": {
        "@context": "https://openactive.io/ns/oa.jsonld",
        "type": "Error",
        "errorType": "https://openactive.io/errors/anonymous_lease_expired",
        "title": "Anonymous Lease Expired",
        "details": "The lease has expired. Please restart the booking process.",
        "status": 400,
        "instance": "",
        "method": ""
    },
    "payment_amount_incorrect": {
        "@context": "https://openactive.io/ns/oa.jsonld",
        "type": "Error",
        "errorType": "https://openactive.io/errors/payment_amount_incorrect",
        "title": "Payment Amount Incorrect",
        "details": "The amount paid does not match the amount in the invoice.",
        "status": 400,
        "instance": "",
        "method": ""
    },
    "currency_incorrect": {
        "@context": "https://openactive.io/ns/oa.jsonld",
        "type": "Error",
        "errorType": "https://openactive.io/errors/currency_incorrect",
        "title": "Currency Incorrect",
        "details": "The currency of the payment does not match the currency of the invoice.",
        "status": 400,
        "instance": "",
        "method": ""
    },
    "order_cannot_be_completed": {
        "@context": "https://openactive.io/ns/oa.jsonld",
        "type": "Error",
        "errorType": "https://openactive.io/errors/order_cannot_be_completed",
        "title": "Order Cannot be Completed",
        "details": "The order is not in a state where it can be completed.",
        "status": 400,
        "instance": "",
        "method": ""
    },
    "order_cannot_be_cancelled": {
        "@context": "https://openactive.io/ns/oa.jsonld",
        "type": "Error",
        "errorType": "https://openactive.io/errors/order_cannot_be_cancelled",
        "title": "Order Cannot be Cancelled",
        "details": "The order is not in a state where it can be cancelled.",
        "status": 400,
        "instance": "",
        "method": ""
    },
    "order_is_uncancellable": {
        "@context": "https://openactive.io/ns/oa.jsonld",
        "type": "Error",
        "errorType": "https://openactive.io/errors/order_is_uncancellable",
        "title": "Order is Uncancellable",
        "details": "The offer in the order is not cancellable.",
        "status": 400,
        "instance": "",
        "method": ""
    },
    "order_cancellation_window_expired": {
        "@context": "https://openactive.io/ns/oa.jsonld",
        "type": "Error",
        "errorType": "https://openactive.io/errors/order_is_uncancellable",
        "title": "Order Cancellation Window Expired",
        "details": "The order cannot be cancelled as the cancellation window has expired.",
        "status": 400,
        "instance": "",
        "method": ""
    }
}
