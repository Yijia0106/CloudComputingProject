import logging
import time


class SimpleMiddleWare(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        start_time = time.time()
        response = self.app(environ, start_response)
        logging.getLogger().info(f"The response takes {time.time() - start_time} sec to finish.")
        return response
