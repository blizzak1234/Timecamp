import requests
from datetime import datetime, timedelta
import cgi
import pandas as pd

form = cgi.FieldStorage()
api_token = form.getfirst("api_token", None)
date_to_copy_start = form.getfirst("date_to_copy_start", None)
date_to_copy_end = form.getfirst("date_to_copy_end", None)
target_date_start = form.getfirst("target_date_start", None)
target_date_end = form.getfirst("target_date_end", None)
target_weekday = form.getfirst("target_weekday", None)
weekday_filter = form.getfirst("weekday_filter", None)


# task_id = 67506246  # refinement
# task_id = 67722746  # daily
# task_id = 68282992  # retro
# task_id = 67506230  # demo
# task_id = 67549535  # sprint planning

def get_tasks_ids(date="2021-07-30"):
    ids = {}
    data = {"from": date, "to": date}
    response = requests.get(f"https://app.timecamp.com/third_party/api/entries/format/json/api_token/{api_token}",
                            params=data)

    json_resp = response.json()
    for entity in json_resp:
        tsk_id = entity.get('task_id')
        task_st = entity.get('start_time')
        task_end = entity.get('end_time')
        ids[tsk_id] = {"start_time": task_st, "end_time": task_end}
    return ids


# date_to_copy_start = "2021-11-01"
# date_to_copy_end = "2021-11-05"
# target_date_start = "2021-12-06"
# target_date_end = "2021-12-10"


init_dates = pd.date_range(start=date_to_copy_start, end=date_to_copy_end).astype(str).tolist()
target_dates = pd.date_range(start=target_date_start, end=target_date_end).astype(str).tolist()
dates_dict = dict(zip(target_dates, init_dates))


def post(task_id, task_time_range, target_date):
    data = {
        'date': target_date,
        'start_time': task_time_range.get('start_time'),
        'end_time': task_time_range.get('end_time'),
        'task_id': task_id
    }
    requests.post(f"https://app.timecamp.com/third_party/api/entries/format/json/api_token/{api_token}",
                  json=data)


def fill_timecamp2():
    for target_date, init_date in dates_dict.items():
        # for init_date in init_dates:
        init_tasks = get_tasks_ids(str(init_date).split()[0])
        for task_id, task_time_range in init_tasks.items():
            post(task_id, task_time_range, str(target_date).split()[0])


fill_timecamp2()

print("Content-type: text/html\n")
print("""<!DOCTYPE HTML>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Filling result</title>
        </head>
        <body>""")

print("<h1>Timecamp is filled</h1>")
print("""</body>
        </html>""")
