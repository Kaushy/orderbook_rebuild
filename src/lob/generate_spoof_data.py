# coding=utf-8
# coding=utf-8
from src import config
import os
import pandas as pd
import numpy as np
import src.utils as utils

pd.set_option('display.max_columns', None)

# 1. It cannot be in the same dataset so we need either different datasets or same dataset with positive and negative skews
# 2. Inside the Skew introduce contra side reduction of values - currently all is set to 5
# 3. Pass values inside of the ranges. Currently hard coded but might be nice to have ranges

def spoofing_imputation(data_original, delete, add, spoof):
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
    data = data_original.copy()
    deletions = data[data['EventType'] == delete]['OrderNumber']
    count_of_selection = int(deletions.count()/4)
    deleted_orders = deletions.sample(count_of_selection)

    mask = data['OrderNumber'].isin(deleted_orders) & (data['EventType'] == add)
    mask_del = data['OrderNumber'].isin(deleted_orders) & (data['EventType'] == delete)

    data.loc[:, 'Spoofing'] = np.where(mask_del, spoof, 'Normal')
    data.loc[:, 'Quantity'] = np.where(mask, np.exp(np.log2(
        data['Quantity'].multiply(np.random.randint(50, 500, mask.shape)))).astype(int), data['Quantity'].values)
    return data


def store_spoof_data(data, del_action, add_action, spoof_col_name, source):
    """

    Parameters
    ----------
    data
    del_action
    add_action
    spoof_col_name
    source
    """
    imputed_data = spoofing_imputation(data, del_action, add_action, spoof_col_name)
    ticker_exchange = str(imputed_data['Ticker'].iloc[0]) + '_' + str(imputed_data['Exchange'].iloc[0]) + '.csv'
    file_name = source / str(imputed_data['Date'].iloc[0]) / ticker_exchange
    utils.make_dir(file_name)
    with open(file_name, "w+") as f:
        imputed_data.to_csv(f, index=False)


for subdir, dirs, files in os.walk(config.source_exchange):
    for file in files:
        data_path = os.path.join(subdir, file)
        print(data_path)
        data = pd.read_csv(data_path)
        store_spoof_data(data, 'DELETE BID', 'ADD BID', 'Spoofing_Bid', config.source_spoof_bid)
        store_spoof_data(data, 'DELETE ASK', 'ADD ASK', 'Spoofing_Ask', config.source_spoof_ask)





