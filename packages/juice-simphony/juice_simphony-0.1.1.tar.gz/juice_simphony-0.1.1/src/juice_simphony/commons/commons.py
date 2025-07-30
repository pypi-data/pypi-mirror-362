# *************************************************************************** #
# This file is subject to the terms and conditions defined in the             #
# file 'LICENSE.txt', which is part of this source code package.              #
#                                                                             #
# No part of the package, including this file, may be copied, modified,       #
# propagated, or distributed except according to the terms contained in       #
# the file 'LICENSE.txt'.                                                     #
#                                                                             #
# (C) Copyright European Space Agency, 2025                                   #
# *************************************************************************** #
import json
import os
from os import path

class file_location():

    # file_name
    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, file_name):
        self._file_name = file_name

    # file_path
    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, file_path):
        self._file_path = file_path

    # file_full_path
    @property
    def file_full_path(self):
        if self._file_full_path.empty():
            return os.path.normpath(os.path.join(self._file_path,self._file_name))
        return self._file_full_path

    @file_full_path.setter
    def file_full_path(self, file_full_path):
        self._file_full_path = file_full_path
        self._file_name = os.path.basename(self._file_full_path)
        self._file_path = os.path.dirname(self._file_full_path)


class config_file(file_location):
    _content = {}

    def __getitem__(self, key):
        return self._content[key]

    def __setitem__(self, key, value):
        self._content[key] = value

    def parse_json(self):
        with open(self.file_full_path) as json_file:
            self._content = json.load(json_file)

    def write_json(self):
        if bool(self._content):
            with open(self.file_full_path, 'w') as outfile:
                json.dump(self._content, outfile, indent=4)
