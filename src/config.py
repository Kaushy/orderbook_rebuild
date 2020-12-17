from pathlib import Path

def find_path(env):
    if env == 0:
        # SOURCE DATA
        source_exchange = Path('/Users/kaushalyakularatnam/Projects/orderbook_rebuild/data/input/raw/')

        # DESTINATION
        destination_exchange = Path('/Users/kaushalyakularatnam/Projects/orderbook_rebuild/data/output/raw/')
    
        # TEST
        test_source_algoseek = Path('/Users/kaushalyakularatnam/Projects/orderbook_rebuild/data/test/input/')
        test_destination_matrix = Path('/Users/kaushalyakularatnam/Projects/orderbook_rebuild/data/test/output/')
    else:
        # SOURCE DATA
        source_exchange = Path('/rds/general/user/kk2219/ephemeral/data/orderbook_rebuild/input/raw')

        # DESTINATION
        destination_exchange = Path('/rds/general/user/kk2219/ephemeral/data/orderbook_rebuild/output/raw/')

        # TEST
        test_source_algoseek = Path('/rds/general/user/kk2219/home/orderbook_rebuild/data/input/raw/')
        test_destination_matrix = Path('/rds/general/user/kk2219/home/orderbook_rebuild/data/output/raw/')
    return source_exchange, destination_exchange, test_source_algoseek, test_destination_matrix


# 0 For Local Computer / Macbook, 1 for Imperial HPC
environment = 1
source, destination, test_source, test_dest = find_path(environment)


add = ['ADD BID', 'ADD ASK']
delete = ['DELETE BID', 'DELETE ASK', 'FILL BID', 'FILL ASK']
update = ['EXECUTE BID', 'EXECUTE ASK', 'CANCEL BID', 'CANCEL ASK']

# Algo Seek Interpretation for order book updates
algoseek_dict = {'ADD BID': 1, 'ADD ASK': 1, 'DELETE BID': 2, 'DELETE ASK': 2, 'FILL BID': 3, 'FILL ASK': 3, \
                 'EXECUTE BID': 4, 'EXECUTE ASK': 4, 'CANCEL BID': 5, 'CANCEL ASK': 5}

ob_depth = 3
