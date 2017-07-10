#!/usr/bin/env python3

import json
import time
from typing import List, Dict, Tuple
from pprint import pprint
import praw
import requests

from config import username, password, client_id, client_secret, show_file

BOT_INFO = (
    "*I'm a bot! Check me out on " +
    "[GitHub](https://github.com/bradysalz/DCI-Scores-Bot)!" +
    " Please PM me with any additional feedback.* \n\n" + "*Hope you enjoy!*")

ORG_URL = 'http://bridge.competitionsuite.com/api/orgscores/GetCompetitionsByOrganization/jsonp'  # noqa
COMP_URL = 'http://bridge.competitionsuite.com/api/orgscores/GetCompetition/jsonp'  # noqa
DCI_API_ID = '96b77ec2-333e-41e9-8d7d-806a8cbe116b'


class WebBot(object):
    """Bot that interacts with the big world wide web.

    In reality, only goes on two sites:
        - dci.org, for parsing and checking for show updates
        - reddit.com, for posting said updates
    """

    def __init__(self, subreddit: str='dcicsstest'):
        self.show_file = show_file
        self.subreddit = subreddit
        self.__agent__ = 'python:dci-scores-tracker:2.0 (by /u/dynerthebard)'
        self.conn = None

    def connect(self):
        """Connects to reddit servers and logs in"""
        self.conn = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=self.__agent__,
            username=username,
            password=password)

    def _parse_show_info(self, show_info: Dict) -> List[Tuple[str, str]]:
        """Takes show's JSON response and returns the title and recap link."""
        comp_guid = show_info['competitionGuid']
        api_keys = {'competition': comp_guid, 'callback': 'jQuery'}
        resp = requests.get(COMP_URL, params=api_keys)

        # Strip off jquery tags from the response string
        content = resp.content.decode('utf-8')
        show = json.loads(content[7:-2])

        recaps = [rnd['categoryRecapUrl'] for rnd in show['rounds']]
        if len(recaps) > 1:
            return [(show['name'] + ' - ' + sh['name'], sh['categoryRecapUrl'])
                    for sh in show['rounds']]
        else:
            return [(show['name'], recaps)]

    def post_thread(self, show_info: Dict):
        """Submits a link-post to the specified subreddit.

        Also waits 15s, then comments with info about the bot. If people want
        I can change this to a self-post later.

        show_info: a Dict of all the JSON response info on the show
        """
        subr = self.conn.subreddit(self.subreddit)

        for title, link in self._parse_show_info(show_info):
            pprint(link)
            pprint(title)
            submission = subr.submit(title, url=link)
            time.sleep(15)

            submission.reply(BOT_INFO)
            time.sleep(45)

    def get_show_list(self) -> List[Dict]:
        """Scrapes the DCI.org API site and returns a list of shows"""
        api_keys = {'organization': DCI_API_ID, 'callback': 'jQuery'}

        resp = requests.get(ORG_URL, params=api_keys)
        content = resp.content.decode('utf-8')

        # Strip off jquery tags from the response string
        json_content = json.loads(content[7:-2])
        return json_content['competitions']
