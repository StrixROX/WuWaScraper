from os import path

from Scrapers.sonata import Sonatas
from Scrapers.item import Items
from Scrapers.enemy import Enemies
from Scrapers.echo import Echoes
from Scrapers.weaponType import WeaponTypes
from Scrapers.attribute import Attributes
from Scrapers.character import Characters

ICON_ROOT_PATH = str(path.abspath('./assets/'))
DATA_ROOT_PATH = str(path.abspath('./data/'))

sonatas = Sonatas.fetch(icons=True, iconRootPath=ICON_ROOT_PATH)
items = Items.fetch(icons=True, iconRootPath=ICON_ROOT_PATH)
enemies = Enemies.fetch(icons=True, iconRootPath=ICON_ROOT_PATH)
echoes = Echoes.fetch(icons=True, iconRootPath=ICON_ROOT_PATH) # all echo icons are same as enemy icons
weaponTypes = WeaponTypes.fetch(icons=True, iconRootPath=ICON_ROOT_PATH)
attributes = Attributes.fetch(icons=True, iconRootPath=ICON_ROOT_PATH)
characters = Characters.fetch(cards=True, icons=False, iconRootPath=ICON_ROOT_PATH, dataRootPath=DATA_ROOT_PATH)
