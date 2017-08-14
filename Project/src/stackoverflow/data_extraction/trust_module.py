import pandas as pd
import datetime
import numpy as np

user_df = pd.read_csv("../../../data/user.csv", sep=';')[['account_id', 'reputation', 'creation_date']]
timeline_df = pd.read_csv("../../../data/timeline_41.csv", sep=';')
    
user_id_list = timeline_df['user_id'].unique().tolist()

user_df = user_df[user_df['account_id'].isin(user_id_list)]
user_df['creation_date'] = pd.to_datetime(user_df['creation_date'])
action_count = timeline_df.shape[0]

current_day = datetime.datetime(2017, 8, 14).timestamp()

start_day = datetime.datetime(2008, 7, 31).timestamp()

system_livetime = current_day - start_day

user_df['presence'] = user_df['creation_date'].astype(np.int64) // 10**9
user_df['presence'] = current_day - user_df['presence']
user_df['presence_factor'] = user_df['presence'] / system_livetime

activity_series = timeline_df.groupby(['user_id'])['creation_date'].count()
activity_indexes = activity_series.index.values.tolist() 
activity_df = pd.DataFrame()
activity_df['account_id'] = activity_indexes
activity_df['activity'] = activity_series.tolist()

user_df = pd.merge(user_df, activity_df, on='account_id')
user_df['activity_factor'] = user_df['activity'] / action_count

frequency = 86400 # one day

user_df['frequency_factor'] = user_df['activity'] * frequency / user_df['presence']

user_df.to_csv("../../../data/user_param_3.csv", sep=';', index=False)
