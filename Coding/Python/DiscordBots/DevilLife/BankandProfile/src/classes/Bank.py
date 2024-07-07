from .. import config
from tinydb import TinyDB, Query
from dataclasses import dataclass

Account_Database: TinyDB = TinyDB(config.ACCOUNTS_DATABASE, indent=2, separators=(',', ': '))

@dataclass()
class Account(object):
  id: str
  money: int = 0
  cash: int = 0
  freeze: bool = False

  def addMoney(self, amount: int) -> bool:
    if self.freeze:
      return False
    self.money += amount
    return True

  def delMoney(self, amount: int) -> bool:
    if self.freeze:
      return False
    self.money -= amount
    return True

  def setMoney(self, amount: int) -> bool:
    if self.freeze:
      return False
    self.money = amount
    return True

  def addCash(self, amount: int) -> bool:
    if self.freeze:
      return False
    self.cash += amount
    return True

  def delCash(self, amount: int) -> bool:
    self.cash -= amount
    return True

  def setCash(self, amount: int) -> bool:
    if self.freeze:
      return False
    self.cash = amount
    return True

  def getFreeze(self) -> bool:
    return self.freeze

  def setFreeze(self, stuts) -> bool:
    self.freeze = stuts


class Bank():
  def __init__(self) -> None:
    self.accounts: list = []
    data = Account_Database.all()
    for i in data:
      self.accounts.append(Account(**i))

  def getAccountById(self, id: int) -> Account:
    for i in self.accounts:
      if i.getId() == id:
        return i

  def add_account(self, account: Account) -> Account:
    self.accounts.append(account)
    Account_Database.insert(account.__dict__)
    return account

  def remove_account(self, account: Account) -> bool:
    self.accounts.remove(account)
    profileToDelete: Query = Query()
    Account_Database.remove(profileToDelete.id == account.getId())
    return True

  def update(self, account: Account) -> bool:
    self.accounts.remove(account)
    up = Account_Database.update(account.__dict__, Query().id == account.getId())
    newAcc = Account_Database.get(Query().id == account.getId())
    self.accounts.append(Account(**newAcc))
    return True

BANK: Bank = Bank()