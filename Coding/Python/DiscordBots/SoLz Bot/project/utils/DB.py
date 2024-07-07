import datetime
import time
from tinydb import TinyDB, Query
db = TinyDB(r'project\assets\databases\db.json', indent=2, separators=(',', ': '))
User = Query()

time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %p')

print(time_now)