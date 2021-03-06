#%%

import datetime
import pandas as pd
from collections import Counter

#%%

df=pd.read_json('new_parsed_tweets_closed.json')
df2=pd.read_csv('parsed_new.csv', encoding='windows-1252')


#%%

all_hashtags=[]
for hashtags in df['hashtags_list']:
    for item in list(hashtags):
        all_hashtags.append(item)
        #print(item)


all_hashtags=sorted(all_hashtags)

#%%
stats=(Counter(all_hashtags ))
common_hashtags=stats.most_common(30)
comm=[]
for i in common_hashtags:
    comm.append(i[0])
#%%
print(comm)
a = datetime.date.today()
numdays = 13
date_list = []
for x in range (0, numdays):
    date_list.append(a - datetime.timedelta(days = x))

print (date_list)
print(date_list[0])
df['created_at']=pd.to_datetime(df['created_at'])
df['created_at']=df['created_at'].apply(lambda x: x.replace(tzinfo=None))
df['created_at']=df['created_at'].dt.date
new_data=[]
for date in date_list:
    df_filtered=df[((df["created_at"]==date))]
    print(df_filtered)
    for hashtag in comm:
        new_row=[0]*6
        #print(new_row)
        for index, row in df_filtered.iterrows():
            #print(row
            #print(row["created_at"].day )
            if hashtag in row["hashtags_list"]:
                new_row[0]=date
                new_row[1]=hashtag
                new_row[2]+=1
                new_row[3]+=row["retweet_count"]
                new_row[4]+=row["favorite_count"]
                new_row[5]+=row["user_followers_count"]
                # print("luj")
                # print(new_row)
                #df.drop(index)
        new_data.append(new_row)
        #print(new_data)


new_df=pd.DataFrame.from_records(new_data)
print(new_df)