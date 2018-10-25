Flask + Celery Send Mail "Hello World"
======================================

The repo is the result of the attempts to run the code from the [Miguel's blog article](https://blog.miguelgrinberg.com/post/using-celery-with-flask).
That beautiful article is about 4 years old, so just to copy-paste and run did not work.
Sadly, the repo does not accept pull requests as well, so the code is here.

The repo provides the up to date code to run the Example1 i.e. to send email asynchronously with Celery.

  
The OS is `Ubuntu 16.04`, `Python3`, `pip3`.
The `Celery` broker is `Redis` (`sudo apt-get install redis-server`).

```bash
ubuntu@ubuntu-xenial:~/mail/app$ pip3 freeze
amqp==2.3.2
billiard==3.5.0.4
blinker==1.4
celery==4.2.1
chardet==2.3.0
Click==7.0
cloud-init==18.3
command-not-found==0.3
configobj==5.0.6
cryptography==1.2.3
Flask==1.0.2
Flask-Mail==0.9.1
idna==2.0
ItsDangerous==1.0.0
Jinja2==2.10
jsonpatch==1.10
jsonpointer==1.9
kombu==4.2.1
language-selector==0.1
MarkupSafe==1.0
oauthlib==1.0.3
prettytable==0.7.2
pyasn1==0.1.9
pycurl==7.43.0
pygobject==3.20.0
PyJWT==1.3.0
pyserial==3.0.1
python-apt==1.1.0b1+ubuntu0.16.4.2
python-debian==0.1.27
python-systemd==231
pytz==2018.6
PyYAML==3.11
redis==2.10.6
requests==2.9.1
six==1.10.0
ssh-import-id==5.5
ufw==0.35
unattended-upgrades==0.1
urllib3==1.13.1
vine==1.1.4
Werkzeug==0.14.1
```


For the mail server, the dummy one was used.
```python
app.config['MAIL_SERVER']='localhost'
app.config['MAIL_PORT'] = 8025
```
for the settings in the `app.py`. 
In the separate terminal window issue:

```bash 
ubuntu@ubuntu-xenial:~$ python3 -m smtpd -n -c DebuggingServer localhost:8025
```
This is window where the output mail will be shown, like:
```bash
---------- MESSAGE FOLLOWS ----------
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: Hello from Flask
From: me@foo.com
To: 56ain@foo.com
Date: Thu, 25 Oct 2018 11:51:38 +0000
Message-ID: <154046829860.7249.18123669423587656992@ubuntu-xenial>
X-Peer: 127.0.0.1

This is a test email sent from a background Celery task.
------------ END MESSAGE ------------
```

The `Celery` worker is issued from the same project dir in the another terminal window:
```bash 
ubuntu@ubuntu-xenial:~/mail/app$ celery -A app.celery  worker -E --loglevel=debug
```

The project structure as the follows:
```bash
ubuntu@ubuntu-xenial:~/mail/app$ tree -L 2
.
├── app.py
├── __pycache__
│   └── app.cpython-35.pyc
├── README.md
└── templates
    └── index.html
```

The project is being launched as:
```bash
ubuntu@ubuntu-xenial:~/mail/app$ python3 app.py
```
