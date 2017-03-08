# Introduction
Pagemail is a system for tracking email views by emailing out links to hosted content. It was built for some friends who were worried that email they sent was being intercepted and read.


# Warnings and disclaimers
Unlike most projects, the code here is simple and it's the setup that's complicated. I attempted to document the setup process, but may have inadvertently left exercises for the reader. This has only been tested on [Debian](https://www.debian.org) Jessie. The web page isn't well-styled, and I can't think of a real-world use case.


# Setup
Besides installing the appropriate software packages, you'll need to:
* Install [Apache](https://httpd.apache.org)
* Install [sudo](https://www.sudo.ws)
* Set up a Python [virtual environment](https://virtualenv.pypa.io/en/stable/). You can initialize one with `virtualenv venv`, then work on it by `source venv/bin/activate`.
* Install the required packages into that virtual environment:
  * [Flask](http://flask.pocoo.org) (`pip install flask`)
  * The latest [pybrowscap](https://github.com/char0n/pybrowscap)
    * `git clone https://github.com/char0n/pybrowscap.git`
    * `pip install ./pybrowscap`
* Download the latest [browscap](https://browscap.org) csv:
  * `curl -o browscap.csv https://browscap.org/stream\?q\=BrowsCapCSV`
* Set up the wsgi and the apache vhost config ([example wsgi](pagemail.wsgi), [example vhost](doc/apache-sites/pagemail-ssl.conf))
* Add the role user to the system: `adduser --shell /usr/sbin/nologin --disabled-login --disabled-password pagemail`
* Add the sudo definition so mail can deliver to the role user:
  * `visudo -f /etc/sudoers.d/pagemail` (add [this content](doc/sudoers.d-pagemail))
* Add a pipe to your /etc/aliases, run `newaliases` afterwards (add [this content](doc/aliases))
* Make sure pagemail owns the pagemail web directory (otherwise, sqlite will crash)
* Edit the config, especially the master secret


# Configuration
While the configuration file at [pagemail.conf](/pagemail.conf) has comments, most of the other configuration files don't, and the interaction between the those files may not be obvious.

### Minimum changes to get running
Edit your `email_address`, `senders_list`, `sender_replacements`, `domain` and `cookie_secret`.

### Changing filesystem locations
Various filesystem locations are in the Apache config, the .wsgi, the aliases entry and the sudo script. If you're moving anything, be careful to update matching lines in other configuration files.

### Changing role user's account name
The role user's name is built into the Apache config, the aliases entry and the sudoers script (and this documentation). You'll need to change all of those at once (as well as chown the directory) to use another user.
