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

ob_depth = 30