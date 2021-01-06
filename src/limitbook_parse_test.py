#!/usr/bin/python

import sys
sys.path.append(".")

import numpy as np
import config
import csv
import copy
import os
import pathlib
import sys
import utils 
from lob.book import Book


def algoseekdata(source, destination_matrix):
    """
    order_book is of type Book() and holds book data. ob_state is a specific state
    """
    for subdir, dirs, files in os.walk(source):
        for file in files:
            data_path = os.path.join(subdir, file)
            with open(data_path) as csv_file:
                if data_path == '/rds/general/user/kk2219/home/orderbook_rebuild/data/input/raw/20190403/USM_NASDAQ.csv':
                    reader = csv.reader(csv_file, delimiter=',')
                    print(data_path)
                    order_book = Book()
                    action_multi = []
                    action_single = 0
                    ob_state_list = []  # List of matrices per time point for order book state changes
                    action_multi_list = [] # List of actions per time point. Last action will be 0. Action is move after current state
                    action_single_list = []
                    try:
                        next(reader)
                        for row in reader:
                            timestamp = utils.convert_datetime(row[0], row[1])
                            if row[3] in ['ADD BID', 'EXECUTE BID', 'CANCEL BID', 'FILL BID', 'DELETE BID']:
                                action_multi = order_book.action_multi_task(row[2], row[3], row[5], 1, row[6])
                                action_single = order_book.action_single_task(row[2], row[3], row[5], 1)
                                order_book.bid_split(row[4], row[2], row[6], row[5], timestamp, config.algoseek_dict.get(row[3]), row[7], row[3])
                            elif row[3] in ['ADD ASK', 'EXECUTE ASK', 'CANCEL ASK', 'FILL ASK', 'DELETE ASK']:
                                action_multi = order_book.action_multi_task(row[2], row[3], row[5], 2, row[6])
                                action_single = order_book.action_single_task(row[2], row[3], row[5], 2)
                                order_book.ask_split(row[4], row[2], row[6], row[5], timestamp, config.algoseek_dict.get(row[3]), row[7], row[3])

                            ob_state = copy.deepcopy(order_book.store_lob_matrix)
                            ob_state_list.append(ob_state)
                            action_multi_list.append(action_multi)
                            action_single_list.append(action_single)
                    except IOError:
                        print('Cannot open input file "%s"' % sys.argv[1])
                        sys.exit(1)


if __name__ == '__main__':
       # algoseekdata(config.test_source, config.test_dest)
       npy = np.load('/rds/general/user/kk2219/home/orderbook_rebuild/data/output/raw/20190403/Y/USM_NASDAQ.npy', allow_pickle=False)
       np.savetxt('usm_y_test.csv', npy[:,2].astype(int), delimiter=',')
