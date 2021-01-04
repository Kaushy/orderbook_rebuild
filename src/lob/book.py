#!/usr/bin/python

import config
import numpy as np
from collections import deque
from datetime import datetime
from lob.tick import Bid, Ask, Trade
from lob.tree import Tree
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
        self.last_timestamp = datetime(1970, 1, 1, 12, 0, 0, 000000)
        self.action = 0
        self.id_num = 0
        self.participant = ""


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


    def calc_volume_in_boundary(self, isreversed, upper, lower, curr_vol):
        """ Takes an upper and lower bound for price levels and calculates volume within this price level. 
            For bids, range inclusive of upper bound, (lower, upper] and for offers range inclusive of lower bound [lower, upper) 
        Args:
            isreversed (bool): Sorted in descending order for bids, and ascending order for offers
            upper (double): Upper bound price level
            lower (double): Lower bound price level
            curr_vol (int): Volume of current order

        Returns:
            (int) : Y parameter based on side returned and liquidity addition percentage in the price band
        """
        total_vol = int(curr_vol) 
        for k, v in self.bids.price_tree.items(reverse=isreversed):
            if isreversed:
                if k > lower and k <= upper:
                    total_vol += v.volume
            else:
                if k >= lower and k < upper:
                    total_vol += v.volume

        curr_vol = (int(curr_vol) / total_vol)
        if curr_vol < 0.25:
            if isreversed:
                return 29
            else:
                return 30
        elif curr_vol >= 0.25 and curr_vol < 0.5:
            if isreversed:
                return 31
            else:
                return 32
        elif curr_vol >= 0.5 and curr_vol < 0.75:
            if isreversed:
                return 33
            else:                                    
                return 34
        elif curr_vol >= 0.75 and curr_vol < 1:
            if isreversed:
                return 35
            else:
                return 36
        else:
            if isreversed:
                return 37
            else:
                return 38


    def action_multi_task(self, row, instruction, price, side, volume):
        """
           side in [1,2] 
           action in [0, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] 
           price_level in [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26] where 13, 20 is default when no price change of even deletions
           liquidity in [27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40] where 27, 40 is default when no price change of even deletion

        Args:
            row ([type]): [description]
            instruction ([type]): [description]
            price ([type]): [description] 
            side ([type]): [description]                                                                                                           
            volume ([type]): [description]

        Returns:
            [type]: [description]
        """
        action = 0
        price = float(price)

        if side == 1:
            liquidity = 27
            price_level = 13
            sorted_keys = sorted(self.bids.price_map.keys(), reverse=True)
            last_idx = len(sorted_keys) - 1

            if instruction == 'FILL BID':
                action = 3
            elif instruction == 'EXECUTE BID':
                action  = 4
            elif instruction == 'DELETE BID':
                action = 5
            elif instruction == 'CANCEL BID':
                action = 6
            elif instruction == 'ADD BID':
                action  = 7
            
            if instruction == 'ADD BID':
                # Improving BB, Joining BB, Top 5 Levels, Top 10 levels, Top 20 Levels, All Else  
                # In the case of 5 level Either there are more than 5 levels and setting within 5 levels or less than 5 levels and setting price within this
                if last_idx == -1 or price > sorted_keys[0]:
                    price_level = 14
                    if last_idx == -1:
                        liquidity = 28
                    else:
                        liquidity = self.calc_volume_in_boundary(True, float('inf'), sorted_keys[0], volume)
                elif last_idx >= 0 and price == sorted_keys[0]:
                    price_level = 15
                    liquidity = self.calc_volume_in_boundary(True, price, sorted_keys[0], volume)
                elif (last_idx >= 4 and sorted_keys[0] > price >= sorted_keys[4]) or (last_idx >= 0 and last_idx < 4 and price < sorted_keys[0]):
                    price_level = 16
                    if last_idx >= 4:
                        liquidity = self.calc_volume_in_boundary(True, sorted_keys[0], sorted_keys[4], volume)
                    else:
                        liquidity = self.calc_volume_in_boundary(True, sorted_keys[0], sorted_keys[last_idx], volume)
                elif (last_idx >= 9 and sorted_keys[4] > price >= sorted_keys[9]) or (last_idx >= 4 and last_idx < 9 and price < sorted_keys[4]):
                    price_level = 17
                    if last_idx >= 9:
                        liquidity = self.calc_volume_in_boundary(True, sorted_keys[4], sorted_keys[9], volume)
                    else:
                        liquidity = self.calc_volume_in_boundary(True, sorted_keys[4], sorted_keys[last_idx], volume)
                elif (last_idx >= 19 and sorted_keys[9] > price >= sorted_keys[19]) or (last_idx >= 9 and last_idx < 19 and price < sorted_keys[9]):
                    price_level = 18
                    if last_idx >= 19:
                        liquidity = self.calc_volume_in_boundary(True, sorted_keys[9], sorted_keys[19], volume)
                    else:
                        liquidity = self.calc_volume_in_boundary(True, sorted_keys[9], sorted_keys[last_idx], volume)   
                else:
                    price_level = 19
                    liquidity = self.calc_volume_in_boundary(True, sorted_keys[19], 0, volume)                                
        else:
            liquidity = 40
            price_level = 20
            sorted_keys = sorted(self.bids.price_map.keys())
            last_idx = len(sorted_keys) - 1
            
            if instruction == 'FILL ASK':          
                action = 8
            elif instruction == 'EXECUTE ASK':
                action  = 9
            elif instruction == 'DELETE ASK':
                action = 10
            elif instruction == 'CANCEL ASK':
                action = 11
            elif instruction == 'ADD ASK':
                action  = 12
            
            if instruction == 'ADD ASK':
                # Improving BB, Joining BB, Top 5 Levels, Top 10 levels, Top 20 Levels, All Else  
                # In the case of 5 level Either there are more than 5 levels and setting within 5 levels or less than 5 levels and setting price within this
                if last_idx == -1 or (price < sorted_keys[0]):                        
                    price_level = 21
                    if last_idx == -1:
                        liquidity = 39
                    else:
                        liquidity = self.calc_volume_in_boundary(False, sorted_keys[0], 0, volume)
                elif last_idx >= 0 and price == sorted_keys[0]:
                    price_level = 22
                    liquidity = self.calc_volume_in_boundary(False, sorted_keys[0], price, volume)
                elif (last_idx >= 4 and sorted_keys[0] < price <= sorted_keys[4]) or (last_idx >= 0 and last_idx < 4 and price > sorted_keys[0]):
                    price_level = 23
                    if last_idx >= 4:
                        liquidity = self.calc_volume_in_boundary(False, sorted_keys[4], sorted_keys[0], volume)
                    else:
                        liquidity = self.calc_volume_in_boundary(False, sorted_keys[last_idx], sorted_keys[0], volume)
                elif (last_idx >= 9 and sorted_keys[4] < price <= sorted_keys[9]) or (last_idx >= 4 and last_idx < 9 and price > sorted_keys[4]):
                    price_level = 24
                    if last_idx >= 9:
                        liquidity = self.calc_volume_in_boundary(False, sorted_keys[9], sorted_keys[4], volume)
                    else:
                        liquidity = self.calc_volume_in_boundary(False, sorted_keys[last_idx], sorted_keys[4], volume)
                elif (last_idx >= 19 and sorted_keys[9] < price <= sorted_keys[19]) or (last_idx >= 9 and last_idx < 19 and price > sorted_keys[9]):
                    price_level = 25
                    if last_idx >= 19:
                        liquidity = self.calc_volume_in_boundary(False, sorted_keys[19], sorted_keys[9], volume)
                    else:
                        liquidity = self.calc_volume_in_boundary(False, sorted_keys[last_idx], sorted_keys[9], volume)
                else:
                    price_level = 26
                    liquidity = self.calc_volume_in_boundary(False,  float('inf'), sorted_keys[19], volume)
        return [side, action, price_level, liquidity, price, volume]



    def action_single_task(self, row, instruction, price, side):
        action = 0
        price = float(price)
        if side == 1:
            sorted_keys = sorted(self.bids.price_map.keys(), reverse=True)
            last_idx = len(sorted_keys) - 1
            if instruction == 'FILL BID':
                action = 1
            elif instruction == 'EXECUTE BID':
                action  = 2
            elif instruction == 'DELETE BID':
                action = 3
            elif instruction == 'CANCEL BID':
                action = 4
            elif instruction == 'ADD BID':
                # Improving BB, Joining BB, Top 5 Levels, Top 10 levels, Top 20 Levels, All Else  
                # In the case of 5 level Either there are more than 5 levels and setting within 5 levels or less than 5 levels and setting price within this
                if last_idx == -1 or price > sorted_keys[0]:
                    action = 5
                elif last_idx >= 0 and price == sorted_keys[0]:
                    action = 6
                elif (last_idx >= 4 and sorted_keys[0] > price >= sorted_keys[4]) or (last_idx >= 0 and last_idx < 4 and price < sorted_keys[0]):
                    action = 7
                elif (last_idx >= 9 and sorted_keys[4] > price >= sorted_keys[9]) or (last_idx >= 4 and last_idx < 9 and price < sorted_keys[4]):
                    action = 8
                elif (last_idx >= 19 and sorted_keys[9] > price >= sorted_keys[19]) or (last_idx >= 9 and last_idx < 19 and price < sorted_keys[9]):
                    action = 9
                else:
                    action = 10                            
        else:
            sorted_keys = sorted(self.asks.price_map.keys())
            last_idx = len(sorted_keys) - 1
            if instruction == 'FILL ASK':
                action = 11
            elif instruction == 'EXECUTE ASK':
                action = 12
            elif instruction == 'DELETE ASK':
                action = 13
            elif instruction == 'CANCEL ASK':
                action = 14
            elif instruction == 'ADD ASK':
                # Improving BB, Joining BB, Top 5 Levels, Top 10 levels, Top 20 Levels, All Else  
                # In the case of 5 level Either there are more than 5 levels and setting within 5 levels or less than 5 levels and setting price within this
                if last_idx == -1 or (price < sorted_keys[0]):                        
                    action = 15
                elif last_idx >= 0 and price == sorted_keys[0]:
                    action = 16
                elif (last_idx >= 4 and sorted_keys[0] < price <= sorted_keys[4]) or (last_idx >= 0 and last_idx < 4 and price > sorted_keys[0]):
                    action = 17
                elif (last_idx >= 9 and sorted_keys[4] < price <= sorted_keys[9]) or (last_idx >= 4 and last_idx < 9 and price > sorted_keys[4]):
                    action = 18
                elif (last_idx >= 19 and sorted_keys[9] < price <= sorted_keys[19]) or (last_idx >= 9 and last_idx < 19 and price > sorted_keys[9]):
                    action = 19
                else:
                    action = 20
        return action


    def bid_as(self, csv):
        columns = ['Date', 'Timestamp', 'OrderNumber', 'EventType', 'Ticker',
                   'Price', 'Quantity', 'MPID', 'Exchange']
        data = parse_csv(columns, csv)
        bid = Bid(data)
        if bid.timestamp >= self.last_timestamp:
            self.last_timestamp = bid.timestamp
            self.action = bid.action
            self.id_num = bid.id_num
            self.participant = bid.participant
        self.last_tick = bid
        self.process_bid_ask(bid)
        return bid


    def bid_split(self, symbol, id_num, qty, price, timestamp, action, participant, action_words):
        data = {
            'Timestamp': timestamp,
            'Quantity': qty,
            'Price': price,
            'OrderNumber': id_num,
            'EventType': action,
            'Participant': participant
        }
        bid = Bid(data)
        if bid.timestamp >= self.last_timestamp:
            self.last_timestamp = bid.timestamp
            self.action = bid.action
            self.id_num = bid.id_num
            self.participant = bid.participant
        self.last_tick = bid
        self.process_bid_ask(bid, action_words)
        return bid


    def ask_as(self, csv):
        columns = ['Date', 'Timestamp', 'OrderNumber', 'EventType', 'Ticker',
                   'Price', 'Quantity', 'MPID', 'Exchange']
        data = parse_csv(columns, csv)
        ask = Ask(data)
        if ask.timestamp >= self.last_timestamp:
            self.last_timestamp = ask.timestamp
            self.action = ask.action
            self.id_num = ask.id_num
            self.participant = ask.participant
        self.last_tick = ask
        self.process_bid_ask(ask)
        return ask


    def ask_split(self, symbol, id_num, qty, price, timestamp, action, participant, action_words):
        data = {
            'Timestamp': timestamp,
            'Quantity': qty,
            'Price': price,
            'OrderNumber': id_num,
            'EventType': action,
            'Participant': participant
        }
        ask = Ask(data)
        if ask.timestamp >= self.last_timestamp:
            self.last_timestamp = ask.timestamp
            self.action = ask.action
            self.id_num = ask.id_num
            self.participant = ask.participant
        self.last_tick = ask
        self.process_bid_ask(ask, action_words)
        return ask


    def trade_as(self, csv):
        columns = ['Date', 'Timestamp', 'OrderNumber', 'EventType', 'Ticker',
                   'Price', 'Quantity', 'MPID', 'Exchange']
        data = parse_csv(columns, csv)
        data['id_num'] = 0
        trade = Trade(data)
        if trade.timestamp >= self.last_timestamp:
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


    @property
    def store_lob_matrix(self):
        ob_state = np.zeros(1, dtype=[('index', '<M8[us]'), ('side', 'U1'), ('action', 'uint64'),
                                      ('curr_orderid', 'uint64'), ('curr_participant', 'U10'),
                                      ('price', ('float64', [2, config.ob_depth])),
                                      ('quantity', ('uint64', [2, config.ob_depth])),
                                      ('order_id', ('uint64', [2, config.ob_depth])),
                                      ('timestamp', ('<M8[us]', [2, config.ob_depth])),
                                      ('participant', ('U10', [2, config.ob_depth]))])

        if self.bids is not None and len(self.bids) > 0:
            count = 0
            for k, v in self.bids.price_tree.items(reverse=True):
                if v.head_order is None:
                    return
                else:
                    n = v.head_order
                    while n is not None and count <= config.ob_depth - 1:
                        ob_state[0][0] = self.last_timestamp
                        ob_state[0][1] = 'B' if self.last_tick.is_bid else 'S'
                        ob_state[0][2] = self.action
                        ob_state[0][3] = self.id_num
                        ob_state[0][4] = self.participant
                        ob_state[0][5][0][count] = k
                        ob_state[0][6][0][count] = n.qty
                        ob_state[0][7][0][count] = n.id_num
                        ob_state[0][8][0][count] = n.timestamp
                        ob_state[0][9][0][count] = n.participant
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
                        ob_state[0][0] = self.last_timestamp
                        ob_state[0][1] = 'B' if self.last_tick.is_bid else 'S'
                        ob_state[0][2] = self.action
                        ob_state[0][3] = self.id_num
                        ob_state[0][4] = self.participant
                        ob_state[0][5][1][count] = k
                        ob_state[0][6][1][count] = n.qty
                        ob_state[0][7][1][count] = n.id_num
                        ob_state[0][8][1][count] = n.timestamp
                        ob_state[0][9][1][count] = n.participant
                        n = n.next_order
                        count += 1
        return ob_state

  #  @property
   # def aggregated_lob_storage(self):
   #     ob_state = np.zeros(1, dtype=[('timestamp', ('<M8[us]', [2, config.ob_depth])),
     #                                  ('price', ('float64', [2, config.ob_depth])),
     #                                  ('quantity', ('uint64', [2, config.ob_depth]))])
      #  for k, v in self.bids.price_tree.items(reverse=True):
       # [(ob_state[0][1][0].append(i), x.append(self.bids.price_map[i].volume)) for i in self.bids.price_map.keys()]
      #      ob_state[0][1].append(k)
        #    ob_state[0][2].append(v.volume)
        # self.bids.price_map[i].volume
        #print(ob_state[2][0][0])
       


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
