from game.items.item import RareItem
from character import Character
import math, random

class Monster(Character):
    def __init__(self, lvl_mult=1):
        super().__init__()
        self._cls = 'Monster'
        self._lvl_mult = lvl_mult / math.sqrt(lvl_mult * 2)
        self._maxhp = (random.randint(21, 40) * self._lvl_mult)
        self._hp = self.get_maxhp()
        self._mp = (random.randint(1, 1) * self._lvl_mult)
        self._attack = (random.randint(1, 15) * self._lvl_mult)

class GreaterMonster(Monster):
    def __init__(self, lvl_mult=1):
        lvl_mult *= 2 * math.log10(lvl_mult)
        super().__init__(lvl_mult)
        self._cls = 'Greater Monster'
        self.add_item(RareItem(int(lvl_mult)))
        self.add_item(RareItem(int(lvl_mult)))
        self.add_item(RareItem(int(lvl_mult)))
        self._hp = self.get_maxhp()
        self._mp = self.get_mp()
