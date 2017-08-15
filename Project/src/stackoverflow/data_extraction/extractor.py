"""
Created on Wed Aug  9 09:44:36 2017

@author: almaz
"""

import stackexchange
import pandas as pd
import numpy as np
import random


data_folder = "/home/almaz/Thesis/Project/data/"

def generate_user_id():
    user_id_list = []
    max_id = 11490000
    random.seed(10)
    for i in range(10000, max_id, 10000):
        first_id = random.randrange(i, i+10000)
        second_id = random.randrange(i, i+10000)
        user_id_list.append(first_id)
        user_id_list.append(second_id)
    
    return user_id_list


def extract_user(id_list=[]):
    indexes = ('display_name',  'account_id', 'creation_date',
               'last_access_date', 'reputation')
    data = []
    so = stackexchange.Site(stackexchange.StackOverflow, app_key="A8wB710uq0)YLzS271nWug((")
    count = 0
    for user_id in id_list:
        try:
            user = so.user(user_id)
            data.append(user.display_name)
            data.append(user.account_id)
            data.append(user.creation_date)
            data.append(user.last_access_date)
            data.append(user.reputation)
        except :
            continue
        count += 1
        print("User " + user.display_name + " is added. - " + str(count))

    data_np = np.asarray(data)
    data_np = data_np.reshape((int(len(data)/len(indexes)), len(indexes)))
    print(data_np.shape)
    user_df = pd.DataFrame(data=data_np, columns=indexes)
    user_df.to_csv(data_folder + "user_new.csv", sep=';', index=False)


def extract_timeline():
    indexes = ['user_id', 'timeline_type', 'creation_date']
    so = stackexchange.Site(stackexchange.StackOverflow, app_key="A8wB710uq0)YLzS271nWug((")
    data_df = pd.read_csv(data_folder + "user_set.csv", sep=';')
    id_list = data_df['account_id'].tolist()
    count = 1
    timeline_list = []
    for user_id in id_list:
        try:
            user = so.user(user_id)
            timeline = user.timeline.fetch()
            print(user.display_name + " - " + str(count))
            for event in timeline:
                timeline_list.append(event.user_id)
                timeline_list.append(event.timeline_type)
                timeline_list.append(event.creation_date)
            if count % 10 == 0:
                data_np = np.asarray(timeline_list)
                data_np = data_np.reshape((int(len(timeline_list)/len(indexes)), len(indexes)))
                timeline_df = pd.DataFrame(data=data_np, columns=indexes)
                timeline_df.to_csv(data_folder + "timeline" + str(count/10) +".csv", sep=';')
                timeline_list = []
            count += 1
        except:
            print("Skip user - " + str(user_id))
            continue



def make_one_timelines():
    data_df = pd.read_csv(data_folder + "timeline1.0.csv", sep=';',index_col=0)
    print(data_df.shape)
    for i in range(2,104):
        data_10_df = pd.read_csv(data_folder + "timeline"+str(i)+".0.csv", sep=';',index_col=0)
        data_df = pd.concat([data_df, data_10_df])
        print(data_df.iloc[0])
    data_df.to_csv(data_folder + "timeline_103_all.csv", sep=';', index=False)


def make_one_user_data():
    user_df_400 = pd.read_csv(data_folder + "user.csv", sep=';')
    user_df_1528 = pd.read_csv(data_folder + "user_new.csv", sep=';')
    
    user_new_df = pd.concat([user_df_400, user_df_1528])
    user_new_df.to_csv(data_folder + "user_set.csv", sep=';', index=False)


if __name__ == "__main__":
    make_one_timelines()
    #extract_timeline()
    #make_one_user_data()
    #user_list = generate_user_id()
    #extract_user(user_list)