import requests
from datetime import datetime, timedelta
import cgi

form = cgi.FieldStorage()
api_token = form.getfirst("api_token", None)
date_to_copy = form.getfirst("date_to_copy", None)
start = form.getfirst("start", None)
end = form.getfirst("end", None)
target_weekday = form.getfirst("target_weekday", None)
weekday_filter = form.getfirst("weekday_filter", None)


# api_token = "f7b21441c6aa6fa57f66a3aa4b"


# task_id = 67506246  # refinement
# task_id = 67722746  # daily
# task_id = 68282992  # retro
# task_id = 67506230  # demo
# task_id = 67549535  # sprint planning

def get_tasks_ids(date="2021-05-12"):
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
    print(ids)
    return ids


def date_to_days(start, end, target_weekday, d_filter=False):
    start = datetime.strptime(str(start), "%Y-%m-%d")
    end = datetime.strptime(str(end), "%Y-%m-%d")
    dates_list = []
    filtered_list = []
    end_data = end + timedelta(days=1)
    while start.strftime("%Y-%m-%d") != end_data.strftime("%Y-%m-%d"):
        date_day = start.strftime("%A")
        if target_weekday in date_day:
            dates_list.append(start.strftime("%Y-%m-%d"))
        start = start + timedelta(days=1)
    if d_filter:
        for datee in range(0, len(dates_list), 2):
            filtered_list.append(dates_list[datee])
        return filtered_list
    else:
        return dates_list


def post(date, task, start_time, end_time):
    data = {
        'date': date,
        'start_time': start_time,
        'end_time': end_time,
        'task_id': task
    }
    requests.post(f"https://app.timecamp.com/third_party/api/entries/format/json/api_token/{api_token}",
                  json=data)


def fill_timecamp(date_to_copy, start, end, target_weekday, d_filter):
    list_of_days = date_to_days(start=start, end=end, target_weekday=target_weekday, d_filter=d_filter)
    tasks_ids = get_tasks_ids(date=date_to_copy)
    for tid in tasks_ids:
        start_time = tasks_ids[tid].get('start_time')
        end_time = tasks_ids[tid].get('end_time')
        for date in list_of_days:
            post(date, tid, start_time, end_time)


fill_timecamp(date_to_copy=date_to_copy, start=start, end=end, target_weekday=target_weekday, d_filter=weekday_filter)

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
