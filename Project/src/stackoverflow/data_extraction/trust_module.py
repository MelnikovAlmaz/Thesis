import pandas as pd
import datetime
import numpy as np
import seaborn as sns


data_folder = "/home/almaz/Thesis/Project/data/"


def generate_3_factors():
    user_df = pd.read_csv(data_folder + "user_set.csv", sep=';')[['account_id', 'reputation', 'creation_date']]
    timeline_df = pd.read_csv(data_folder + "timeline_103.csv", sep=';')
        
    user_id_list = timeline_df['user_id'].unique().tolist()
    
    user_df = user_df[user_df['account_id'].isin(user_id_list)]
    user_df['creation_date'] = pd.to_datetime(user_df['creation_date'])
    action_count = timeline_df.shape[0]
    
    current_day = datetime.datetime(2017, 8, 14).timestamp()
    
    start_day = datetime.datetime(2008, 7, 31).timestamp()
    
    system_livetime = current_day - start_day
    
    user_df['presence'] = user_df['creation_date'].astype(np.int64) // 10**9
    user_df['creation_date_int'] = user_df['creation_date'].astype(np.int64) // 10**9
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
    user_df['frequency_factor'] = user_df['frequency_factor'].apply(lambda x: 1 if x > 1 else x)
    user_df.to_csv(data_folder + "user_param_3_new.csv", sep=';', index=False)


def generate_4_factors():
    user_df = pd.read_csv(data_folder + "user_param_3_new.csv", sep=';')
    user_df['creation_date'] = pd.to_datetime(user_df['creation_date'])
    user_df['creation_date_int'] = user_df['creation_date'].astype(np.int64) // 10**9
    user_df['regularity_factor'] = np.zeros(user_df.shape[0])
    
    timeline_df = pd.read_csv(data_folder + "timeline_103.csv", sep=';')
    timeline_df['creation_date'] = pd.to_datetime(timeline_df['creation_date'])
    timeline_df['creation_date'] = timeline_df['creation_date'].astype(np.int64) // 10**9
    
    user_id_list = user_df['account_id'].tolist()
    frequency = 86400 # one day
    current_day = datetime.datetime(2017, 8, 14).timestamp()
    
    for user_id in user_id_list:
        user_timeline = timeline_df[timeline_df['user_id'] == user_id]
        user_info = user_df[user_df['account_id'] == user_id].iloc[0]
        
        born_time = user_info['creation_date_int']
        start_time  = born_time
        end_time = start_time + frequency
        
        reg_count = 0
        
        while end_time < current_day:
            user_period_timeline = user_timeline[(user_timeline['creation_date'] >= start_time) & (user_timeline['creation_date'] < end_time)]
            if user_period_timeline.shape[0] > 0:
                reg_count += 1
            
            start_time = end_time
            end_time += frequency
        period_count = int((current_day - born_time) / frequency)
        regularity_factor = reg_count / period_count
        user_df.regularity_factor[user_df.account_id == user_id] = regularity_factor

    user_df.to_csv(data_folder + "user_param_4_new.csv", sep=';', index=False)

def calculate_trust():
    user_df = pd.read_csv(data_folder + "user_param_4_new.csv", sep=';')
    #user_df['frequency_factor'] = user_df['frequency_factor'].apply(lambda x: 1 if x > 1 else x)
    #user_df['presence_factor'] = (user_df['presence_factor'] - user_df['presence_factor'].min()) / (user_df['presence_factor'].max() - user_df['presence_factor'].min())
    #user_df['activity_factor'] = (user_df['activity_factor'] - user_df['activity_factor'].min()) / (user_df['activity_factor'].max() - user_df['activity_factor'].min())
    #user_df['regularity_factor'] = (user_df['regularity_factor'] - user_df['regularity_factor'].min()) / (user_df['regularity_factor'].max() - user_df['regularity_factor'].min())
    #user_df['frequency_factor'] = (user_df['frequency_factor'] - user_df['frequency_factor'].min()) / (user_df['frequency_factor'].max() - user_df['frequency_factor'].min())
    
    
    user_df['trust'] = user_df['presence_factor']/3 + user_df['activity_factor']/4 + user_df['regularity_factor']/4 + user_df['frequency_factor']/6
    user_df.to_csv(data_folder + "user_trust_new.csv", sep=';', index=False)
    corr = user_df.corr()
    sns.heatmap(corr)
    
if __name__ == "__main__":
    #generate_4_factors()
    calculate_trust()