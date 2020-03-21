# coding=utf-8
from datetime import datetime


def convert_datetime(date_field, time_field):
    return datetime.strptime(date_field + time_field, '%Y%m%d%H:%M:%S.%f')
