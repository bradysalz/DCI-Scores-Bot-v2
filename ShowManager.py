#!/usr/bin/env python3

from typing import Dict

import pandas as pd
from pprint import pprint
from WebBot import WebBot
from config import show_file


class ShowManager(object):
    """Checks show lists for updates."""

    def __init__(self):
        self.bot = WebBot()
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

    def check_if_new_shows(self):
        """Compares online show list with self show list.
        
        If the show_file in config doesn't exist, it overwrites and creates
        the file. This WILL delete anything in that file, be careful!
        
        If a new show exists, it posts to reddit [/r/dci] with the
        appropriate info.
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
                pprint(show)
                self.bot.post_thread(show)
                self._add_show(show)

        self.shows.to_csv(show_file, index=False, header=False)
