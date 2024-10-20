from os import path
import json

from Scrapers.sonata import Sonatas
from Scrapers.item import Items
from Scrapers.enemy import Enemies
from Scrapers.echo import Echoes
from Scrapers.weaponType import WeaponTypes
from Scrapers.attribute import Attributes
from Scrapers.character import Characters

ICON_ROOT_PATH = str(path.abspath('./assets/'))
DATA_ROOT_PATH = str(path.abspath('./data/'))
OUTPUT_ROOT_PATH = str(path.abspath('./output/'))

DOWNLOAD_IMAGES = False

sonatas = Sonatas.fetch(icons=DOWNLOAD_IMAGES, iconRootPath=ICON_ROOT_PATH)
items = Items.fetch(icons=DOWNLOAD_IMAGES, iconRootPath=ICON_ROOT_PATH)
enemies = Enemies.fetch(icons=DOWNLOAD_IMAGES, iconRootPath=ICON_ROOT_PATH)
echoes = Echoes.fetch(icons=DOWNLOAD_IMAGES, iconRootPath=ICON_ROOT_PATH) # all echo icons are same as enemy icons
weaponTypes = WeaponTypes.fetch(icons=DOWNLOAD_IMAGES, iconRootPath=ICON_ROOT_PATH)
attributes = Attributes.fetch(icons=DOWNLOAD_IMAGES, iconRootPath=ICON_ROOT_PATH)
characters = Characters.fetch(cards=DOWNLOAD_IMAGES, icons=DOWNLOAD_IMAGES, iconRootPath=ICON_ROOT_PATH, dataRootPath=DATA_ROOT_PATH)

outputFilePaths = {
  "sonatas.json": [x.export() for x in sonatas],
  "items.json": [x.export() for x in items],
  "enemies.json": [x.export() for x in enemies],
  "echoes.json": [x.export() for x in echoes],
  "weaponTypes.json": [x.export() for x in weaponTypes],
  "attributes.json": [x.export() for x in attributes],
  "characters.json": [x.export() for x in characters]
}

for i in outputFilePaths:
  with open(path.join(OUTPUT_ROOT_PATH, i), "w") as f:
    f.write(json.dumps(outputFilePaths[i]))
