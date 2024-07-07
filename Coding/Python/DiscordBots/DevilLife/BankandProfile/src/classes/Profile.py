from .. import config
from tinydb import TinyDB, Query
from dataclasses import dataclass, Field

Profile_Database: TinyDB = TinyDB(config.PROFILES_DATABASE, indent=2, separators=(',', ': '))


@dataclass()
class Profile(object):
  # def __init__(self, name: str, id: str, staff: str, place_of_birth: str, date_of_birth: str, character: str, image: str, member_id: int) -> None:
  name: str
  id: str
  staff: str = Field(repr=False)
  place_of_birth: str = Field(repr=False)
  date_of_birth: str = Field(repr=False)
  character: str = Field(repr=False)
  image: str = Field(repr=False)
  discord_member_id: int = Field(repr=False)


class ProfilesManager():
  def __init__(self) -> None:
    self.profiles: list = []
    data = Profile_Database.all()
    for i in data:
      self.profiles.append(Profile(**i))

  def getProfileById(self, id: str) -> Profile:
    for i in self.profiles:
      if i.getId() == id:
        return i

  def getProfileByName(self, Name: str) -> Profile:
    for i in self.profiles:
      if i.getName() == Name:
        return i
  
  def getProfileByMemberId(self, discord_member_id: int) -> Profile:
    for i in self.profiles:
      if i.getMemberId() == discord_member_id:
        return i
    return None

  def add_profile(self, profile: Profile):
    self.profiles.append(profile)
    Profile_Database.insert(profile.__dict__)

  def remove_profile(self, profile: Profile):
    self.profiles.remove(profile)
    profileToDelete: Query = Query()
    Profile_Database.remove(profileToDelete.id == profile.getId())



PROFILES_MANAGER: ProfilesManager = ProfilesManager()