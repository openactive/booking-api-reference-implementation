import click
from flask import Flask
import uuid

import utils
import models
import actions

from manage import Manage

import logging
from datetime import datetime

app = Flask(__name__)
manage = Manage(app)
if not manage.check_persistence_exists():
    manage.build_clean_persistence()
    manage.populate_persistence()


@app.route("/", methods=["GET"])
@utils.requires_auth
def index():
    data = utils.render_json('index.json')
    return utils.json_response(data)


@app.route("/api/rpde", methods=["GET"])
@utils.requires_auth
def feed():
    variables = {
        'next': 'blah',
        'items': []
    }
    data = utils.render_json('feed.json', variables)
    return utils.json_response(data)


@app.route("/orders", methods=["POST"])
@app.route("/api/orders", methods=["POST"])
@utils.requires_auth
def create_order():
    params = ['orderedItem', 'acceptedOffer', 'customer', 'broker']
    variables, erroring_params, error = utils.request_variables(params)
    if error:
        if not variables['orderedItem']:
            return utils.error_response("incomplete_event_details")

        if not variables['acceptedOffer']:
            return utils.error_response("incomplete_offer_details")

        if not variables['customer']:
            return utils.error_response("incomplete_customer_details")

        if not variables['acceptedOffer']:
            return utils.error_response("incomplete_broker_details")

    else:
        event_id = utils.get_identifier(variables['orderedItem'][0]['orderedItem']['id'])
        offer_id = utils.get_identifier(variables['acceptedOffer'][0]['id'])
        event_data, event_error = models.Event(event_id).get()
        offer_data, offer_error = models.Offer(offer_id).get()

        if not event_error and not offer_error:

            quantity_of_order = int(variables['orderedItem'][0]['orderQuantity'])

            if utils.get_identifier(offer_data['itemOffered']['id']) != utils.get_identifier(event_data['id']):
                #EVENT DOES NOT MATCH OFFER
                return utils.error_response("offer_not_valid")

            if event_data['remainingAttendeeCapacity'] == 0:
                #EVENT IS FULL
                return utils.error_response("event_is_full")

            if event_data['remainingAttendeeCapacity'] < quantity_of_order:
                #EVENT HAS INSUFFICIENT SPACES
                return utils.error_response("event_has_insufficient_spaces")

            if utils.is_date_in_past(utils.from_datestring(event_data['startDate'])):
                # EVENT IS IN THE PAST
                logging.warn('EVENT IS IN THE PAST')
                return utils.error_response("unavailable_event")

            if utils.is_date_in_past(utils.from_datestring(offer_data['validThrough'])):
                # OFFER VALID THROUGH IS IN THE PAST
                logging.warn('VALID THROUGH IS IN THE PAST')
                return utils.error_response("offer_expired")

            if not utils.is_date_in_past(utils.from_datestring(offer_data['validFrom'])):
                # OFFER VALID FROM IS NOT YET IN THE PAST
                logging.warn('VALID FROM IS NOT THE PAST')
                return utils.error_response("offer_not_yet_valid")

            order = models.Order()

            variables['orderDate'] = datetime.now()
            variables['paymentDueDate'] = utils.add_time(datetime.now(), 15, 'M')

            value_of_order = offer_data['price'] * quantity_of_order
            currency_of_offer = offer_data['priceCurrency']

            variables['partOfInvoice'] = {
                "type": "Invoice",
                "paymentStatus": "PaymentDue",
                "totalPaymentDue": {
                  "type": "MonetaryAmount",
                  "value": value_of_order,
                  "currency": currency_of_offer
                }
            }

            order.create(variables)
            order_data, errors = order.get()
            order_id = order_data['identifier']

            order_summary = {
                'leaseExpiresAt': order_data['paymentDueDate'],
                'places': quantity_of_order
            }

            event_data['remainingAttendeeCapacity'] = event_data['remainingAttendeeCapacity'] - quantity_of_order
            event_data['orderLeases'][str(order_id)] = order_summary
            event = models.Event(event_id)
            event.update(event_data)

            return utils.json_response(order.as_json_ld(), created=True, created_key=order.as_json_ld()['id'].replace('$HOST$', ''))
        else:

            if event_error == 'resource_not_found':
                # EVENT NOT FOUND
                return utils.error_response("unavailable_event")

            if offer_error == 'resource_not_found':
                # OFFER NOT FOUND
                return utils.error_response("unavailable_offer")



@app.route("/events/<event_id>", methods=["GET"])
@app.route("/api/events/<event_id>", methods=["GET"])
#@utils.requires_auth
def get_event(event_id):
    data, error = models.Event(event_id).get()
    if not error:
        return utils.json_response(data)
    else:
        return utils.error_response(error)


@app.route("/offers/<offer_id>", methods=["GET"])
@app.route("/api/offers/<offer_id>", methods=["GET"])
#@utils.requires_auth
def get_offer(offer_id):
    data, error = models.Offer(offer_id).get()
    if not error:
        return utils.json_response(data)
    else:
        return utils.error_response(error)


@app.route("/orders/<order_id>", methods=["GET"])
@app.route("/api/orders/<order_id>", methods=["GET"])
@utils.requires_auth
def get_order(order_id):
    data, error = models.Order(order_id).get()
    if not error:
        return utils.json_response(data)
    else:
        return utils.error_response(error)


@app.route("/api/orders/<order_id>", methods=["PATCH"])
@utils.requires_auth
def update_order(order_id):
    order = models.Order(order_id)
    order.update({})
    return utils.json_response(order.as_json_ld())


@app.route("/api/orders/<order_id>", methods=["DELETE"])
@utils.requires_auth
def delete_order(order_id):
    order = models.Order(order_id)
    order.delete()
    return utils.json_response(order.as_json_ld())


### HANDLING ERRORS ###

# handling the disallowed verbs for the index route
@app.route("/", methods=["POST", "PUT", "PATCH", "DELETE"])
@utils.requires_auth
def index_error():
    return utils.error_response("method_not_allowed")


# handling the disallowed verbs for the rdpe route
@app.route("/api/rpde", methods=["POST", "PUT", "PATCH", "DELETE"])
@utils.requires_auth
def feed_error():
    return utils.error_response("method_not_allowed")


# handling the disallowed verbs for the orders collection route
@app.route("/api/orders", methods=["GET", "PUT", "PATCH", "DELETE"])
@utils.requires_auth
def create_order_error():
    return utils.error_response("method_not_allowed")


# handling the disallowed verbs for the orders item route
@app.route("/api/orders/<order_id>", methods=["POST", "PUT"])
@utils.requires_auth
def order_error(order_id):
    return utils.error_response("method_not_allowed")


# default error handling for 404, route not found
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
@utils.requires_auth
def default(path):
    return utils.error_response("not_found")


@app.cli.command()
def rebuild():
    manage = Manage(app)
    manage.reset_local_persistence()
    manage.build_clean_persistence()
    manage.populate_persistence()
