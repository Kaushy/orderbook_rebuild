#!/usr/bin/python

import config
import numpy as np
import pickle
from collections import deque
from datetime import datetime
from src.lob.tick import Bid, Ask, Trade
from src.lob.tree import Tree
from six.moves import cStringIO as StringIO

def parse_csv(columns, line):
    """
    Parse a CSV line that has ',' as a separator.
    Columns is a list of the column names, must match the number of
    comma-separated values in the input line.
    """
    data = {}
    split = line.split(',')
    for idx, name in enumerate(columns):
        data[name] = split[idx]
    return data


class Book(object):
    def __init__(self):
        self.trades = deque(maxlen=100)  # Index [0] is most recent trade
        self.bids = Tree()
        self.asks = Tree()
        self.last_tick = None
        self.last_timestamp = datetime(1950, 1, 1, 12, 0, 0, 000000)
            #np.datetime64('1950-1-1T12:00')
        self.ob_state = np.array([[np.zeros(config.ob_depth), np.zeros(config.ob_depth)],
                                                        [np.zeros(config.ob_depth), np.zeros(config.ob_depth)],
                                                        [np.zeros(config.ob_depth), np.zeros(config.ob_depth)]], np.float)

    def process_bid_ask(self, tick, action):
        """
        Generic method to process bid or ask.
        """
        tree = self.asks
        if tick.is_bid:
            tree = self.bids

        if action in config.add:
            tree.insert_tick(tick)
        elif action in config.delete:
            tree.remove_order_by_id(tick.id_num)
        elif action in config.update:
            if tree.order_exists(tick.id_num):
                tree.update_order(tick)

    def bid_as(self, csv):
        columns = ['Date', 'Timestamp', 'OrderNumber', 'EventType', 'Ticker',
                   'Price', 'Quantity', 'MPID', 'Exchange']
        data = parse_csv(columns, csv)
        bid = Bid(data)
        if bid.timestamp > self.last_timestamp:
            self.last_timestamp = bid.timestamp
        self.last_tick = bid
        self.process_bid_ask(bid)
        return bid

    def bid_split(self, symbol, id_num, qty, price, timestamp, action):
        data = {
            'Timestamp': timestamp,
            'Quantity': qty,
            'Price': price,
            'OrderNumber': id_num
        }
        bid = Bid(data)
        if bid.timestamp > self.last_timestamp:
            self.last_timestamp = bid.timestamp
        self.last_tick = bid
        self.process_bid_ask(bid, action)
        return bid

    def ask_as(self, csv):
        columns = ['Date', 'Timestamp', 'OrderNumber', 'EventType', 'Ticker',
                   'Price', 'Quantity', 'MPID', 'Exchange']
        data = parse_csv(columns, csv)
        ask = Ask(data)
        if ask.timestamp > self.last_timestamp:
            self.last_timestamp = ask.timestamp
        self.last_tick = ask
        self.process_bid_ask(ask)
        return ask

    def ask_split(self, symbol, id_num, qty, price, timestamp, action):
        data = {
            'Timestamp': timestamp,
            'Quantity': qty,
            'Price': price,
            'OrderNumber': id_num
        }
        ask = Ask(data)
        if ask.timestamp > self.last_timestamp:
            self.last_timestamp = ask.timestamp
        self.last_tick = ask
        self.process_bid_ask(ask, action)
        return ask

    def trade_as(self, csv):
        columns = ['Date', 'Timestamp', 'OrderNumber', 'EventType', 'Ticker',
                   'Price', 'Quantity', 'MPID', 'Exchange']
        data = parse_csv(columns, csv)
        data['id_num'] = 0
        trade = Trade(data)
        if trade.timestamp > self.last_timestamp:
            self.last_timestamp = trade.timestamp
        self.last_tick = trade
        self.trades.appendleft(trade)
        return trade

    def trade_split(self, symbol, id_num, qty, price, timestamp):
        data = {
            'Timestamp': timestamp,
            'Quantity': qty,
            'Price': price,
            'OrderNumber': id_num
        }

        trade = Trade(data)
        if trade.timestamp > self.last_timestamp:
            self.last_timestamp = trade.timestamp
        self.last_tick = trade
        self.trades.appendleft(trade)
        return trade

    def store_lob_matrix(self):
        if self.bids is not None and len(self.bids) > 0:
            count = 0
            for k, v in self.bids.price_tree.items(reverse=True):
                if v.head_order is None:
                    return
                else:
                    n = v.head_order
                    while n is not None and count <= config.ob_depth - 1:
                        self.ob_state[0][0][count] = k
                        self.ob_state[1][0][count] = n.qty
                        self.ob_state[2][0][count] = n.id_num
                        # self.ob_state[3][0][count] = n.timestamp
                        n = n.next_order
                        count += 1
        if self.asks is not None and len(self.asks) > 0:
            count = 0
            for k, v in self.asks.price_tree.items():
                if v.head_order is None:
                    return
                else:
                    n = v.head_order
                    while n is not None and count <= config.ob_depth - 1:
                        self.ob_state[0][1][count] = k
                        self.ob_state[1][1][count] = n.qty
                        self.ob_state[2][1][count] = n.id_num
                        # self.ob_state[3][1][count] = n.timestamp
                        n = n.next_order
                        count += 1
        return self.ob_state


    def __str__(self):
        # Efficient string concat
        file_str = StringIO()
        file_str.write("------ Bids -------\n")
        if self.bids is not None and len(self.bids) > 0:
            count = 0
            for k, v in self.bids.price_tree.items(reverse=True):
                file_str.write('%s' % v)
                count += 1
        file_str.write("\n------ Asks -------\n")
        if self.asks is not None and len(self.asks) > 0:
            for k, v in self.asks.price_tree.items():
                file_str.write('%s' % v)
        file_str.write("\n------ Trades ------\n")
        if self.trades is not None and len(self.trades) > 0:
            num = 0
            for entry in self.trades:
                if num < 5:
                    file_str.write(str(entry.qty) + " @ " \
                                   + str(entry.price) \
                                   + " (" + str(entry.timestamp) + ")\n")
                    num += 1
                else:
                    break
        file_str.write("\n")
        return file_str.getvalue()
