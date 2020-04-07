#!/usr/bin/python

import numpy as np
import config
import csv
import copy
import errno
import os
import pandas as pd
import pathlib
import sys
import src.utils as utils
from src.lob.book import Book


def make_dir(file_name):
    if not os.path.exists(os.path.dirname(file_name)):
        try:
            os.makedirs(os.path.dirname(file_name))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def split_data_into_exchanges(source_path, destination_path):
    """
    Splits the data into different exchanges as currently it is one large exchange file. As groupby preserves order we
    do not further sort the outcome.
    Parameters
    ----------
    """
    for subdir, dirs, files in os.walk(source_path):
        for file in files:
            source_full_file = os.path.join(subdir, file)
            df = pd.read_csv(source_full_file)
            for group_name, df in df.groupby(['Ticker', 'Exchange']):
                file_name = destination_path / str(df['Date'].iloc[0]) / convertTuple(group_name)
                make_dir(file_name)
                with open(file_name, "w+") as f:
                    df.to_csv(f, index=False)


def convertTuple(tup):
    tup_str = '_'.join(tup)
    return str(tup_str) + '.csv'


def algoseekdata(source, destination_matrix):
    """
    order_book is of type Book() and holds book data. ob_state is a specific state
    """
    for subdir, dirs, files in os.walk(source):
        for file in files:
            data_path = os.path.join(subdir, file)
            with open(data_path) as csv_file:
                reader = csv.reader(csv_file, delimiter=',')
                print(data_path)
                order_book = Book()
                ob_state_list = []  # List of matrices per time point for order book state changes
                try:
                    next(reader)
                    for row in reader:
                        timestamp = utils.convert_datetime(row[0], row[1])
                        if row[3] in ['ADD BID', 'EXECUTE BID', 'CANCEL BID', 'FILL BID', 'DELETE BID']:
                            order_book.bid_split(row[4], row[2], row[6], row[5], timestamp, row[3])
                        elif row[3] in ['ADD ASK', 'EXECUTE ASK', 'CANCEL ASK', 'FILL ASK', 'DELETE ASK']:
                            order_book.ask_split(row[4], row[2], row[6], row[5], timestamp, row[3])

                        ob_state = copy.deepcopy(order_book.store_lob_matrix())
                        ob_state_list.append(ob_state)
                    file_name = destination_matrix / pathlib.PurePath(os.path.normpath(data_path)).parent.name / \
                                os.path.splitext(pathlib.PurePath(data_path).name)[0]
                    make_dir(file_name)
                    np.save(file_name, ob_state_list)
                except IOError:
                    print('Cannot open input file "%s"' % sys.argv[1])
                    sys.exit(1)


if __name__ == '__main__':
    # split_data_into_exchanges(config.source_algoseek, config.destination_exchange)
     algoseekdata(config.test_source_exchange, config.test_destination_matrix)
    # algoseekdata(config.source_exchange, config.destination_matrix)
