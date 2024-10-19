from .utils import Entity, get, getPageTitle, hash, downloadIcon, downloadCard
from os import path
import re
from time import time
from urllib.parse import urljoin
from .attribute import Attributes
from .weaponType import WeaponTypes
from .item import Items

class Character(Entity):
  def __init__(self, name, iconSrc, cardSrc, attribute, weaponType, ascensions, skills):
    super().__init__()

    self.setData("id", hash("character", name))
    self.setData("name", name)
    self.setData("iconSrc", iconSrc)
    self.setData("iconPath", f"character_icon/{name}.png")
    self.setData("cardSrc", cardSrc)
    self.setData("cardPath", f"character_card/{name}.png")
    self.setData("attribute", attribute)
    self.setData("weaponType", weaponType)
    self.setData("ascensions", ascensions)
    self.setData("skills", skills)

  def __repr__(self):
    return f"Character: {self.getData("name")}"

  def __eq__(self, val):
    if type(val) == str:
      return val == self.getData("name")
    elif type(val) == Character:
      return val.getData("id") == self.getData("id")
    else:
      return False

class Characters:
  __SOURCE = "https://wuthering.wiki/index.html"
  __SOURCE_DOMAIN = "https://wuthering.wiki"
  __SOURCE_DOMAIN2 = "https://wutheringwaves.fandom.com/wiki/"
  __DATA = None

  __ASCENSION_COST_TYPE_TO_INDEX_MAP = {
    "N2": 1,
    "N3": 2,
    "N4": 3,
    "N5": 4,
    "A4": 5,
    "R3": 6
  }
  __SKILL_COST_TYPE_TO_INDEX_MAP = {
    "N2": 1,
    "N3": 2,
    "N4": 3,
    "N5": 4,
    "B4": 5,
    "F2": 6,
    "F3": 7,
    "F4": 8,
    "F5": 9,
  }

  def __asd():
    pass

  @classmethod
  def fetch(self, cards:bool, icons:bool, iconRootPath:str, dataRootPath:str):
    if self.__DATA is not None:
      print("Reusing fetched character data...")
      print("Done.")
      return self.__DATA

    print("Fetching Character data...")
    start = time()



    if not path.isfile(path.join(dataRootPath, "ascensionCostFormulae.dat")):
        raise Exception("Resource not found -> [File] Scrapers/ascensionCostFormulae.dat")
    
    if not path.isfile(path.join(dataRootPath, "skillCostFormulae.dat")):
        raise Exception("Resource not found -> [File] Scrapers/skillCostFormulae.dat")



    attributesRef = {x.getData("name"):x for x in Attributes.fetch(icons=False, iconRootPath=iconRootPath)}
    weaponTypesRef = {x.getData("name"):x for x in WeaponTypes.fetch(icons=False, iconRootPath=iconRootPath)}
    itemsRef = {x.getData("name"):x for x in Items.fetch(icons=False, iconRootPath=iconRootPath)}



    page = get(self.__SOURCE)

    characters = []

    for entry in page.find_all(class_="itementry"):
      charName = entry.find(class_="navtext").text.strip()
      if charName == "" or charName in characters:
        continue
      iconSrc = urljoin(self.__SOURCE_DOMAIN, entry.find("img", class_="navicon")['src'])

      detailsPage = get(urljoin(self.__SOURCE_DOMAIN, entry.find("a")['href']))
      details = detailsPage.findAll("td", class_="infovalue")

      detailsPage2 = get(urljoin(self.__SOURCE_DOMAIN2, charName.replace(' ', '_')))
      cardSrc = detailsPage2.find("figure", class_="pi-image").find("a")['href']

      attribute = attributesRef[details[1].text.strip()]
      weaponType = weaponTypesRef[details[2].text.strip()]

      levelUpMaterials = detailsPage.find("div", class_="basetable").findAll(class_="costsection")



      # ascension costs
      ascensions = []

      ascensionMaterials = levelUpMaterials[1].findAll(class_="costentry")

      def resolveAscensionCost(x:str):
        [itemType, amount] = x.split('_')
        itemIndex = self.__ASCENSION_COST_TYPE_TO_INDEX_MAP[itemType]
        itemName = getPageTitle(urljoin(self.__SOURCE_DOMAIN, ascensionMaterials[itemIndex].find("a")['href'])).split("(")[0].strip()
        item = itemsRef[itemName]
        return {
          "item": item,
          "amount": amount
        }

      with open(path.join(dataRootPath, "ascensionCostFormulae.dat"), "r") as f:
        lines = f.read().split('\n')
        for i in range(len(lines)):
          line = lines[i].strip()
          if line == "":
            continue

          ascensionLevel = str(i+1)
          minLevelNeeded = line.split(' ')[0]
          ascensionCost = list(map(resolveAscensionCost, line.split(' ')[1:]))
          
          ascensions.append({ "rank": ascensionLevel, "minLevel": minLevelNeeded, "cost": ascensionCost })

      

      # skill costs
      skills = []

      skillUpgradeMaterials = levelUpMaterials[0].findAll(class_="costentry")

      def resolveSkillUpgradeCost(x:str):
        [itemType, amount] = x.split('_')
        itemIndex = self.__SKILL_COST_TYPE_TO_INDEX_MAP[itemType]
        itemName = getPageTitle(urljoin(self.__SOURCE_DOMAIN, skillUpgradeMaterials[itemIndex].find("a")['href'])).split("(")[0].strip()
        item = itemsRef[itemName]
        return {
          "item": item,
          "amount": amount
        }

      with open(path.join(dataRootPath, "skillCostFormulae.dat"), "r") as f:
        skillTypeCosts = f.read().strip().split("\n\n")

        for section in skillTypeCosts:
          lines = section.strip().split("\n")

          type_ = lines[0][5]
          name = re.search('\".*\"$', lines[0]).group()[1:-1]
          costs = []
          for i in range(1, len(lines)):
            if "NA" in lines[i]:
              continue

            skillLevel = str(i)
            minAscension = lines[i].split(' ')[0]
            upgradeCost = list(map(resolveSkillUpgradeCost, lines[i].split(' ')[1:]))

            costs.append({ "level": skillLevel, "cost": upgradeCost, "minAscension": minAscension })
        
          skills.append({ "type": type_, "name": name, "upgrades": costs })



      character = Character(charName, iconSrc, cardSrc, attribute, weaponType, ascensions, skills)

      if icons:
        print(f"\t Downloading Icon: {charName}", end="")
        downloadIcon(iconSrc, path.join(iconRootPath, character.getData("iconPath")))
        print("✔️")

      if cards:
        if "Rover" not in charName or not path.isfile(path.join(iconRootPath, character.getData("cardPath"))):
          print(f"\t Downloading Card: {charName}", end="")
          downloadCard(cardSrc, path.join(iconRootPath, character.getData("cardPath")))
          print("✔️")

      characters.append(character)


    self.__DATA = characters
    end = time()

    print(f"Done. {round(end-start, 2)}s")
    return self.__DATA

if __name__ == "__main__":
  exit()
