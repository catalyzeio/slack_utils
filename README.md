Catalyze Slackbot
=================

Catalyze Slackbot is a pretty simple bot to do useful things for our team.

## Project Setup
This is just a super simple API written with Falcon.

### Install dependencies
Use pip to install the project dependencies in `requirements.txt`.

### Environment Variables
There are only a couple required environment variables, they include:

```
PORT - The network port for the server to bind to.
UPDATES_WEBHOOK_URL - The Slack webhook URL for the Updates slash command.
COMMIT_HASH - (Optional) The Git commit hash to return in the heathcheck route.
```

## Slack Integrations
### Slash Commands

#### Daily Updates

##### Command

```
/updates {status}
```

##### Usage
You can post your daily updates with this command. Status items should be newline separated and each line should start with a `t:` for "today" (as in, "Today I plan on working on this..."), `y:` for "yesterday" (as in, "Yesterday I did this..."), and `b:` for "blockers" (as in, "Right now I'm blocked by this...").

##### Example

```
/updates
t: this is a today task
t: this is another today task
y: yesterday I did this
b: I'm blocked by this
```

