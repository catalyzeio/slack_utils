"""
Slack Daily Updates
"""
import falcon
import json
import logging
import requests
import os

logging.basicConfig()


class Updates(object):
    """
    API route for the custom Slack slash command: /updates
    """
    def __init__(self, webhook_url):
        super(Updates, self).__init__()
        self.webhook_url = webhook_url

    @staticmethod
    def build_slack_message(username, updates):
        """
        Takes raw updates text and makes a pretty Slack formatted message.
        """
        today = []
        yesterday = []
        blockers = []
        other = []
        for line in updates.splitlines():
            status = line.split(':', 1)
            if len(status) > 1:
                status_type = status[0].strip().lower()
                status_text = ':'.join(status[1:]).strip()

                if status_type == 't':
                    today.append(status_text)
                elif status_type == 'y':
                    yesterday.append(status_text)
                elif status_type == 'b':
                    blockers.append(status_text)
                else:
                    other.append(status_text)
            else:
                other.append(status)

        message = {
            'icon_url': 'https://catalyze.io/favicon.png',
            'username': 'Updates: {}'.format(username),
            'attachments': []
        }
        if len(today) > 0:
            message['attachments'].append({
                'fallback': 'Today: {}'.format(', '.join(today)),
                'title': 'Today',
                'text': '\n'.join('- {}'.format(t) for t in today)
            })
        if len(yesterday) > 0:
            message['attachments'].append({
                'fallback': 'Yesterday: {}'.format(', '.join(yesterday)),
                'title': 'Yesterday',
                'text': '\n'.join('- {}'.format(y) for y in yesterday),
            })
        if len(blockers) > 0:
            message['attachments'].append({
                'fallback': 'Blockers: {}'.format(', '.join(blockers)),
                'title': 'Blockers',
                'text': '\n'.join('- {}'.format(b) for b in blockers),
            })
        return message

    @staticmethod
    def post_to_slack(webhook_url, message_json):
        """
        Posts a message to the Slack webhook.
        """
        resp = requests.post(webhook_url, data=json.dumps(message_json))
        logging.getLogger().info('Response:', resp.status_code, ' -', resp.text)
        return resp

    def on_post(self, req, resp):
        """
        Handles incoming web hooks for the "updates" Slack slash command.
        """
        if req.content_length in (None, 0):
            # Nothing to do
            return

        body = req.stream.read()
        if not body:
            raise falcon.HTTPBadRequest('Empty request body',
                                        'A valid JSON document is required.')

        data = dict(line.split('=', 1) for line in body.splitlines())
        message = self.build_slack_message(data['user_name'], data['text'])
        self.post_to_slack(self.webhook_url, message)
        resp.status = falcon.HTTP_200
        resp.body = ''


class HealthCheck(object):
    """
    API route for health checking
    """
    @staticmethod
    def status():
        """
        Returns system status JSON object (dict)
        """
        status = {"status": "ok"}
        if 'COMMIT_HASH' in os.environ:
            status['git'] = os.environ['COMMIT_HASH']
        return status

    def on_get(self, req, resp):
        """
        Handles requests for health check status.
        """
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(self.status(), indent=4)


def api():
    """
    Creates the API
    """
    updates_webhook_url = os.environ['UPDATES_WEBHOOK_URL']
    app = falcon.API()
    app.add_route('/updates', Updates(updates_webhook_url))
    app.add_route('/healthcheck', HealthCheck())
    return app

