from .utils import Entity, get, hash, downloadIcon
import re
from os import path
from urllib.parse import urljoin
from time import time

class Attribute(Entity):
  def __init__(self, name, iconSrc):
    super().__init__()

    self.setData("id", hash("attribute", name))
    self.setData("name", name)
    self.setData("iconSrc", iconSrc)
    self.setData("iconPath", f"attribute/{name}.png")

  def __repr__(self):
    return f"Attribute: {self.getData("name")}"

class Attributes:
  __SOURCE = "https://wuthering.wiki/index.html"
  __SOURCE_DOMAIN = "https://wuthering.wiki"
  __DATA = None

  __ATTRIBUTE_ID_TO_TYPE_MAP = {
    "1": "Glacio",
    "2": "Fusion",
    "3": "Electro",
    "4": "Aero",
    "5": "Spectro",
    "6": "Havoc"
  }

  @classmethod
  def fetch(self, icons:bool, iconRootPath:str):
    if self.__DATA is not None:
      print("Reusing fetched attribute data...")
      print("Done.")
      return self.__DATA

    print("Fetching Attribute data...")
    start = time()



    page = get(self.__SOURCE)

    attributes = []

    for i in page.find(id="filter-elements").findAll("img"):
      attributeId = re.search("[0-9].png$", i['src']).group()[:-4]
      name = self.__ATTRIBUTE_ID_TO_TYPE_MAP[attributeId]
      iconSrc = urljoin(self.__SOURCE_DOMAIN, i["src"])

      attribute = Attribute(name, iconSrc)

      if icons:
        print(f"\t Downloading Icon: {name}", end="")
        downloadIcon(iconSrc, path.join(iconRootPath, attribute.getData("iconPath")))
        print("✔️")

      attributes.append(attribute)



    self.__DATA = attributes
    end = time()

    print(f"Done. {round(end-start, 2)}s")
    return self.__DATA

if __name__ == "__main__":
  exit()
