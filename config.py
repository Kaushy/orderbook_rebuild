from pathlib import Path

# SOURCE Data
source_algoseek = Path('/Users/kaushalyakularatnam/Projects/orderbook_rebuild/data/full_depth/')

# DESTINATION
destination_exchange = Path('/Users/kaushalyakularatnam/Projects/orderbook_rebuild/data/symbol_exchange/')
destination_matrix = Path('/Users/kaushalyakularatnam/Projects/orderbook_rebuild/data/output')

# TEST
test_source_algoseek = Path('/Users/kaushalyakularatnam/Projects/orderbook_rebuild/data/test_files/')

add = ['ADD BID', 'ADD ASK']
delete = ['DELETE BID', 'DELETE ASK', 'FILL BID', 'FILL ASK']
update = ['EXECUTE BID', 'EXECUTE ASK', 'CANCEL BID', 'CANCEL ASK']

ob_depth = 10