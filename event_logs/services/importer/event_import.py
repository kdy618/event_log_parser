import pandas as pd

from event_logs import app


class EventImporter:
    """Reads events.csv file and saves in db"""

    def load_to_db(self):
        file_path = "/app/event_logs/static_data/events.csv"
        df = pd.read_csv(
            file_path,
            names=["customer_id", "event_type", "transaction_id", "timestamp"],
        )
        df["timestamp"] = pd.to_datetime(df["timestamp"])

        engine = app.get_engine()
        df.to_sql(con=engine, index_label="id", name="event_log", if_exists="replace")
