import click
from flask import Flask
import random

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
def index():
    return utils.json_response({'message':'Hello'})


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
        utils.clean_expired_leases(event_id)


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
                return utils.error_response("unavailable_event")

            if utils.is_date_in_past(utils.from_datestring(offer_data['validThrough'])):
                # OFFER VALID THROUGH IS IN THE PAST
                return utils.error_response("offer_expired")

            if not utils.is_date_in_past(utils.from_datestring(offer_data['validFrom'])):
                # OFFER VALID FROM IS NOT YET IN THE PAST
                return utils.error_response("offer_not_yet_valid")

            order = models.Order()

            variables['orderDate'] = datetime.now()
            variables['paymentDueDate'] = utils.add_time(datetime.now(), 15, 'M')

            value_of_order = offer_data['price'] * quantity_of_order
            currency_of_offer = offer_data['priceCurrency']

            variables['partOfInvoice'] = {
                "type": "Invoice",
                "paymentStatus": "https://schema.org/PaymentDue",
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
    utils.clean_expired_leases(event_id)
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
#@utils.requires_auth
def get_order(order_id):
    data, error = models.Order(order_id).get()
    if not error:
        if data['orderStatus'] == "https://schema.org/OrderPaymentDue" and utils.is_date_in_past(utils.from_datestring(data['paymentDueDate'])):
            return utils.error_response('anonymous_lease_expired')
        else:
            return utils.json_response(data)
    else:
        return utils.error_response(error)


@app.route("/api/orders/<order_id>", methods=["PATCH"])
@utils.requires_auth
def update_order(order_id):
    order_data, error = models.Order(order_id).get()

    if error:
        return utils.error_response(error)
    else:
        event_id = utils.get_identifier(order_data['orderedItem'][0]['orderedItem']['id'])

        params = ['payments', 'orderedItem']
        variables, erroring_params, error = utils.request_variables(params)

        if params == erroring_params:
            return utils.error_response('insufficient_information')

        if [param for param in variables] == params:
            return utils.error_response('too_much_information')

        if 'payments' in variables and variables['payments'] is not None:
            # PAYMENT FLOW
            if utils.is_date_in_past(utils.from_datestring(order_data['paymentDueDate'])):
                # LEASE HAS EXPIRED
                # TODO delete the expired lease and release the places
                #utils.clean_expired_leases(event_id)
                return utils.error_response("anonymous_lease_expired")

            if variables['payments'][0]['totalPaidToProvider']['value'] != order_data['partOfInvoice']['totalPaymentDue']['value']:
                return utils.error_response("payment_amount_incorrect")

            if variables['payments'][0]['totalPaidToProvider']['currency'] != order_data['partOfInvoice']['totalPaymentDue']['currency']:
                return utils.error_response("currency_incorrect")

            if order_data['orderStatus'] != "https://schema.org/OrderPaymentDue":
                return utils.error_response("order_cannot_be_completed")

            order_data['payments'] = variables['payments']
            order_data['orderStatus'] = 'https://schema.org/OrderDelivered'
            order_data['potentialAction'] = [{
                "type": "CancelAction",
                "name": "Cancel",
                "target": {
                    "type": "EntryPoint",
                    "urlTemplate": "https://example.com/orders/{order_id}",
                    "encodingType": "application/vnd.openactive.v1.0+json",
                    "httpMethod": "PATCH"
                }
            }]
            order_data['orderedItem'][0]['orderItemStatus'] = 'https://schema.org/OrderDelivered'
            order_data['partOfInvoice']['paymentStatus'] = 'https://schema.org/PaymentComplete'
            order_data['payments'][0]['confirmationNumber'] = 'C' + str(random.randint(0, 100000))

            order = models.Order(order_id)
            order.update(order_data)

            event_data, error = models.Event(event_id).get()

            # Remove used lease from Event

            order_summary = event_data['orderLeases'][str(order_id)]
            del event_data['orderLeases'][str(order_id)]
            del order_summary['leaseExpiresAt']

            # Add completed order to event

            order_summary['orderCompletedAt'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            event_data['completedOrders'][str(order_id)] = order_summary

            event = models.Event(event_id)
            event.update(event_data)

            return utils.json_response(order.as_json_ld())
        else:
            # CANCELLATION FLOW
            offer_id = utils.get_identifier(order_data['acceptedOffer'][0]['id'])

            offer_data, error = models.Offer(offer_id).get()

            if order_data['orderStatus'] != "https://schema.org/OrderDelivered":
                return utils.error_response("order_cannot_be_cancelled")

            if offer_data['isCancellable'] == False:
                return utils.error_response("order_is_uncancellable")

            if offer_data['isCancellable'] == True and utils.is_date_in_past(utils.from_datestring(offer_data['cancellationValidUntil'])):
                return utils.error_response("order_cancellation_window_expired")

            order_data['orderedItem'][0]['orderItemStatus'] = 'https://schema.org/OrderCancelled'
            order_data['orderStatus'] = 'https://schema.org/OrderCancelled'

            order = models.Order(order_id)
            order.update(order_data)

            quantity_of_order = int(order_data['orderedItem'][0]['orderQuantity'])

            event_data, error = models.Event(event_id).get()
            event_data['remainingAttendeeCapacity'] = event_data['remainingAttendeeCapacity'] + quantity_of_order
            del event_data['completedOrders'][str(order_id)]

            event = models.Event(event_id)
            event.update(event_data)

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
