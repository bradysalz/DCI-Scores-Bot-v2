#!/usr/bin/env python3

import sys

from src.show_manager import ShowManager


def run(post: bool):
    sm = ShowManager()
    sm.check_if_new_shows(post)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        run(False)
    elif sys.argv[1] == 'post':
        run(True)
    else:
        print('Valid run methods are: "./main.py" and "./main.py post"')
        sys.exit(1)
