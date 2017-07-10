#!/usr/bin/env python3

import json
from typing import List, Dict

import requests

COMP_URL = 'http://bridge.competitionsuite.com/api/orgscores/GetCompetitionsByOrganization/jsonp'  # noqa
DCI_API_ID = '96b77ec2-333e-41e9-8d7d-806a8cbe116b'


class WebCrawler(object):
    """Crawls dci.org/scores and fetches scores.

    Currently just saves show IDs to a local textfile, but later will
    use a database for historical reasons.
    """

    def __init__(self, show_file: str):
        self.show_file = show_file

    def get_show_list(self) -> List[Dict]:
        """Scrapes the DCI.org API site and returns a list of shows"""
        api_keys = {'organization': DCI_API_ID, 'callback': 'jQuery'}

        resp = requests.get(COMP_URL, params=api_keys)
        content = resp.content.decode('utf-8')

        # Strip off jquery tags from the response string
        json_content = json.loads(content[7:-2])
        competitions = json_content['competitions']

        return competitions

    # TODO: Add parsing.... or not. Was a bore last time.
