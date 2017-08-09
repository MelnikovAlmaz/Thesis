"""
Created on Wed Aug  9 09:44:36 2017

@author: almaz
"""

import stackexchange
import pandas as pd


indexes = ('display_name', 'profile_image', 'age', 'website_url',
           'location', 'about_me', 'view_count', 'up_vote_count',
           'down_vote_count', 'account_id', 'profile_image',
           'creation_date',
           'last_access_date',
           'reputation')
so = stackexchange.Site(stackexchange.StackOverflow)

for i in range(1, 100, 100):
    id_list = list(range(i, i+100))
    users = so.users(id_list)
    for user in users:
        print(user.reputation)
        #create_user(user)
