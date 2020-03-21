from pathlib import Path

full_depth_folder = Path('/Users/kaushalyakularatnam/Projects/orderbook_rebuild/data/full_depth/20160901/')
test_data = Path('/Users/kaushalyakularatnam/Projects/orderbook_rebuild/data/test_files/')

add = ['ADD BID', 'ADD ASK']
delete = ['DELETE BID', 'DELETE ASK', 'FILL BID', 'FILL ASK']
update = ['EXECUTE BID', 'EXECUTE ASK', 'CANCEL BID', 'CANCEL ASK']

ob_depth = 10