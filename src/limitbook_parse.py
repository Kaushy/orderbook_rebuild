#!/usr/bin/python

import numpy as np
from src import config
import csv
import copy
import os
import pathlib
import sys
import src.utils as utils
from src.lob.book import Book


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
                            order_book.bid_split(row[4], row[2], row[6], row[5], timestamp,
                                                 config.algoseek_dict.get(row[3]), row[7], row[3])
                        elif row[3] in ['ADD ASK', 'EXECUTE ASK', 'CANCEL ASK', 'FILL ASK', 'DELETE ASK']:
                            order_book.ask_split(row[4], row[2], row[6], row[5], timestamp,
                                                 config.algoseek_dict.get(row[3]), row[7], row[3])

                        ob_state = copy.deepcopy(order_book.store_lob_matrix)
                        ob_state_list.append(ob_state)
                    file_name = destination_matrix / pathlib.PurePath(os.path.normpath(data_path)).parent.name / \
                                os.path.splitext(pathlib.PurePath(data_path).name)[0]
                    utils.make_dir(file_name)
                    np.save(file_name, ob_state_list)
                except IOError:
                    print('Cannot open input file "%s"' % sys.argv[1])
                    sys.exit(1)


if __name__ == '__main__':
      # algoseekdata(config.test_source_exchange, config.test_destination_matrix)
      # You have to split this more exchange specific as well as not all exchanges obey same rules
        algoseekdata(config.source_exchange, config.destination_exchange)
      # algoseekdata(config.source_spoof_bid, config.destination_spoof_bid)
      # algoseekdata(config.source_spoof_ask, config.destination_spoof_ask)
