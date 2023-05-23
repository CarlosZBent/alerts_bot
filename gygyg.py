from datetime import datetime, timedelta
from dateutil import tz

print(datetime.now().date() - timedelta(1))

tz = tz.gettz("America/Havana")
x = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 9, 54, 00, 0o40153, tz).time()

print(x, type(x))
print(tz)