from constants import LOCAL_PERSISTENCE
import json
import random

import logging


class FileSystemProvider():

    def build_filepath(self, resource_type, resource_id):
        return LOCAL_PERSISTENCE['folder'] + '/' + resource_type + '/' + resource_id + '.json'

    def get_file_handle(self, resource_type, resource_id, mode):
        return open(self.build_filepath(resource_type, resource_id), mode)

    def get_unique_id(self, resource_type):
        resource_id = str(random.randint(0, 10000))
        is_unique = False
        try:
            self.get_file_handle(resource_type, resource_id, 'r')
        except:
            is_unique = True
        if is_unique:
            return resource_id
        else:
            return self.get_unique_id(resource_type)

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

    def write(self, resource_type, resource_id, content):
        error = None
        try:
            _file = self.get_file_handle(resource_type, resource_id, 'w')
            _file.write(content)
            _file.close()
        except:
            error = 'server_error'
        return error

    def delete(self, resource_type, resource_id):
        pass
