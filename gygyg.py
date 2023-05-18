from datetime import datetime
from dateutil import tz

print(datetime.now().astimezone())

tz = tz.gettz("America/Havana")
x = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 9, 54, 00, 0o40153, tz).time()

print(x, type(x))
print(tz)