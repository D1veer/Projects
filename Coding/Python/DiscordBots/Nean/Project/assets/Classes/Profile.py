import json
import re
from tkinter import Image
from Project.config import PROFILESDATABASE

class Profile():
  def __init__(self, name: str, id: str, staff: str, place_of_birth: str, date_of_birth: str, character: str, image: str, member_id: int) -> None:
    self.name: str = name
    self.id: str = id
    self.staff: str = staff
    self.place_of_birth: str = place_of_birth
    self.date_of_birth: str = date_of_birth
    self.character: str = character
    self.image: str = image
    self.member_id: int = member_id

  def getName(self) -> str:
    return self.name

  def getId(self) -> str:
    return self.id

  def getImage(self) -> str:
    return self.image

  def getStaff(self) -> str:
    return self.staff

  def getPlaceOfBirth(self) -> str:
    return self.place_of_birth

  def getDateOfBirth(self) -> str:
    return self.date_of_birth

  def getCharacter(self) -> str:
    return self.character

  def getMemberId(self) -> int:
    return self.member_id

class ProfilesManager():
  def __init__(self) -> None:
    self.profiles: list = []
    with open(PROFILESDATABASE, "r") as f:
      data = json.load(f)
    for i in data:
      self.profiles.append(Profile(data[i]["name"], data[i]["id"], data[i]["staff"], data[i]["place_of_birth"], data[i]["date_of_birth"], data[i]["character"], data[i]["image"], data[i]["member_id"]))


  def getProfileById(self, id: str) -> Profile:
    for i in self.profiles:
      print(id, i.getId)
      if i.getId() == id:
        print(id, i.getId)
        print("True")
        return i

  def getProfileByName(self, Name: str) -> Profile:
    for i in self.profiles:
      if i.getName() == Name:
        return i
  
  def getProfileByMemberId(self, member_id: int) -> Profile:
    for i in self.profiles:
      if i.getMemberId() == member_id:
        return i
      else:
        return False

  def add_profile(self, profile: Profile):
    self.profiles.append(profile)
    with open(PROFILESDATABASE, "r") as f:
      data = json.load(f)
    data[str(profile.getId())] = {"id": profile.getId(), "name": profile.getName(), "staff": profile.getStaff(), "place_of_birth": profile.getPlaceOfBirth(), "date_of_birth": profile.getDateOfBirth(), "character": profile.getCharacter(), "image": profile.getImage(), "member_id": profile.getMemberId()}
    with open(PROFILESDATABASE, 'w') as new_user_data:
      json.dump(data, new_user_data, indent=4)

  def remove_profile(self, profile: Profile):
    self.procedures.remove(profile)
    with open(PROFILESDATABASE, "r") as f:
      data = json.load(f)
    del data[str(profile.getId())]
    with open(PROFILESDATABASE, 'w') as new_user_data:
      json.dump(data, new_user_data, indent=4)