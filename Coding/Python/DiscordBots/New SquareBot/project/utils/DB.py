import datetime
from tinydb import TinyDB, Query

from project.utils.utils import ListSortWay
db = TinyDB(r'project\assets\databases\Members.json', indent=2, separators=(',', ': '))

# time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %p')

def get_member(id: int):
  User = Query()
  member = db.get(User.id == id)
  if member:
    return member
  else: 
    return None

def get_top(type: str, top: int):
  members = get_all(type)
  if members == None or len(members) == 0: return None
  members.sort(key=ListSortWay, reverse=True)
  members = members[:top]
  return members

def get_all(type: str):
  User = Query()
  if type == 'all':
    return db.all()
  if type == 'staff':
    return db.search(User.staff == True)
  if type == 'members':
    return db.search(User.staff == False)

def get_member_xp(id: int):
  member = get_member(id)
  if member:
    return member['xp']
  else:
    return 0

def add_member(id: int, xp: int, staff: bool):
  User = Query()
  db.upsert({'id': id, 'xp': xp, 'staff': staff}, User.id == id)

def clear():
  db.truncate()