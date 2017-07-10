#!/usr/bin/env python3

import time

import praw

from config import username, password, client_id, client_secret

BOT_INFO = (
    "*I'm a bot! Check me out on" +
    "[GitHub](https://github.com/bradysalz/DCI-Scores-Bot)!" +
    " Please PM me with any additional feedback.* \n\n" + "*Hope you enjoy!*")


class RedditBot(object):
    """Bot that posts scores to reddit."""

    def __init__(self, subreddit: str='dcicsstest'):
        self.subreddit = subreddit
        self.__agent__ = 'python:dci-scores-tracker:2.0 (by /u/dynerthebard)'
        self.conn = None

    def connect(self):
        """Connects to reddit servers and logs in"""
        print(client_id)
        print(client_secret)
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
