from constants import LOCAL_PERSISTENCE
import json

import logging


class FileSystemProvider():

    def build_filepath(self, resource_type, resource_id):
        return LOCAL_PERSISTENCE['folder'] + '/' + resource_type + '/' + resource_id + '.json'

    def get_file_handle(self, resource_type, resource_id, mode):
        return open(self.build_filepath(resource_type, resource_id), mode)

    def create(self, resource_type, resource_id, variables):
        _file = self.get_file_handle(resource_type, resource_id, 'w')
        pass

    def read(self, resource_type, resource_id):
        data = None
        error = None
        try:
            _file = self.get_file_handle(resource_type, resource_id, 'r')
        except:
            error = 'not_found'
        if not error:
            try:
                data = json.loads(_file.read())
            except:
                error = 'server_error'

        return data, error

    def update(self, resource_type, resource_id, variables):
        _file = self.get_file_handle(resource_type, resource_id, 'w')
        pass

    def delete(self, resource_type, resource_id):
        pass
