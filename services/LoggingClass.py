import datetime
from admininterface.models import Logging


class LoggingClass:
    logging_action = ""

    @staticmethod
    def add_notice(logging_action: str):
        logging_info = Logging()
        logging_info.time = datetime.datetime.now()
        logging_info.action = logging_action
        logging_info.save()

    @staticmethod
    def delete_all_notes():
        Logging.objects.all().delete()
