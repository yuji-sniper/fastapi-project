import datetime
import time

now = datetime.datetime.now()
print(now)
print(now.isoformat())
print(now.strftime('%d/%m/%Y-%H:%M:%S:%f'))

today = datetime.date.today()
print(today)
print(today.isoformat())
print(today.strftime('%d/%m/%Y'))

t = datetime.time(hour=1, minute=10, second=5, microsecond=100)
print(t)
print(t.isoformat())
print(t.strftime('%H:%M:%S:%f'))

print(now)
d = datetime.timedelta(weeks=1)
print(now - d)

# print('###')
# time.sleep(1)
# print('###')

print(time.time())
