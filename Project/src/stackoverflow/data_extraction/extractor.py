"""
Created on Wed Aug  9 09:44:36 2017

@author: almaz
"""

import stackexchange
import pandas as pd
import numpy as np


def extract_user():
    indexes = ('display_name',  'account_id', 'creation_date',
               'last_access_date', 'reputation')
    data = []
    so = stackexchange.Site(stackexchange.StackOverflow, app_key="A8wB710uq0)YLzS271nWug((")

    for i in range(1, 10000, 100):
        id_list = list(range(i, i+100))
        try:
            users = so.users(id_list)
        except:
            continue
        for user in users:
            data.append(user.display_name)
            data.append(user.account_id)
            data.append(user.creation_date)
            data.append(user.last_access_date)
            data.append(user.reputation)

    data_np = np.asarray(data)
    data_np = data_np.reshape((int(len(data)/len(indexes)), len(indexes)))
    print(data_np.shape)
    user_df = pd.DataFrame(data=data_np, columns=indexes)
    user_df.to_csv("../../../data/user.csv", sep=';')


def extract_timeline():
    indexes = ['user_id', 'timeline_type', 'post_type', 'creation_date']
    so = stackexchange.Site(stackexchange.StackOverflow, app_key="A8wB710uq0)YLzS271nWug((")
    data_df = pd.read_csv("../../../data/user.csv", sep=';')
    id_list = data_df['account_id'].tolist()
    count = 1
    timeline_list = []
    for id in id_list:
        try:
            user = so.user(id)
            timeline = user.timeline.fetch()
            print(user.display_name + " - " + str(count))
            for event in timeline:
                if event.timeline_type != "badge":
                    timeline_list.append(event.user_id)
                    timeline_list.append(event.timeline_type)
                    timeline_list.append(event.post_type)
                    timeline_list.append(event.creation_date)
            if count % 10 == 0:
                data_np = np.asarray(timeline_list)
                data_np = data_np.reshape((int(len(timeline_list)/len(indexes)), len(indexes)))
                timeline_df = pd.DataFrame(data=data_np, columns=indexes)
                timeline_df.to_csv("../../../data/timeline" + str(count/10) +".csv", sep=';')
                timeline_list = []
            count += 1
        except:
            continue



def make_one_timelines():
    data_df = pd.read_csv("../../../data/timeline1.0.csv", sep=';',index_col=0)
    print(data_df.shape)
    for i in range(2,41):
        data_10_df = pd.read_csv("../../../data/timeline"+str(i)+".0.csv", sep=';',index_col=0)
        data_df = pd.concat([data_df, data_10_df])
        print(data_df.iloc[0])
    data_df.to_csv("../../../data/timeline_41.csv", sep=';', index=False)
         
if __name__ == "__main__":