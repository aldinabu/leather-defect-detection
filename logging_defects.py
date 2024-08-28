import configparser
from datetime import datetime
import logging
import csv

config = configparser.ConfigParser()
config.read('config.ini')


def get_logger(filename=config['LOGGING']['filename']):
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename=filename, encoding='utf-8', level=logging.DEBUG)
    return logger


def log_prediction(image_path, prediction, filename=config['LOGGING']['filename_for_defect_tracking']):
    with open(filename, 'a', encoding='UTF8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), image_path, prediction])
