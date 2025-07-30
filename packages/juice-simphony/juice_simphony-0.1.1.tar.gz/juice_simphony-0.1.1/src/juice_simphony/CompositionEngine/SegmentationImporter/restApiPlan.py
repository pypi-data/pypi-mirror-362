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
from __future__ import annotations
import json
from requests import session

SUCCES_RESPONSE = 200

class RestApiPlan:
    def __init__(self, server_url: str):
        self.session = session()
        self.server_url = server_url.rstrip("/") + "/"

    def __get_json(self, endpoint: str):
        response = self.session.get(self.server_url + endpoint)
        if response.status_code != SUCCES_RESPONSE:
            raise RestApiError(response.text)
        return response.json()

    def __get_file(self, file_path: str):
        response = self.session.get(file_path)
        if response.status_code != SUCCES_RESPONSE:
            raise RestApiError(file_path)
        return response.text

    def get_segment_definitions(self, trajectory: str):
        return self.__get_json("plan")

    def get_file(self, file_path: str):
        return self.__get_file(file_path)

    def get_events(self, trajectory: str, mnemonic: str):
        body = {
            "trajectory": trajectory,
            "mnemonic": mnemonic
        }
        endpoint = f"events/?body={json.dumps(body)}"
        return self.__get_json(endpoint)

    def get_trajectory(self, trajectory: str, mnemonic: str = None):
        data = self.__get_json("plan")
        # Filter by trajectory and optionally mnemonic
        filtered = [
            item for item in data
            if item["trajectory"] == trajectory and
               (mnemonic is None or item["mnemonic"] == mnemonic)
        ]
        return filtered

class RestApiError(Exception):
    pass
