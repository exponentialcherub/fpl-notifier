import requests
import logging

logger = logging.getLogger(__name__)

class NotifyApi(object):
    def __init__(self, url):
        self.url = url

    def notify(self, message):
        logger.info("Sending message to queue: " + self.url + "\n" + message)
        response = requests.post(self.url, json={"message": message})
        logger.info(response.text)