import config
import csv
import numpy as np

google_data = config.full_depth_folder / "GOOG.csv"
ob_state = np.array([[[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
                     [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
                     [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]], np.float)
training_data = []
# use put / putmask and so on to add elements to array

with open(google_data) as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)
    step=0
    for row in reader:
        #print(row)
        if (row[3] == 'ADD BID'):
            np.insert(ob_state, 1, np.array((1, 1)), 0)
            print(ob_state)
        elif (row[3] == 'ADD_ASK'):
            ob_state[[0][0]] = row[2]

    training_data.append(ob_state)




print(training_data[0])