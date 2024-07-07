import json
import discord
import datetime
from ..config import SERVER_ICON, MEMBERSDATABASE, PROCEDUREDATABASE, SERVER_NAME


class Procedure:
  def __init__(self, staff: int, member: int, reason: str, procedure: str, duration: str, id: int, attachments: list, time):
    self.staff: int = staff
    self.member: int = member
    self.reason: str = reason
    self.procedure: str = procedure
    self.duration: str = duration
    self.id: int = id
    self.attachments: list = attachments
    self.time: datetime.datetime = time

  def get_member(self):
    return self.member

  def get_reason(self):
    return self.reason

  def get_procedure(self):
    return self.procedure

  def get_duration(self):
    return self.duration

  def get_staff(self):
    return self.staff

  def get_time(self):
    return self.time

  def get_id(self):
    return self.id

  def get_attachments(self):
    return self.attachments

  def to_json(self):
    return {"staff": self.staff, "member": self.member, "reason": self.reason, "procedure": self.procedure, "duration": self.duration, "id": self.id, "attachments": self.attachments, "time": self.time.strftime("%Y-%m-%d %H:%M:%S")}

  def to_embed(self):
    embed = discord.Embed(title = f"Proof {self.get_id()}", description = f"<@{self.get_member()}>", color = 0x00ff00, timestamp=self.get_time())
    embed.add_field(name = "Staff 🤵", value = f"<@{self.get_staff()}>", inline = True)
    embed.add_field(name = "Reason 📝", value = f"{self.get_reason()}", inline = True)
    embed.add_field(name = "Procedure 🔑", value = f"{self.get_procedure()}", inline = True)
    embed.add_field(name = "Duration ⏲️", value = f"{self.get_duration()}", inline = True)
    embed.add_field(name = "Attachments 🧾", value = f"{self.get_attachments()}", inline = True)
    embed.set_footer(text=f"{SERVER_NAME}", icon_url=f"{SERVER_ICON}")
    return embed

  def __repr__(self) -> str:
    return (
      f'<id={self.id} member={self.member} staff={self.staff} time={self.time}'
      f' reason={self.reason} procedure={self.procedure} duration={self.duration}>'
    )

class ProcedureManager:
  def __init__(self):
    self.procedures: list = []
    with open(PROCEDUREDATABASE, "r") as f:
      data = json.load(f)
    for i in data:
      self.procedures.append(Procedure(data[i]["staff"], data[i]["member"], data[i]["reason"], data[i]["procedure"], data[i]["duration"], data[i]["id"], data[i]["attachments"], data[i]['time']))

  def add_procedure(self, procedure: Procedure):
    self.procedures.append(procedure)
    with open(MEMBERSDATABASE, "r") as f:
      data = json.load(f)
    if str(procedure.get_staff()) in data:
      data[str(procedure.get_staff())]["procedures_count"] += 1
    else:
      data[str(procedure.get_staff())] = {"id": procedure.get_staff(), "procedures_count": 1}
    with open(MEMBERSDATABASE, 'w') as new_user_data:
      json.dump(data, new_user_data, indent=4)
  
  def get_procedure_count(self):
    return len(self.procedures)

  def get_procedures(self):
    return self.procedures

  def get_procedure_by_id(self, id: int) -> Procedure:
    for procedure in self.procedures:
      if procedure.get_id() == id:
        return procedure

  def get_procedure_by_member(self, member: int) -> Procedure:
    for procedure in self.procedures:
      if procedure.get_member() == member:
        return procedure

  def get_procedure_by_staff(self, staff: int) -> Procedure:
    for procedure in self.procedures:
      if procedure.get_staff() == int(staff):
        return procedure

  def get_procedures_by_member(self, member: int) -> list[Procedure]:
    procedures_by_member: list = []
    for procedure in self.procedures:
      if procedure.get_member() == member:
        procedures_by_member.append(procedure)
    return procedures_by_member

  def get_procedures_by_staff(self, staff: int) -> list[Procedure]:
    procedures_by_staff: list = []
    for procedure in self.procedures:
      if procedure.get_staff() == staff:
        procedures_by_staff.append(procedure)
    return procedures_by_staff

  def remove_procedure(self, procedure: Procedure):
    print("old one: ", self.procedures)
    self.procedures.remove(procedure)
    with open(PROCEDUREDATABASE, "r") as f:
      data = json.load(f)
    del data[str(procedure.get_id())]
    with open(PROCEDUREDATABASE, 'w') as new_user_data:
      json.dump(data, new_user_data, indent=4)