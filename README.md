# ClutchTimeAlerts - NBA Clutch Time Alert Service
A service that tracks ongoing NBA games and sends alerts when games enter "clutch time"—the last five minutes of the fourth quarter or overtime when the point difference is five points or fewer. The serivce monitors live game data and sends notifications via configured messaging platforms (such as GroupMe, Slack, etc.) to keep you informed of the most intense moments.

## Features
- **Real-Time Clutch Detection**: Monitors live NBA game data and detects when games enter clutch time.
- **Customizable Alerts**: Configure the service to send alerts on various platforms (GroupMe, Slack, etc.).
- **Multiple Game Support**: Tracks multiple NBA games simultaneously to ensure you don't miss any clutch moments.

## Supported Notification Types

We currently support the following notification types out of the box:

- **GroupMe** 
- **Slack**

On our road map we want to expand the supported notification types. If there's a type you want to see supported add an issue or submit a PR for review.

## Installation 

**Python**
 
```sh
git clone git@github.com:bwalheim1205/clutchtimealerts.git
pip install clutchtimealerts
```

**Docker**

```sh
git clone git@github.com:bwalheim1205/clutchtimealerts.git
docker build clutchtimealerts/ -t clutchtimealerts
```

## Usage

**Python**

```sh
python3 -m clutchtimealerts -f <path-to-config>
```

**Docker**
```sh
docker run -v <path-to-config>:/app/config.yml clutchtimealerts
```