from .utils import Entity, get, hash, downloadIcon
from os import path
from time import time
from urllib.parse import urljoin
from .sonata import Sonatas

class Echo(Entity):
  def __init__(self, name, iconSrc, cost, sonatas):
    super().__init__()

    self.setData("id", hash("echo", name))
    self.setData("name", name)
    self.setData("iconSrc", iconSrc)
    self.setData("iconPath", f"enemy/{name}.png") # all echo icons are same as enemy icons
    self.setData("cost", cost)
    self.setData("sonatas", sonatas)

  def __repr__(self):
    return f"Echo: {self.getData("name")}"

  def __eq__(self, val):
    if type(val) == str:
      return val == self.getData("name")
    elif type(val) == Echo:
      return val.getData("id") == self.getData("id")
    else:
      return False

class Echoes:
  __SOURCE = "https://wuthering.gg/echos"
  __SOURCE_DOMAIN = "https://wuthering.gg"
  __DATA = None
  __NAME_CORRECTIONS_BY_NAME = {
    "Jué": "Sentinel Jué",
    "JuÃ©": "Sentinel Jué"
  }

  @classmethod
  def fetch(self, icons:bool, iconRootPath:str):
    if self.__DATA is not None:
      print("Reusing fetched echo data...")
      print("Done.")
      return self.__DATA

    print("Fetching Echo data...")
    start = time()


    
    sonatas = Sonatas.fetch(icons=False, iconRootPath=iconRootPath)
    sonataRef = {x.getData("name"): x for x in sonatas}
    page = get(self.__SOURCE)



    echoes = []

    entries = page.find(class_="list").find_all(class_="item")
    for entry in entries:
      name = entry.find(class_="name").text.strip()
      if name in self.__NAME_CORRECTIONS_BY_NAME.keys():
        name = self.__NAME_CORRECTIONS_BY_NAME[name]
      if name == "" or "Phantom" in name or name in echoes:
        continue

      iconSrc = urljoin(self.__SOURCE_DOMAIN, entry.find(class_="image").find("img")['srcset'].split(' ')[0])
      cost = entry.find(class_="cost").text.strip()
      sonatas = [sonataRef[x['alt']] for x in entry.find(class_="fetters").findAll("img")]

      echo = Echo(name, iconSrc, cost, sonatas)

      if icons:
        # if enemy icon already exists, i don't want to overwrite it with echo icon
        # enemy icon is higher quality
        if not path.exists(path.join(iconRootPath, echo.getData("iconPath"))):
          print(f"\t Downloading Icon: {name}", end="")
          downloadIcon(iconSrc, path.join(iconRootPath, echo.getData("iconPath")))
          print("✔️")
        else:
          print(f"\t Enemy Icon Already Downloaded: {name}✔️")

      echoes.append(echo)



    self.__DATA = echoes
    end = time()

    print(f"Done. {round(end-start, 2)}s")
    return self.__DATA

if __name__ == "__main__":
  exit()
