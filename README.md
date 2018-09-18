# Booking API Reference Implementation

## What is this?

It is a lightweight reference implementation of the Open Active Booking API Specification (v1.0). It is designed to be something that could be run locally as a simple datasource for developing/testing a **broker** application, simulating the **booking system**.

## Aims

It aims to simulate a set of standard conditions when booking spaces on **opportunities**. It simulates the **leases** created during the booking process, cancellable and uncancellable **offers**, cancellation windows, and the completion of **orders**
where a **broker** notifies the **booking system** that they have taken **payment** from a customer.

## How do I run it?

It is a self contained Flask application with minimal imports which uses the filesystem as a datastore (this has the advantage of reducing the number of moving parts to install/set up). On startup it creates a minimal set of Events and Offers which can be
then used to create Orders. All of these created objects can be seen via the API and also in the filesystem objects contained in a
local_data folder which is created.

## What can I do with it?

## What conditions does it simulate?

It simulates the following conditions:

- Successful Order Creation
- Successful Payment
- Successful Cancellation

Event related error conditions:
- events which are full (0 remainingAttendeeCapacity)
- events which do not have enough spaces required for the order
- events which cannot yet be booked
- events which are in the past
- events which don't exist

Offer related error conditions:
- offers which are not yet valid
- offers which have expired
- offers which don't exist
- mismatch of offer and event

Order related error conditions
- missing customer details
- missing broker details
- missing order item (the event required and number of places)
- missing accepted offer (the offer chosen by the customer)
- expiry of the anonymous lease

Payment related error conditions
- no payment information provided
- wrong payment amount (payment amount not matching invoice amount)
- wrong payment currency (payment currency not matching invoice currency)

Cancellation related error conditions
- uncancellable offers
- offers which could not be cancelled as the cancellation window had expired
- orders which are in an uncancellable state (i.e. an order which is not in OrderDelivered)

It simulates
- GET requests for Events, Offers, Orders
- POST requests for creating Orders 
- PATCH requests for updating Orders (notifying payment/cancelling an order)


## What does it not do in its current implementation?

It currently does not do the following things:

- simulate or emulate an RDPE feed
- validation of inputs against the Open Active data model (other tools are available for this)
- simulation of opportunities other than events (Facility Use/Slots)
- simulation of events with subEvents and schedules

## Installation/setup instructions

First install Python. Python 3.6 or higher is known to work.

Clone or download this repository.

Change directory to the downloaded directory.

Create a virtual environment for the project

`virtualenv -p python3 env`

Activate the virtual environment

`source activate env`

or

`source env/bin/activate`

Depending on how you have installed Python.

You will then need to install the minimal dependencies in your newly activated environment.

`pip install -r requirements.txt`

Now change directory to the `app` directory.

Run the script to start the Flask app. There are two versions of this. One will create a clean local data environment with a sample set of events and offers.

`source ../scripts/clean_run_flask.sh`

The other one will use a pre-existing set of data in case you wish to keep using the data environment you've already interacted with but have had to stop Flask for some reason.

`source ../scripts/run_flask.sh`

Visiting the application in a browser will result in a JSON return, instructing you that

http://localhost:5000/

## Authentication

All of the API calls, except for the welcome message are protected. The API can be authenticated against in two ways:

- passing a set of Basic Auth credentials
  - username : openactive
  - password : UsingDataToHelpPeopleGetActive

- providing an API key (rr4nlnyhi3tdoonxfysi) in the 'x-api-key' header

## Accept Headers/Content Type

All data provided to and returned by the API is in a JSON-LD format conforming to the Open Active schema (Modelling Specification version 2.0 / Booking API Version 1.0). This includes all error messages.

Data sent to the API should include an 'Accept' header, set to 'application/vnd.openactive.v1.0+json'

## Errors

## What's in the sample data?



## Examples


```json
{
	"@context": "https://openactive.io/ns/oa.jsonld",
	"type": "Order",
	"broker": {
		"type": "Organization",
		"name": "MyFitnessApp",
		"url": "https://myfitnessapp.example.com"
	},
	"customer": {
		"type": "Person",
		"email": "geoffcapes@example.com",
		"givenName": "Geoff",
		"familyName": "Capes"
	},
	"acceptedOffer": [{
		"type": "Offer",
		"id": "http://localhost:5000/offers/12341"
	}],
	"orderedItem": [{
		"orderQuantity": "1",
		"orderedItem": {
			"type": "Event",
			"id": "http://localhost:5000/events/1234"
		}
	}]
}
```
