from .utils import Entity, get, hash, downloadIcon
from urllib.parse import urljoin
from os import path
from time import time

class Item(Entity):
  def __init__(self, name, iconSrc, sources):
    super().__init__()

    self.setData("id", hash("item", name))
    self.setData("name", name)
    self.setData("iconSrc", iconSrc)
    self.setData("iconPath", f"item/{name}.png")
    self.setData("sources", sources)

  def __repr__(self):
    return f"Item: {self.getData("name")}"

class Items:
  __SOURCE = "https://encore.moe/en/item" # for item details
  __SOURCE_DOMAIN = "https://encore.moe"
  __SOURCE_2 = "https://wuthering.wiki/" # for items sources
  __DATA = None

  @classmethod
  def fetch(self, icons:bool, iconRootPath:str):
    if self.__DATA is not None:
      print("Reusing fetched item data...")
      print("Done.")
      return self.__DATA

    print("Fetching Item data...")
    start = time()



    page = get(self.__SOURCE)

    items = []

    sections = page.find_all(class_="item-type-group")
    sectionsToRead = [
      "Resonator Ascension Material",
      "Skill Upgrade Material",
      "Weapon and Skill Material",
      "Weapon and Skill Material",
      "Ascension Material"
    ]
    sectionsRead = []
    for _section in sections:
      _title = _section.find("p").text.strip()
      
      if _title not in sectionsToRead:
        continue

      sectionsRead.append(_title)
      
      for _item in _section.find_all("a"):
        commonId = _item['href'].split('/')[-1]
        iconSrc = urljoin(self.__SOURCE_DOMAIN, _item.find_all("img")[1]['src'])
        name = _item.find("p").text.strip()

        detailsPage = get(urljoin(self.__SOURCE_2, f"item_{commonId}.html"))

        def resolveItemSource(source):
          if _title == "Skill Upgrade Material" and "drop" in detailsPage.find(class_="description").text.strip().lower():
            source = "Drop: " + source.strip().strip("Drop: ")

          return source.strip()
        
        sources = [resolveItemSource(x.text) for x in detailsPage.find(class_="sources-grid").find_all(class_="sources-entry")]
        
        item = Item(name, iconSrc, sources)

        if icons:
          print(f"\t Downloading Icon: {name}", end="")
          downloadIcon(iconSrc, path.join(iconRootPath, item.getData("iconPath")))
          print("✔️")

        items.append(item)
    


    if len(sectionsToRead) != len(sectionsRead):
      unreadSections = [f"[Section] {x}" for x in sectionsToRead if x not in sectionsRead]
      print(sectionsRead)
      raise Exception(f"Resource not found -> {unreadSections}")



    end = time()
    self.__DATA = items

    print(f"Done. {round(end-start, 2)}s")
    return self.__DATA

if __name__ == "__main__":
  exit()
