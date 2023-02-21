from event_logs import app

class EventLogService:
    def get_events_by_customer_id(self, customer_id):
        query = """SELECT customer_id, transaction_id, timestamp
                FROM event_log 
                WHERE customer_id = "{}" 
                """.format(customer_id)
    
        results = self._execute_sql_query(query)
        return results

    def get_events_by_customer_id_and_time(self, customer_id, start_time, end_time):
        query = """SELECT  
                strftime('%Y-%m-%d %H:00:00', timestamp) AS hour_bucket, 
                COUNT(transaction_id) AS total_transactions
                FROM event_log 
                WHERE customer_id = "{}" AND timestamp > "{}" AND timestamp < "{}"
                Group By hour_bucket
                ORDER By hour_bucket ASC""".format(customer_id, start_time, end_time) 
                
        results = self._execute_sql_query(query)
        return {"results":results,"customer_id":customer_id}

    def _execute_sql_query(self, query):
        results = []
        with app.get_engine().connect() as con:
            rs = con.execute(query)
            for row in rs:
                results.append(dict(row))
        return results 
        
            