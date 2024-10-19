from .utils import Entity, get, hash, downloadIcon
from os import path
from time import time
from urllib.parse import urljoin

class Enemy(Entity):
  def __init__(self, name, iconSrc, isWeeklyBoss):
    super().__init__()

    self.setData("id", hash("enemy", name))
    self.setData("name", name)
    self.setData("iconSrc", iconSrc)
    self.setData("iconPath", f"enemy/{name}.png")
    self.setData("isWeeklyBoss", isWeeklyBoss)

  def __repr__(self):
    return f"Enemy: {self.getData("name")}"
  
  def __eq__(self, val):
    if type(val) == str:
      return val == self.getData("name")
    elif type(val) == Enemy:
      return val.getData("id") == self.getData("id")
    else:
      return False

class Enemies:
  __SOURCE = "https://wuthering.wiki/monsters.html" # for enemy list
  __SOURCE_DOMAIN = "https://wuthering.wiki"
  __SOURCE2 = "https://game8.co/games/Wuthering-Waves/archives/453471" # for weekly boss list
  __DATA = None
  __NAME_CORRECTIONS_BY_NAME = {
    "Jué": "Sentinel Jué"
  }

  @classmethod
  def fetch(self, icons:bool, iconRootPath:str):
    if self.__DATA is not None:
      print("Reusing fetched enemy data...")
      print("Done.")
      return self.__DATA

    print("Fetching Enemy data...")
    start = time()



    page = get(self.__SOURCE)
    page2 = get(self.__SOURCE2)

    # get list of weekly bosses
    weeklyBosses = []
    weeklyBossTable = None
    for _table in page2.find_all("table"):
      # get table title
      _siblings = _table.previous_siblings
      _title = next(_siblings)
      while _title.name != "h2":
        try:
          _title = next(_siblings)
        except StopIteration:
          break

      # check if table title is correct
      try:
        if _title.text.strip() == "List of Weekly Challenge Bosses":
          weeklyBossTable = _table
          break
      except:
        continue
    
    if weeklyBossTable is None:
      raise Exception("Resource not found -> [Table] List of Weekly Challenge Bosses")



    for row in weeklyBossTable.findAll("tr")[1:]:
      name = row.find("td").text.strip()
      if name in self.__NAME_CORRECTIONS_BY_NAME:
        name = self.__NAME_CORRECTIONS_BY_NAME[name]
      weeklyBosses.append(name)


    enemies = []

    entries = page.find_all(class_="itementry")
    for entry in entries:
      name = entry.find(class_="navtext").text.strip()
      if name in self.__NAME_CORRECTIONS_BY_NAME.keys():
        name = self.__NAME_CORRECTIONS_BY_NAME[name]
      if name == "" or "Phantom" in name or name in enemies:
        continue

      iconSrc = urljoin(self.__SOURCE_DOMAIN, entry.find("img", class_="navicon-small")['src'])
      isWeeklyBoss = bool(name in weeklyBosses)

      enemy = Enemy(name, iconSrc, isWeeklyBoss)

      if icons:
        print(f"\t Downloading Icon: {name}", end="")
        downloadIcon(iconSrc, path.join(iconRootPath, enemy.getData("iconPath")))
        print("✔️")

      enemies.append(enemy)



    self.__DATA = enemies
    end = time()

    print(f"Done. {round(end-start, 2)}s")
    return self.__DATA

if __name__ == "__main__":
  exit()
