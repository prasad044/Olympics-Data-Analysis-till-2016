import pandas as pd


def preprocess(data, noc_region_data):

    data = data[data['Season']== 'Summer']

    data = data.merge(noc_region_data, on = 'NOC', how = "left")

    data.drop_duplicates(inplace=True)

    data = pd.concat([data, pd.get_dummies(data['Medal'])], axis = 1)
    return data