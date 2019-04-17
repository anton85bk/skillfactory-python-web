#!/usr/bin/python3

" Анализирует файл и находит в нём: самый частый IP и информацию о нём "

import csv

data = {}
top_count = 0
top_ip = ""
total_records = 0
with open("m5-access-log-all.csv", "r") as file:
    input_data = csv.reader(file)

    # skip csv header
    (timestamp, ip, user_agent) = input_data.__next__()

    for (timestamp, ip, user_agent) in input_data:
        total_records += 1
        if ip in data:
            data[ip] = [data[ip][0] + 1, user_agent, timestamp]
            if data[ip][0] > top_count:
                top_count = data[ip][0]
                top_ip = ip

        else:
            data[ip] = [1, user_agent, timestamp]

suspicious_agent = {
    "ip" : top_ip,
    "fraction" : (top_count * 100 / total_records),
    "count" : top_count,
    "last" : {
        "agent" : data[top_ip][1],
        "timestamp" : data[top_ip][2]
    }
}
print(repr(suspicious_agent))
