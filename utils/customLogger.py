import logging
import sys

def initLogger():
    loggerMvshub = logging.getLogger('activity')
    loggerMvshub.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s \t %(levelname)s \t [%(filename)s:%(lineno)d] \t %(message)s')
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(formatter)
    logName = "_activity.log"
    file_handler = logging.FileHandler('./'+logName)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    loggerMvshub.addHandler(file_handler)
    loggerMvshub.addHandler(stdout_handler)