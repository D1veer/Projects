import json
from typing_extensions import Self
from unittest import mock
from Project.assets.Classes.Profile import ProfilesManager, Profile

profilesManager = ProfilesManager()

class Account():
  def __init__(self, profile: Profile, money: int) -> None:
    self.profile = profile
    print(profile)
    self.id = profile.getId()
    self.money = money

  def getProfile(self) -> str:
    return self.profile

  def getId(self) -> int:
    return self.id

  def getMoney(self) -> int:
    return self.money

  def addMoney(self, amount: int) -> bool:
    self.money += amount
    return True

  def delMoney(self, amount: int) -> bool:
    self.money -= amount
    return True

  def setMoney(self, amount: int) -> bool:
    self.money = amount
    return True

class Bank():
  def __init__(self) -> None:
    self.accounts: list = []
    with open(ACCOUNTSDATABASE, "r") as f:
      data = json.load(f)
    for i in data:
      self.accounts.append(Account(profilesManager.getProfileById(data[i]['id']), data[i]['money']))


  def getAccountById(self, id: int) -> Account:
    for i in self.accounts:
      if i.getProfile().getId() == id:
        return i

  def add_account(self, account: Account):
    self.accounts.append(account)
    with open(ACCOUNTSDATABASE, "r") as f:
      data = json.load(f)
    data[str(account.getId())] = {"money": account.getMoney(), "id": account.getId()}
    with open(ACCOUNTSDATABASE, 'w') as new_user_data:
      json.dump(data, new_user_data, indent=4)

  def remove_account(self, account: Account):
    self.accounts.remove(account)
    with open(ACCOUNTSDATABASE, "r") as f:
      data = json.load(f)
    del data[str(account.getId())]
    with open(ACCOUNTSDATABASE, 'w') as new_user_data:
      json.dump(data, new_user_data, indent=4)

  def update(self, account: Account):
    self.accounts.remove(account)
    with open(ACCOUNTSDATABASE, "r") as f:
      data = json.load(f)
    del data[str(account.getId())]
    data[str(account.getId())] = {"money": account.getMoney(), "id": account.getId()}
    with open(ACCOUNTSDATABASE, 'w') as new_user_data:
      json.dump(data, new_user_data, indent=4)
    self.accounts.append(account)