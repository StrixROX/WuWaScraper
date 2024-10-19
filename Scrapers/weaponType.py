from .utils import Entity, get, hash, downloadIcon
import re
from os import path
from urllib.parse import urljoin
from time import time

class WeaponType(Entity):
  def __init__(self, name, iconSrc):
    super().__init__()

    self.setData("id", hash("weaponType", name))
    self.setData("name", name)
    self.setData("iconSrc", iconSrc)
    self.setData("iconPath", f"weapon_type/{name}.png")

  def __repr__(self):
    return f"WeaponType: {self.getData("name")}"

class WeaponTypes:
  __SOURCE = "https://wuthering.wiki/weapons.html"
  __SOURCE_DOMAIN = "https://wuthering.wiki"
  __DATA = None

  __WEAPON_ID_TO_TYPE_MAP = {
    "1": "Broadblade",
    "2": "Sword",
    "3": "Pistols",
    "4": "Gauntlets",
    "5": "Rectifier"
  }

  @classmethod
  def fetch(self, icons:bool, iconRootPath:str):
    if self.__DATA is not None:
      print("Reusing fetched weapon type data...")
      print("Done.")
      return self.__DATA

    print("Fetching Weapon Type data...")
    start = time()



    page = get(self.__SOURCE)

    weaponTypes = []

    for i in page.find(id="filter-weapontype").findAll("img"):
      weaponId = re.search("[0-9].png$", i['src']).group()[:-4]
      name = self.__WEAPON_ID_TO_TYPE_MAP[weaponId]
      iconSrc = urljoin(self.__SOURCE_DOMAIN, i["src"])

      weaponType = WeaponType(name, iconSrc)

      if icons:
        print(f"\t Downloading Icon: {name}", end="")
        downloadIcon(iconSrc, path.join(iconRootPath, weaponType.getData("iconPath")))
        print("✔️")

      weaponTypes.append(weaponType)



    self.__DATA = weaponTypes
    end = time()

    print(f"Done. {round(end-start, 2)}s")
    return self.__DATA

if __name__ == "__main__":
  exit()
