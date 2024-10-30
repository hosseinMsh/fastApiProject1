from datetime import datetime, timedelta
import requests

from sabtFaramoshi import addDataToDb

# Define your URL and other parameters for login
def getDataFromServer():
    url ="https://172.17.7.101"
    # username = usernames
    # password = passwords  # Securely get the password
    username = "admin"
    password = "hoss1383"
    url_login = f"{url}/api/login"
    headers = {
      'Content-Type': 'application/json'
    }

    payload = {
      "User": {
        "login_id": f"{username}",
        "password": f"{password}"
      }
    }

    # Disable SSL verification
    response_login = requests.post(url_login, headers=headers, json=payload, verify=False)
    authenticate_user = response_login.headers['bs-session-id']

    # New section for events search


    url_events = f"{url}/api/events/search"

    current_date = datetime.now() - timedelta(hours=3, minutes=30)
    adjusted_date = current_date
    first_date = current_date.replace(hour=0, minute=0, second=0, microsecond=0)
    formatted_first_date = first_date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    formatted_adjusted_date = adjusted_date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    payload_events ={
      "Query": {
        "limit": 2_000_000,
        "conditions": [
          {
            "column": "datetime",
            "operator": 3,
            "values": [
              f"{formatted_first_date}",
              f"{formatted_adjusted_date}",
            ]
          }
        ],
        "orders": [
          {
            "column": "datetime",
            "descending": True
          }
        ]
      }
    }

    headers_events = {
      'bs-session-id': authenticate_user,  # Use the session ID from the login response
      'Content-Type': 'application/json',

    }

    response_events = requests.post(url_events, headers=headers_events, json=payload_events, verify=False).json()

    # print(response_events)

    rows_with_code_4867 = [row for row in response_events['EventCollection']['rows'] if row['event_type_id']['code'] in ["4867","4102"]]


    fields = ['event id', 'name', 'job id', 'id cart', 'time event', 'type event']
    date = datetime.now().strftime('%Y-%m-%d')
    # print(date)
    # Open the CSV file for writing

    for row in rows_with_code_4867:
        eventID = row['id']
        names = row['user_id']['name']
        job_id = row['user_id']['user_id']
        time_event = row['datetime']
        time_event_datetime = datetime.strptime(time_event[:-1], '%Y-%m-%dT%H:%M:%S.%f')
        time_event_datetime += timedelta(hours=3, minutes=30)
        datetime_obj = time_event_datetime
        day = datetime_obj.date()
        time = datetime_obj.time()
        door = row['device_id']['name']

        # Determine the type of event based on the event_type_id code
        if row['event_type_id']['code'] == "4867":
            typeEvent = "face"
        else:
            typeEvent = "cart"

        # Set type_ to 0, letting addDataToDb determine if it's an entry or exit
        type_ = 0

        # Call addDataToDb with the extracted information
        addDataToDb(names, job_id, day, time, type_, door, typeEvent)


# Call the function to fetch and process data
getDataFromServer()