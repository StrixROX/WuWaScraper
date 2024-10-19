from .utils import Entity, get, hash, downloadIcon
import re
from os import path
from time import time

class Sonata(Entity):
  def __init__(self, name, iconSrc, _2pcEffect, _5pcEffect):
    super().__init__()

    self.setData("id", hash("sonata", name))
    self.setData("name", name)
    self.setData("iconSrc", iconSrc)
    self.setData("iconPath", f"sonata/{name}.png")
    self.setData("effects", [
      {
        "type": "2-Piece Effect",
        "desc": _2pcEffect
      },
      {
        "type": "5-Piece Effect",
        "desc": _5pcEffect
      }
    ])

  def __repr__(self):
    return f"Sonata: {self.getData("name")}"

class Sonatas:
  __SOURCE = "https://wutheringwaves.fandom.com/wiki/Sonata"
  __DATA = None

  @classmethod
  def fetch(self, icons:bool, iconRootPath:str):
    if self.__DATA is not None:
      print("Reusing fetched sonata data...")
      print("Done.")
      return self.__DATA

    print("Fetching Sonata data...")
    start = time()



    page = get(self.__SOURCE)

    sonataTable = None
    for _table in page.find_all("table"):
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
        if _title.find(class_="mw-headline").text.strip() == "List of Sonata":
          sonataTable = _table
          break
      except:
        continue
    
    if sonataTable is None:
      raise Exception("Resource not found -> [Table] List of Sonata")



    sonataEffects = []
    for row in sonataTable.find_all("tr")[1:]: # first row is header row
      cells = row.find_all("td")
      
      iconSrc = re.sub(
        r'/scale-to-width-down/[0-9]+',
        "",
        cells[0].find("img").get('data-src') or cells[0].find("img").get('src')
      )
      name = cells[0].text.strip()
      twopc = cells[1].text.strip()
      fivepc = cells[2].text.strip()

      sonata = Sonata(name, iconSrc, twopc, fivepc)

      if icons:
        print(f"\t Downloading Icon: {name}", end="")
        downloadIcon(iconSrc, path.join(iconRootPath, sonata.getData("iconPath")))
        print("✔️")

      sonataEffects.append(sonata)



    self.__DATA = sonataEffects
    end = time()

    print(f"Done. {round(end-start, 2)}s")
    return self.__DATA

if __name__ == "__main__":
  exit()
