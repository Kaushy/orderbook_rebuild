#!/usr/bin/python

import sys
from src.lob.book import Book
import config
import csv
import src.utils as utils


test_data = config.test_data / "test_data_parse.csv"
test_abeo = config.test_data / "ABEO_Small.csv"
real_data = config.full_depth_folder / 'ABEO.csv'

def algoseekdata():
    with open(test_data) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        step = 0
        order_book_EDGX = Book()
        order_book_EDGA = Book()
        order_book_NYSE = Book()
        order_book_ARCA = Book()
        order_book_NASDAQ = Book()
        order_book_BATS = Book()

        try:
            next(reader)
            for row in reader:
                if row[8] == 'EDGX':
                    order_book = order_book_EDGX
                elif row[8] == 'EDGA':
                    order_book = order_book_EDGA
                elif row[8] == 'NYSE':
                    order_book = order_book_NYSE
                elif row[8] == 'ARCA':
                    order_book = order_book_ARCA
                elif row[8] == 'NASDAQ':
                    order_book = order_book_NASDAQ
                elif row[8] == 'BATS':
                    order_book = order_book_BATS
                else:
                    print('what order book ' + str(row[8]))

                timestamp = utils.convert_datetime(row[0], row[1])
                if row[3] in ['ADD BID', 'EXECUTE BID', 'CANCEL BID', 'FILL BID', 'DELETE BID']:
                    order_book.bid_split(row[4], row[2], row[6], row[5], timestamp, row[3])
                elif row[3] in ['ADD ASK', 'EXECUTE ASK', 'CANCEL ASK', 'FILL ASK', 'DELETE ASK']:
                    order_book.ask_split(row[4], row[2], row[6], row[5], timestamp, row[3])
                print(row[8])
                print(order_book)
                order_book.store_lob_matrix()
        except IOError:
            print('Cannot open input file "%s"' % sys.argv[1])
            sys.exit(1)


if __name__ == '__main__':
    algoseekdata()
