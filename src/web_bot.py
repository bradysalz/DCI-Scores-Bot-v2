#!/usr/bin/env python3

import json
from typing import List, Dict, Tuple

import praw
import requests

from config import username, password, client_id, client_secret, show_file

BOT_INFO = (
    "*I'm a bot! Check me out on " +
    "[GitHub](https://github.com/bradysalz/DCI-Scores-Bot-v2)!" +
    " Please PM me with any additional feedback.* \n\n" + "*Hope you enjoy!*")

ORG_URL = 'http://bridge.competitionsuite.com/api/orgscores/GetCompetitionsByOrganization/jsonp'  # noqa
COMP_URL = 'http://bridge.competitionsuite.com/api/orgscores/GetCompetition/jsonp'  # noqa
DCI_API_ID = '96b77ec2-333e-41e9-8d7d-806a8cbe116b'


class WebBot(object):
    """Bot that interacts with the big world wide web.

    In reality, only goes on two sites:
        - dci.org, for parsing and checking for show updates
        - reddit.com, for posting said updates

    Primary functionality is parsing JSON information and formatting that to
    a markdown-based reddit post.
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

    def _parse_show_recap(self, show_rounds: List[Dict]) -> str:
        """Reads through show query and formats to a reddit post."""
        body_str = ''

        for _round in show_rounds:
            body_str += '## ' + _round['name'] + '\n\n'
            body_str += '[Full Recap Here](' + _round['fullRecapUrl'] + ')\n\n'

            body_str += 'Rank|Corp|Score\n'
            body_str += ':--|:--|:--\n'

            for perf in _round['performances']:
                body_str += '{}|{}|{:.2f}\n'.format(perf['rank'], perf['name'],
                                                    perf['score'])

            body_str += '\n\n---\n\n'

        body_str += '\n\n' + BOT_INFO
        return body_str

    def _parse_show_info(self, show_guid: str) -> Tuple[str, str]:
        """Pings show's GUID and returns the title and recap post.

        show_guid: an API GUID that corresponds to a certain show
        returns: a two-item tuple with the formatted title and reddit body
        """
        api_keys = {'competition': show_guid, 'callback': 'jQuery'}
        resp = requests.get(COMP_URL, params=api_keys)

        # Strip off jquery tags from the response string
        content = resp.content.decode('utf-8')
        show = json.loads(content[7:-2])

        title_str = '[Score Recap] ' + show['name'] + ' | ' + show['location']
        body = self._parse_show_recap(show['rounds'])
        return (title_str, body)

    def post_thread(self, show_info: Dict):
        """Submits a link-post to the specified subreddit.

        show_info: a Dict of all the JSON response info on the show
        """
        subr = self.conn.subreddit(self.subreddit)

        title, body = self._parse_show_info(show_info['competitionGuid'])
        subr.submit(title, selftext=body)

    def get_show_list(self) -> List[Dict]:
        """Scrapes the DCI.org API site and returns a list of shows"""
        api_keys = {'organization': DCI_API_ID, 'callback': 'jQuery'}

        resp = requests.get(ORG_URL, params=api_keys)
        content = resp.content.decode('utf-8')

        # Strip off jquery tags from the response string
        json_content = json.loads(content[7:-2])
        return json_content['competitions']
