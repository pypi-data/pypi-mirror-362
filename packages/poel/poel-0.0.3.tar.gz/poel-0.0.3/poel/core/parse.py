# -*- coding: UTF-8 -*-

import requests
from pofile import get_files

from poel.lib.config import easylink_parse_url, staus_url


class parse():
    def __init__(self, api_key):
        self.url = easylink_parse_url
        self.api_key = api_key

    def parse_files(self, file_list, mode=None, url=None):
        """
        来自：https://docs.easylink-ai.com/easydoc/quick-start/restful-api
        """
        url = self.url if url is None else url
        headers = {
            "api-key": self.api_key
        }
        pre_files = get_files(file_list)
        files = []
        for file in pre_files:
            files.append(("files", open(file, "rb")))

        data = {
            "mode": "lite" if mode is None else mode
        }

        response = requests.post(url, headers=headers, files=files, data=data)
        j = response.json()
        task_id = response.json()['data']['task_id']
        return self.get_status_code(task_id)

    def get_status_code(self, task_id):
        url = f"{staus_url}{task_id}"
        headers = {
            "api-key": self.api_key
        }

        status = False
        results = None
        while status is False:
            response = requests.get(url, headers=headers)
            if response.json()['data']['status'] == 'SUCCESS':
                status = True
                results = response.json()['data']['results']
        else:
            return results
