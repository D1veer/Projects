from dataclasses import dataclass, field
from enum import Enum

class Type(Enum):
  R1 = 1
  R2 = 2
  R3 = 3
  R4 = 4

@dataclass()
class Remnant():
  id: int = field(compare=False)
  title: str = field(compare=True)
  cash: int = field(compare=False)
  type: Type = field(compare=False)
  
  def __str__(self) -> str:
    return f'{self.title}' 


Remnants: list[Remnant] = [
  Remnant(1, 'قطع إشارة', 3_000, Type.R1),
  Remnant(2, 'تفحيط في المدينة', 5_000, Type.R1),
  Remnant(3, 'سرعة داخل المدينة', 3_000, Type.R1),
  Remnant(4, 'صدم عسكري', 8_000, Type.R1),
  Remnant(5, 'وقوف خاطئ', 1_000, Type.R1),
  Remnant(5, 'عكس سير', 3_000, Type.R1),
  Remnant(6, 'وقوف فوق الرصيف', 5_000, Type.R1),
  Remnant(7, 'عرقلة السير', 1_000, Type.R1),
  Remnant(8, 'تجارة ممنوعات', 8_000, Type.R2),
]

class RemnantManager(object):
  def __init__(self):
    self.remnants: list[Remnant] = Remnants
    
  def getRemnant(self, id) -> Remnant | None:
    for child in self.remnants:
      if child.id == id:
        return child
      
  def addRemnant(self, remnant: Remnant):
    self.remnants.append(remnant)
  
  def getRemnantByName(self, name: str):
    for child in self.remnants:
      if name in child.title:
        return child 

  def getRemnants(self) -> list[Remnant]:
    return self.remnants

  def getRemnantsStr(self) -> list[str]:
    return [n.__str__() for n in self.remnants]

  def getRemnantsByType(self, Type: Type) -> list[Remnant]:
    rem: list[str] = []
    for n in self.remnants:
      if n.type == Type:
        rem.append(n)
    return rem

RM: RemnantManager = RemnantManager()