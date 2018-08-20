import os
import shutil


persistence_structure = {
    "folder": "local_data",
    "contains": [
        {"folder": "events"},
        {"folder": "offers"},
        {"folder": "orders"}
    ]
}


class Manage():

    def __init__(self, app):
        self.app = app

    def reset_local_persistence(self):
        if self.check_folder_exists(persistence_structure['folder']):
            path = os.path.join(self.app.root_path, persistence_structure['folder'])
            shutil.rmtree(path)

    def check_folder_exists(self, folder):
        path = os.path.join(self.app.root_path, folder)
        if not os.path.isdir(path):
            return False
        else:
            return True

    def check_persistence_exists(self):
        if not self.check_folder_exists(persistence_structure['folder']):
            return False
        else:
            return True

    def add_folder(self, folder):
        path = os.path.join(self.app.root_path, folder)
        os.makedirs(path)


    def build_clean_persistence(self):
        if not self.check_persistence_exists():
            print('>> Building persistence folder structure')
            self.add_folder(persistence_structure['folder'])
            for folder in persistence_structure['contains']:
                folder_path = persistence_structure['folder'] + '/' + folder['folder']
                self.add_folder(folder_path)
        pass

    def populate_persistence(self):
        print('>> Populating data')
        pass
