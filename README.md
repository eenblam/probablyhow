# probablyHow
probablyHow is a terrible markov chain app that aggregates wikiHow articles
by leveraging [bleeding edge](https://github.com/jsvine/markovify) [AI](https://imgur.com/ZeSy3Zu)
to bring you the best instructional content you never wanted.

probablyHow is available as a hosted [Flask application](https://probablyhow.herokuapp.com)
and as a command-line client.

Created by [@eenblam](https://github.com/eenblam) and [@squigglydonut](https://github.com/squigglydonut)
for the 2017 [Stupid Shit No One Needs & Terrible Ideas Hackathon](http://www.stupidhackathon.com/)
hosted at [NoiseBridge](https://noisebridge.net).

## Installation
You should probably use a [virtual environment](https://virtualenv.pypa.io/en/stable/)
or [something](https://conda.io/docs/using/envs.html).
Maybe it works with Python 3, maybe it doesn't.

```bash
git clone https://github.com/eenblam/probablyhow.git
cd probablyhow
python setup.py install
```

## Command Line Usage
Here are some actual examples that we've gotten back from the model.

```bash
$ howto turn off a banana
1: First, using a spatula.
2: Add the mashed bananas.
3: For some people, a banana until it is beaten.
4: Remove from the freezer.
5: Pack a lunch and strike out for a long time even if they are working on.
6: If you are not bad for you, but many people are bound to have a bitter taste and consistency.
7: Pinch just behind the blossom end to break it apart, then peel bits of it as it is, or you can use a spoon or spatula is too dry and crumbly, spritz it with a spiky decorators tip.
8: Make sure that the thinness determines the final two minutes, to avoid burning the banana first, then add it to a year.

$ howto hack the planet
1: Enter values next to any other resources you want to give them your email so they may be required to log in yet!
2: Put in your browser.
3: Hack tools developed for Head Soccer using an online hack tools may be banned or suspended at any time for failing to adhere to the menu immediately.
4: You may also comment on the Ultimate Free Cheats site to limit downloads on the Head Soccer hack tool to work.
5: In general, these are the only options you can enter your email if you want added to your account.
6: It may also be because the information you can unblock them if you experience difficulty with accessing surveys or access Head Soccer offers unlimited points throughout gameplay.
7: A backup account is like a second account that you use an Android device, you can access without having the door closed is limited and fairly harmless . In order to get it back and how to avoid losing your account.
8: This will help you when you forget your password.
```

## Web Server
To run the Flask application locally, run the following after following the above installation steps:

```bash
cd probablyhow
export FLASK_APP=app.py
flask run
```

Note that this is rather slow because:
1. A number of round trips are needed to fetch the training data,
as WikiHow only supports the bare minimum of the MediaWiki API offerings.
2. Each request generates a new Markov model, even if you just refresh the page.
