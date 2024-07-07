from tinydb import TinyDB, Query

db = TinyDB(r'project\assets\databases\MC.json', indent=2, separators=(',', ': '))

def get_member(member_id: str):
  """Get a Member By Id From The Database"""
  re = db.get(Query().ign == member_id)
  if re:
    return re["id"]
  else:
    return "Not linked"

# def add_member()