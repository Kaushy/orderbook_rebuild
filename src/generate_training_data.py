# coding=utf-8
from src import config
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)

# NASDAQ
# LARGE ORDERS - POSITIVE SAMPLES
data_positive = pd.read_csv(config.source_exchange / '20160901/GOOG_NASDAQ.csv')
deleted_orders = data_positive[data_positive['EventType'] == 'DELETE BID']['OrderNumber']
pos_mask = data_positive['OrderNumber'].isin(deleted_orders)

# TODO : Currently this only multiplies by one random number. We may need each value multiplied by different random numbers
data_positive['Quantity'] = np.where(pos_mask,
                            data_positive['Quantity'].multiply(np.random.randint(1000, 10000, pos_mask.shape)),
                            data_positive['Quantity'].values)
data_positive.to_csv(config.source_exchange / '20160901_Positive/GOOG_NASDAQ.csv', index=False)


# SMALL ORDERS - NEGATIVE SAMPLES
data_negative = pd.read_csv(config.source_exchange / '20160901/GOOG_NASDAQ.csv')
deleted_orders_neg = data_negative[data_negative['EventType'] == 'DELETE BID']['OrderNumber']

# TODO : Currently this only divides by one random number. We may need each value multiplied by different random numbers
neg_mask = data_negative['OrderNumber'].isin(deleted_orders_neg)
data_negative['Quantity'] = np.where(neg_mask,
                            np.random.randint(1, 1500, neg_mask.shape),
                            data_negative['Quantity'].values)

print(data_positive)
data_negative.to_csv(config.source_exchange / '20160901_Negative/GOOG_NASDAQ.csv', index=False)

# BATS
# LARGE ORDERS - POSITIVE SAMPLES
data_positive = pd.read_csv(config.source_exchange / '20160901/GOOG_BATS.csv')
deleted_orders = data_positive[data_positive['EventType'] == 'DELETE BID']['OrderNumber']
pos_mask = data_positive['OrderNumber'].isin(deleted_orders)

# TODO : Currently this only multiplies by one random number. We may need each value multiplied by different random numbers
data_positive['Quantity'] = np.where(pos_mask,
                            data_positive['Quantity'].multiply(np.random.randint(1000, 10000, pos_mask.shape)),
                            data_positive['Quantity'].values)
data_positive.to_csv(config.source_exchange / '20160901_Positive/GOOG_BATS.csv', index=False)


# SMALL ORDERS - NEGATIVE SAMPLES
data_negative = pd.read_csv(config.source_exchange / '20160901/GOOG_BATS.csv')
deleted_orders_neg = data_negative[data_negative['EventType'] == 'DELETE BID']['OrderNumber']

# TODO : Currently this only divides by one random number. We may need each value multiplied by different random numbers
neg_mask = data_negative['OrderNumber'].isin(deleted_orders_neg)
data_negative['Quantity'] = np.where(neg_mask,
                            np.random.randint(1, 1500, neg_mask.shape),
                            data_negative['Quantity'].values)

print(data_positive)
data_negative.to_csv(config.source_exchange / '20160901_Negative/GOOG_BATS.csv', index=False)





