#!/usr/bin/env python3

import sys

from ShowManager import ShowManager


def run(post: bool):
    sm = ShowManager()
    sm.check_if_new_shows(post)


if __name__ == '__main__':
    if len(sys.argv) > 2:
        print('Valid run methods are: "./main.py" and "./main.py post"')
        sys.exit(1)

    if sys.argv[1] == 'post':
        run(True)
    else:
        run(False)
