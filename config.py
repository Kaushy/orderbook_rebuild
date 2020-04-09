from pathlib import Path

# SOURCE DATA
source_algoseek = Path('/Users/kaushalyakularatnam/Projects/orderbook_rebuild/data/full_depth/')
source_exchange = Path('/Users/kaushalyakularatnam/Projects/orderbook_rebuild/data/input/')

# DESTINATION
destination_matrix = Path('/Users/kaushalyakularatnam/Projects/orderbook_rebuild/data/output/')

# TEST
test_source_exchange = Path('/Users/kaushalyakularatnam/Projects/orderbook_rebuild/data/test/input/')
test_destination_matrix = Path('/Users/kaushalyakularatnam/Projects/orderbook_rebuild/data/test/output/')

add = ['ADD BID', 'ADD ASK']
delete = ['DELETE BID', 'DELETE ASK', 'FILL BID', 'FILL ASK']
update = ['EXECUTE BID', 'EXECUTE ASK', 'CANCEL BID', 'CANCEL ASK']

# Algo Seek Interpretation for order book updates
algoseek_dict = {'ADD BID': 1, 'ADD ASK': 1, 'DELETE BID': 2, 'DELETE ASK': 2, 'FILL BID': 3, 'FILL ASK': 3, \
                 'EXECUTE BID': 4, 'EXECUTE ASK': 4, 'CANCEL BID': 5, 'CANCEL ASK': 5}

ob_depth = 30
