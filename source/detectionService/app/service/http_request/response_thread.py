import logging
from multiprocessing import Queue
from time import sleep

from api.api_rest_client_database import update_database_products
from entities.http.database_models import DatabaseUpdateResponse

logger = logging.getLogger(__name__)

def response_thread(response_queue:Queue):
    while True:
        try:
            response:DatabaseUpdateResponse = response_queue.get()
            if response is not None:
                update_database_products(response)
        except:
            logger.error("Error while sending response")
        sleep(5)