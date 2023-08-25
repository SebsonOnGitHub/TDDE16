import pandas as pd

def time_to_secs(raw_time):
    time_hours_secs = int(raw_time[0:2]) * 60 * 60
    time_minutes_secs = int(raw_time[3:5]) * 60
    time_secs = int(raw_time[6:8])
    time_tot_secs = time_hours_secs + time_minutes_secs + time_secs

    return time_tot_secs

def set_date_to_NASDAQ():
    file_path = 'Elon_2017-2022_tworows.xls'
    df = pd.read_excel(file_path)

    opening_time_secs = time_to_secs("14:30:00")
    closing_time_secs = time_to_secs("21:00:00")

    for i in range(len(df)):
        raw_date = df.iloc[i, 0][0:10]
        raw_time = df.iloc[i, 0][11:19]

        tweet_time_secs = time_to_secs(raw_time)
        additional_days = 0

        if tweet_time_secs >= opening_time_secs and tweet_time_secs <= closing_time_secs:
            #print(raw_time + ": is during open hours")
            additional_days = 0
        elif tweet_time_secs > closing_time_secs:
            #print(raw_time + ": is after open hours")
            additional_days = 1
        elif tweet_time_secs < opening_time_secs:
            #print(raw_time + ": is before open hours")
            additional_days = 0
        else:
            print("Something went wrong")

        enddate = pd.to_datetime(raw_date) + pd.DateOffset(days=additional_days)

        if enddate.dayofweek >= 5:
            enddate = pd.to_datetime(enddate) + pd.DateOffset(days= 7 - enddate.dayofweek)

        df.iloc[i, 1] = str(enddate)[0:10]

    df.to_excel('test_res.xlsx')

def fuse():
    file_path = 'Elon_2017-2022.xls'
    df_tweets = pd.read_excel(file_path)

    file_path = 'Master.xls'
    df_stock = pd.read_excel(file_path)

    for i in range(len(df_tweets)):
        for j in range(len(df_stock)):
            if df_tweets.iloc[i, 1] == df_stock.iloc[j, 0]:
                df_tweets.iloc[i, 7] = df_stock.iloc[j, 1]
                df_tweets.iloc[i, 8] = df_stock.iloc[j, 2]
                df_tweets.iloc[i, 9] = df_stock.iloc[j, 3]
                df_tweets.iloc[i, 10] = df_stock.iloc[j, 4]

    df_tweets.to_excel('test_res.xlsx')

fuse()
