# coding=utf-8
import errno
import os
from datetime import datetime


def convert_datetime(date_field, time_field):
    return datetime.strptime(date_field + time_field, '%Y%m%d%H:%M:%S.%f')


def make_dir(file_name):
    if not os.path.exists(os.path.dirname(file_name)):
        try:
            os.makedirs(os.path.dirname(file_name))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
