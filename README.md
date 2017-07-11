## DCI-Scores-Bot-v2
Round two on creating a DCI Scores bot for [/r/drumcorps](https://reddit.com/r/drumcorps). The last one was OK, but I spent way too much time messing around with trying to parse their awful HTML tables. This time, we just post the top scores and links to the full recap, for people to read at their discretion. 


### Getting Started

First, [register an app](https://ssl.reddit.com/prefs/apps) with Reddit. Choose `personal use script` as the type. 

Then check out the repo and install the requirements. I recommend using [`virtualenv`](https://virtualenv.pypa.io/en/stable/) or something similar. Install reqs:

```
pip install -r requirements.txt
```

After that, edit `config.py` with your information.

- `username` : reddit account username
- `password` : reddit account password
- `client_id`: reddit app ID
- `client_secret`: reddit app secret code
- `show_file`: CSV-file where you want to store the store list. Defaults to `shows.csv`
- `subreddit`: name of subreddit to post to (no /r/ needed). Defaults to `drumcorps` 


### Running The Bot

You run the bot with `main.py`. By default, the bot will only update it's own show list and not post anything. It is **highly recommended** you do this the first time you run the bot, as there will likely be a large number of shows that you will just be spamming somewhere. 

Run `main.py post` to post all new shows to reddit. If multiple new shows are found, it waits 8 minutes to ensure there we don't get blocked from reddit for spam. 

I run the bot with a cronjob using the `update_shows.sh` script, but you can use whatever job manager you'd like. 

### Tests

TBD...

### Contributing

Make an issue, PR, etc. For style, please use `yapf` and `flake8` for formatting and linting respectively. Both included in `requirements.txt`. 

### License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
