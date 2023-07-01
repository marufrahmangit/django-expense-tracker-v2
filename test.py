from datetime import datetime

now = datetime.now()

print(now.strftime("%d/%m/%Y, %H:%M:%S"))
print(now.strftime("%Y-%m-%d %H:%M:%S"))

time = "2023-06-10  3:30:00 PM"
time2 = "6/10/2023  3:30:00 PM"
print(datetime.strptime(time, "%Y-%m-%d %H:%M:%S %p"))
print(datetime.strptime(time2, "%m/%d/%Y %H:%M:%S %p"))

