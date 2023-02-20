from event_logs.database import Column, PkModel, db

class EventLog(PkModel):
    __tablename__ = "event_log"

    customer_id = Column(db.Text)
    event_type = Column(db.Text)
    transaction_id = Column(db.Text)
    timestamp = Column(db.DateTime)
