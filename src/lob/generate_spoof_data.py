# coding=utf-8
# coding=utf-8
import config
import os
import pandas as pd
import numpy as np


def spoofing_imputation(data, delete, add, spoof, is_new_field):
    """

    Parameters
    ----------
    data
    delete
    add
    spoof
    is_new_field

    Returns
    -------

    """
    deleted_orders = data[data['EventType'] == delete]['OrderNumber']
    mask = (data['OrderNumber'].isin(deleted_orders)) & (data['EventType'] == add)
    samples = int(mask.count() / 4)
    mask_convert_to_neg = mask.sample(samples)
    mask_convert_to_neg.replace(True, False, inplace=True)
    mask.update(mask_convert_to_neg)
    if is_new_field:
        data.loc[:, 'Spoofing'] = np.where(mask, spoof, 'Normal')
    else:
        data.loc[:, 'Spoofing'] = np.where(mask, spoof, data['Spoofing'].values)
    data.loc[:, 'Quantity'] = np.where(mask, np.exp(np.log2(
        data['Quantity'].multiply(np.random.randint(50, 500, mask.shape)))).astype(int), data['Quantity'].values)
    return data

data = pd.read_csv(config.source_exchange / '20160901/GOOG_BATS.csv')
bid_data = spoofing_imputation(data, 'DELETE BID', 'ADD BID', 'Spoofing_Bid', True)
spoofing_imputation(bid_data, 'DELETE ASK', 'ADD ASK', 'Spoofing_Ask', False)

for subdir, dirs, files in os.walk(config.source_exchange):
    for file in files:
        data_path = os.path.join(subdir, file)
        print(data_path)