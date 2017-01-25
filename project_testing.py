
# coding: utf-8

# In[42]:

import csv
import pandas as pd
import pickle
import os
import datetime
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('fivethirtyeight')
get_ipython().magic('matplotlib inline')


# In[6]:

ospath = os.path.abspath('C:/Users/Leonard/Downloads/Dataset/F1_All_Traffic.csv')


# In[9]:

data1 = pd.read_csv(ospath)


# In[12]:

data1.columns.values


# In[33]:

data1[data1.columns.values[14:35]].head(30)


# In[16]:

def roundTime(dt=None, dateDelta=datetime.timedelta(minutes=1)):
    """Round a datetime object to a multiple of a timedelta
    dt : datetime.datetime object, default now.
    dateDelta : timedelta object, we round to a multiple of this, default 1 minute.
    Author: Thierry Husson 2012 - Use it as you want but don't blame me.
            Stijn Nevens 2014 - Changed to use only datetime objects as variables
    """
    roundTo = dateDelta.total_seconds()

    if dt == None : dt = datetime.datetime.now()
    seconds = (dt - dt.min).seconds
    # // is a floor division, not a comment on following line:
    rounding = (seconds+roundTo/2) // roundTo * roundTo
    return dt + datetime.timedelta(0,rounding-seconds,-dt.microsecond)


# In[20]:

roundTime(datetime.datetime(2016,12,31,23,37,32),datetime.timedelta(minutes=15))


# In[24]:

datetime.datetime.strptime('2016-12-16 02:00:52','%Y-%m-%d %H:%M:%S')


# In[25]:

data1['update_time_datetime'] = data1.apply(lambda x: datetime.datetime.strptime(x['update_time'],'%Y-%m-%d %H:%M:%S'),axis=1)


# In[26]:

data1['update_time15'] = data1.apply(lambda x: roundTime(x['update_time_datetime'],datetime.timedelta(minutes=15)),axis=1)


# In[53]:

list(data1.info_5.unique())[0] is not np.nan


# In[54]:

data1['sent_bytes'] = data1.apply(lambda x: int(x['info_5'].split('; ')[1].split('=')[1]) if x['info_5'] is not np.nan else 0,axis=1)
data1['rcvd_bytes'] = data1.apply(lambda x: int(x['info_5'].split('; ')[2].split('=')[1]) if x['info_5'] is not np.nan else 0,axis=1)


# In[ ]:




# In[57]:

data1.fillna(0,inplace=True)


# In[68]:

min(data1.update_time15.values)


# In[74]:

data1[(data1.update_time15>=datetime.datetime(2017,1,2,0,0,0)) & (data1.update_time15<datetime.datetime(2017,1,5,0,0,0))].groupby(['update_time15'])['rcvd_bytes','sent_bytes'].sum().apply(lambda x: x/1024/1024/1024).plot(kind='line',figsize=(12,6))


# In[40]:

int('duration=30; sent_bytes=75; rcvd_bytes=234'.split('; ')[2].split('=')[1])

