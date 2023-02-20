import pandas as pd

from flask import current_app

class EventImporter():
    def load_to_db(self): 
        df = pd.read_csv('/app/event_logs/static_data/events.csv',
                        names=["customer_id", "event_type", "transaction_id", "timestamp"])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        engine = self._get_engine()
        df.to_sql(con=engine, index_label='id', name="event_log", if_exists='replace')

    def _get_engine(self):
        try:
            # this works with Flask-SQLAlchemy<3 and Alchemical
            return current_app.extensions['migrate'].db.get_engine()
        except TypeError:
            # this works with Flask-SQLAlchemy>=3
            return current_app.extensions['migrate'].db.engine


""" 

import pandas as pd

# read the CSV file into a Pandas DataFrame
df = pd.read_csv('log_events.csv')

# convert the 'timestamp' column to datetime format
df['timestamp'] = pd.to_datetime(df['timestamp'])

# set the 'timestamp' column as the index
df.set_index('timestamp', inplace=True)

# define the start and end times
start_time = pd.to_datetime('2023-02-15 00:00:00')
end_time = pd.to_datetime('2023-02-16 00:00:00')

# filter the DataFrame to include only events between the start and end times
filtered_df = df.loc[start_time:end_time]

# group the events by hour and count the number of events in each hour
event_counts = filtered_df.groupby(pd.Grouper(freq='1H')).size()

print(event_counts)



In this code, we first read the CSV file into a Pandas DataFrame and convert the 'timestamp' column to datetime format. We then set the 'timestamp' column as the index of the DataFrame, which will allow us to easily filter the DataFrame based on the start and end times.

Next, we define the start and end times as datetime objects and use them to filter the DataFrame to include only events between those times. We then group the filtered DataFrame by hour using the pd.Grouper function with a frequency of '1H', and count the number of events in each hour using the size() function.

Finally, we print the resulting event counts. Note that the output will be a Pandas Series with a datetime index, where each value represents the number of events that occurred in the corresponding hour. 

"""
