#!/usr/bin/env python3

import json
import time
from typing import List, Dict

import praw
import requests

from config import username, password, client_id, client_secret

BOT_INFO = (
    "*I'm a bot! Check me out on" +
    "[GitHub](https://github.com/bradysalz/DCI-Scores-Bot)!" +
    " Please PM me with any additional feedback.* \n\n" + "*Hope you enjoy!*")

COMP_URL = 'http://bridge.competitionsuite.com/api/orgscores/GetCompetitionsByOrganization/jsonp'  # noqa
DCI_API_ID = '96b77ec2-333e-41e9-8d7d-806a8cbe116b'


class WebBot(object):
    """Bot that interacts with the big world wide web.

    In reality, only goes on two sites:
        - dci.org, for parsing and checking for show updates
        - reddit.com, for posting said updates
    """

    def __init__(self, show_file: str, subreddit: str='dcicsstest'):
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

    def post_thread(self, title: str, link: str):
        """Submits a link-post to the specified subreddit.

        Also waits 15s, then comments with info about the bot. If people want
        I can change this to a self-post later.

        title: title of the submission
        link: link to DCI Scores show-specific recap
        """
        subr = self.conn.subreddit(self.subreddit)
        submission = subr.submit(title, url=link)

        time.sleep(15)
        submission.reply(BOT_INFO)

    def get_show_list(self) -> List[Dict]:
        """Scrapes the DCI.org API site and returns a list of shows"""
        api_keys = {'organization': DCI_API_ID, 'callback': 'jQuery'}

        resp = requests.get(COMP_URL, params=api_keys)
        content = resp.content.decode('utf-8')

        # Strip off jquery tags from the response string
        json_content = json.loads(content[7:-2])
        competitions = json_content['competitions']

        return competitions
