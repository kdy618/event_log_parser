# event_logs

Simple flask app that loads events.csv (static data) and provides view to display the events customer X sends in one hour buckets between timestamp A and B. In this app, timestamp A and B are represented as start and end time. To run the app, please follow the steps below. 

## 1. Docker Quickstart

This app can be run completely using `Docker` and `docker-compose`. **Using Docker is recommended, as it guarantees the application is run using compatible versions of Python and Node**.

To run the development version of the app

```bash
docker-compose up flask-dev
```

## 2. Go to [http://localhost:8080](http://localhost:8080)
Before clicking "Try Me" button to view event log by customerId and/or time, click the button to import the data. 

The "Try Me" button for "View by CustomerId & Time" passes in timestamp A and B. If you'd like to verify/view all the event logs for customer X, click "Try Me" button for "View by Customer Id" to verify returned results for "View by CustomerId & Time". 

If you'd like to try passing in different timestamp A and B, feel free to tweak datetime values on URL below. 

Example: "http://localhost:8080/query/30330c9c4e7173ba9474c46ee5191570/2021-03-01 04:00:00.00000/2021-03-01 06:00:00.848000" 
