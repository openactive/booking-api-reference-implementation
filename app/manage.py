import os
import shutil
from datetime import datetime

from constants import LOCAL_PERSISTENCE
from constants import LOCAL_DATA

import models
import utils


class Manage():

    def __init__(self, app):
        self.app = app

    def reset_local_persistence(self):
        if self.check_folder_exists(LOCAL_PERSISTENCE['folder']):
            path = os.path.join(self.app.root_path, LOCAL_PERSISTENCE['folder'])
            shutil.rmtree(path)

    def check_folder_exists(self, folder):
        path = os.path.join(self.app.root_path, folder)
        if not os.path.isdir(path):
            return False
        else:
            return True

    def check_persistence_exists(self):
        if not self.check_folder_exists(LOCAL_PERSISTENCE['folder']):
            return False
        else:
            return True

    def add_folder(self, folder):
        path = os.path.join(self.app.root_path, folder)
        os.makedirs(path)

    def build_clean_persistence(self):
        if not self.check_persistence_exists():
            print('>> Building persistence folder structure')
            self.add_folder(LOCAL_PERSISTENCE['folder'])
            for model in LOCAL_PERSISTENCE['models']:
                folder_path = LOCAL_PERSISTENCE['folder'] + '/' + model
                self.add_folder(folder_path)
        pass

    def populate_persistence(self):
        print('>> Populating Data')
        print('>> Creating Events')
        today = datetime.today()
        for event_data in LOCAL_DATA['Events']:
            self.create_event(event_data, today)
        pass

    def create_event(self, event_data, today):
        identifier = event_data['identifier']
        event = models.Event(identifier=identifier)

        startTime = event_data['startTime'].split(':')
        adjusted_now = datetime(today.year, today.month, today.day,
                                int(startTime[0]), int(startTime[1]), int(startTime[2]))

        event_data['startDate'] = utils.add_time(
            adjusted_now, event_data['startDateDelta'], event_data['startDateDeltaType'])
        event_data['endDate'] = utils.add_time(
            event_data['startDate'], event_data['durationDelta'], event_data['durationDeltaType'])
        event_data['duration'] = 'PT' + \
            str(event_data['durationDelta']) + event_data['durationDeltaType']

        event_data['offers'] = []
        for offer_data in LOCAL_DATA['Offers']:
            offer = self.create_offer(
                offer_data, identifier, event_data['startDate'])
            del offer['@context']
            event_data['offers'].append(offer)

        event.create(event_data)

    def create_offer(self, offer_data, event_id, event_start_date):
        print(event_id)
        print(offer_data['identifier'])
        identifier = event_id + offer_data['identifier']

        offer_data['itemOffered'] = {
            "type": "Event",
            "id": "$HOST$/events/" + event_id
        }

        offer_data['validFrom'] = utils.add_time(
            event_start_date, offer_data['validFromDelta'], offer_data['validFromDeltaType'])
        offer_data['validThrough'] = utils.add_time(
            event_start_date, offer_data['validThroughDelta'], offer_data['validThroughDeltaType'])

        if offer_data['isCancellable']:
            offer_data['cancellationValidUntil'] = utils.add_time(
                event_start_date, offer_data['cancellationValidUntilDelta'], offer_data['cancellationValidUntilDeltaType'])

        offer = models.Offer(identifier=identifier)
        offer.create(offer_data)
        return offer.as_json_ld()
