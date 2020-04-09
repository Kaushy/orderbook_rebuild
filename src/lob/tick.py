#!/usr/bin/python


class Tick(object):
    def __init__(self, data):
        self.timestamp = data['Timestamp']
        self.qty = int(data['Quantity'])
        self.price = float(data['Price'])
        self.id_num = data['OrderNumber']
        self.action = data['EventType']
        self.participant = data['Participant']


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
