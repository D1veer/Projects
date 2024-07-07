from tinydb import TinyDB, Query
from ...config import *

db = TinyDB(BANKDATABASE, sort_keys=True, indent=2, separators=(',', ': '))

class Account(object):
  def __init__(self, id: str, money: int, freeze: bool) -> None:
    self.id = id
    self.money = money
    self.freeze = freeze

  def getId(self) -> str:
    return self.id

  def getMoney(self) -> int:
    return self.money

  def addMoney(self, amount: int) -> bool:
    if self.freeze:
      return [False, 'FREEZE']
    self.money += amount
    return True

  def delMoney(self, amount: int) -> bool:
    if self.freeze:
      return [False, 'FREEZE']
    self.money -= amount
    return True

  def setMoney(self, amount: int) -> bool:
    if self.freeze:
      return [False, 'FREEZE']
    self.money = amount
    return True

  def setFreeze(self, value: bool) -> bool:
    if value == True:
      self.freeze = True
      return True
    elif value == False:
      self.freeze = False
      return True

class Bank():
  def __init__(self) -> None:
    self.accounts: list = []
    data = db.all()
    for i in data:
      self.accounts.append(Account(**i))

  def getAccountById(self, id: str) -> Account:
    for i in self.accounts:
      if i.getId() == id:
        return i

  def addAccount(self, account: Account):
    self.accounts.append(account)
    db.insert(account.__dict__)

  def removeAccount(self, account: Account):
    self.accounts.remove(account)
    AccountToDelete = Query()
    db.remove(AccountToDelete.id == account.getId())

  def update(self, account: Account):
    self.accounts.remove(account)
    db.update(account.__dict__, Query().id == account.getId())
    newAcc = db.get(Query().id == account.getId())
    self.accounts.append(Account(**newAcc))



bank = Bank()