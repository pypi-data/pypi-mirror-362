import requests

from typing import Optional

from prefect import get_run_logger
from prefect.blocks.webhook import Webhook

class SlackWebhooksBlock:
    def __init__(self, environment, webhook_name):
        self.webhook_dev = webhook_name if webhook_name else "team-engineering-test-webhooks"
        self.webhook_prod = webhook_name if webhook_name else "team-data-alerts"
        self.environment = environment

    def get_webhook_block_name(self):
        """
        This function will return the webhook block name based on the environment.
        """
        return self.webhook_dev if self.environment == "dev" else self.webhook_prod


class SlackWebhooksNotification:
    def __init__(
            self,
            environment,
            slack_message,
            webhook_name: Optional[str] = None
        ):
        slack_block = SlackWebhooksBlock(environment=environment, webhook_name=webhook_name)
        slack_webhook = Webhook.load(slack_block.get_webhook_block_name())
        self.slack_webhook_url = slack_webhook.url.get_secret_value()
        self.slack_message = slack_message
        self.headers = {"Content-Type": "application/json"}

    def send_slack_json_message(self):
        """
        This function will send a JSON message to the Slack channel using the webhook URL.
        """
        logger = get_run_logger()

        response = requests.post(
            self.slack_webhook_url,
            json={"text": self.slack_message},
            headers=self.headers,
        )
        if response.status_code != 200:
            logger.warn(
                f"Error: response status code: {response.status_code} - error message: {response.text}"
            )
        return response

    def send_slack_data_message(self):
        """
        Ths function will send a data message to the Slack channel using the webhook URL.
        """
        logger = get_run_logger()
        response = requests.post(
            self.slack_webhook_url,
            data=self.slack_message,
            headers=self.headers,
        )
        if response.status_code != 200:
            logger.warn(
                f"Error: response status code: {response.status_code} - error message: {response.text}"
            )
        return response
