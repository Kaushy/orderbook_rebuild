#!/usr/bin/python
import numpy as np

class Tick(object):
    def __init__(self, data):
        self.timestamp = int(data['OrderNumber']) 
        #self.sequence = 0
        self.qty = int(data['Quantity'])
        self.price = float(data['Price'])
        self.id_num = data['OrderNumber']
        #self.participant_id = F.participant_id
        #self.client_id = F.client_id

def convert_datetime(time_field, date_field):
    return np.datetime64(time_field + date_field)

class Trade(Tick):
    def __init__(self, data):
        super(Trade, self).__init__(data)

class Ask(Tick):
    def __init__(self, data):
        super(Ask, self).__init__(data)
        self.is_bid = False

class Bid(Tick):
    def __init__(self, data):
        super(Bid, self).__init__(data)
        self.is_bid = True
