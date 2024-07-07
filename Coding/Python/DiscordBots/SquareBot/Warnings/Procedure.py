import discord
import datetime

class Procedure:
  def __init__(self, staff: discord.Member, member: str, reason: str, procedure: str, duration: str, id: int, attachments: list):
    self.staff: discord.Member = staff
    self.member: str = member
    self.reason: str = reason
    self.procedure: str = procedure
    self.duration: str = duration
    self.id: int = id
    self.attachments: list = attachments
    self.time: datetime.datetime = datetime.datetime.now()

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

  def __repr__(self) -> str:
    return (
      f'<Member id={self.id} member={self.member} staff={self.staff} time={self.time}'
      f' reason={self.reason} procedure={self.procedure} duration={self.duration}>'
    )

class ProcedureManager:
  def __init__(self):
    self.procedures: list = []

  def add_procedure(self, procedure: Procedure):
    self.procedures.append(procedure)
  
  def get_procedure_count(self):
    return len(self.procedures)

  def get_procedures(self):
    return self.procedures

  def get_procedure_by_id(self, id: int):
    for procedure in self.procedures:
      if procedure.get_id() == id:
        return procedure

  def get_procedure_by_member(self, member: str):
    for procedure in self.procedures:
      if procedure.get_member() == member:
        return procedure

  def get_procedure_by_staff(self, staff: discord.Member):
    for procedure in self.procedures:
      print(procedure.get_staff())
      print(type(staff))
      if procedure.get_staff() == staff:
        return procedure

  def get_procedures_by_member(self, member: str):
    procedures_by_member: list = []
    for procedure in self.procedures:
      if procedure.get_member() == member:
        procedures_by_member.append(procedure)
    return procedures_by_member

  def get_procedures_by_staff(self, staff: discord.Member):
    procedures_by_staff: list = []
    for procedure in self.procedures:
      if procedure.get_staff() == staff:
        procedures_by_staff.append(procedure)
    return procedures_by_staff

  def remove_procedure(self, procedure: Procedure):
    self.procedures.remove(procedure)

