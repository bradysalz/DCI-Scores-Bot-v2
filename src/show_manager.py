#!/usr/bin/env python3

import time
from typing import Dict

import pandas as pd

from src.web_bot import WebBot
from config import show_file, subreddit


class ShowManager(object):
    """Checks show lists for updates."""

    def __init__(self):
        self.bot = WebBot(subreddit)
        self.shows = None

    def _add_show(self, show_info: Dict):
        """Adds a show to the current dataframe."""
        df = pd.DataFrame(
            {
                'Name': [show_info['name']],
                'Date': [show_info['competitionDate']],
                'GUID': [show_info['competitionGuid']],
            },
            columns=['Name', 'Date', 'GUID'])
        self.shows = self.shows.append(df)

    def check_if_new_shows(self, post: bool=True):
        """Checks for shows and posts to reddit if selected.

        post: if True, posts new shows to reddit

        If the show_file in config doesn't exist, it creates it and tries
        to run the script again.
        """
        try:
            self.shows = pd.read_csv(show_file, names=['Name', 'Date', 'GUID'])
        except FileNotFoundError:
            # If file doesn't exist, create w/header and redo
            with open(show_file, 'w') as f:
                f.write('Name,Date,GUID\n')
            self.check_if_new_shows()

        self.bot.connect()
        web_shows = self.bot.get_show_list()

        for show in web_shows:
            if show['competitionGuid'] not in self.shows.GUID.values:
                self._add_show(show)
                self.shows.to_csv(show_file, index=False, header=False)
                
                if post:
                    self.bot.post_thread(show)
                    print('Added {}'.format(show['name']))
                    time.sleep(9 * 60)  # Reddit API timeout
