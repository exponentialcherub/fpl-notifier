import json

import requests
import logging

from config.config import QueueConfig

logger = logging.getLogger(__name__)

class QueueApi(object):
    def __init__(self, queue_config: QueueConfig):
        self.queue_domain = queue_config.domain
        self.consume_url = f"{queue_config.domain}/consume/{queue_config.consume_subject}"
        self.notify_subject = queue_config.notify_subject

    def consume(self):
        response = requests.get(self.consume_url)
        response_json = requests.get(self.consume_url).json()

        if "status" in response_json and response_json["status"] == "empty":
            return None

        logger.info(f"Message found on queue: {self.consume_url}\n" + response.text)
        return response_json

    def publish(self, subject, message):
        push_url = f"{self.queue_domain}/publish/{subject}"
        logger.info("Sending message to queue: " + push_url + "\n" + message)
        response = requests.post(push_url, json={"message": message})
        logger.info(response.text)

    def notify(self, message):
        self.publish(self.notify_subject, message)
