import logging
import sys

def initLogger(name):
    loggerMvshub = logging.getLogger(name)
    loggerMvshub.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s \t %(levelname)s \t [%(filename)s:%(lineno)d] \t %(message)s')
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(formatter)

    logName = "_{0}.log".format(name)
    file_handler = logging.FileHandler('./'+logName)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    loggerMvshub.addHandler(file_handler)
    loggerMvshub.addHandler(stdout_handler)
