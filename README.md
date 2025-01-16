# ClutchTimeAlerts - NBA Clutch Time Alert Service

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![PyPI version](https://badge.fury.io/py/clutchtimealerts.svg)](https://badge.fury.io/py/clutchtimealerts)

A service that tracks ongoing NBA games and sends alerts when games enter "clutch time"—the last five minutes of the fourth quarter or overtime when the point difference is five points or fewer. The serivce monitors live game data and sends notifications via configured messaging platforms (such as GroupMe, Slack, etc.) to keep you informed of the most intense moments.

# Features
- **Real-Time Clutch Detection**: Monitors live NBA game data and detects when games enter clutch time.
- **Customizable Alerts**: Configure the service to send alerts on various platforms (GroupMe, Slack, etc.).
- **Multiple Game Support**: Tracks multiple NBA games simultaneously to ensure you don't miss any clutch moments.

# Supported Notification Types

We currently support the following notification types out of the box:

- **GroupMe** 
- **Slack**
- **Ntfy**
- **Twilio** (SMS)

On our road map we want to expand the supported notification types. If there's a type you want to see supported add an issue or submit a PR for review.

# Installation 

There are two different supported installation types: Python and Docker.

**Python**

To install the python package you can install it from [PYPI](https://pypi.org/project/clutchtimealerts/)

```sh
pip install clutchtimealerts
```

Alertnatively you can clone the repository then install it directly.
 
```sh
git clone git@github.com:bwalheim1205/clutchtimealerts.git
cd clutchtimealerts
pip install clutchtimealerts
```

**Docker**

To install via docker, you can pull image from [Docker Hub](https://hub.docker.com/repository/docker/bwalheim1205/clutchtimealerts):

```sh
docker pull bwalheim1205/clutchtimealerts
```


Alertnatively you can build the image from source:


```sh
git clone git@github.com:bwalheim1205/clutchtimealerts.git
docker build clutchtimealerts/ -t clutchtimealerts
```

# Usage

## Configuration File

The alert system utilizes a yaml configuration file. YAML contains configuration 
options for SQLite database and alert method configurations. Here is an example
of a configuration file

**Example Configuration**

```yaml
db_url: clutchtime.db
notifications:
  - type: GroupMe
    config:
      bot_id: "<group-bot-id>"
  - type: Slack
    config:
      channel: "#general"
      token: "<slack-api-token>"
  - type: Twilio
    config:
      account_sid: "<twilio-accout-sid>"
      auth_token: "<twilio-auth-token>"
      from: "+14155551212"
      to: 
        - "+14155551212"
        - "+14155551212"
  - type: Ntfy
    config:
      host: <ntfy host>
      topic: nba_alerts
      token: <Ntfy auth token>
```

### YAML Fields

**db_url** (__Optional__): DB url to sqlite3 database. Defaults to sqlite:///clutchtime.db

**notifications**: List of notification configs
-  **type**: class name or common name of the alert type
-  **config**: kwargs** for the alert classes


## Running Alert Service

Once you've generated a configuration file you can run alert service
using one of the following commands

**Python**

```sh
python3 -m clutchtimealerts -f <path-to-config>
```

**Docker**
```sh
docker run -v <path-to-config>:/app/config.yml clutchtimealerts
```