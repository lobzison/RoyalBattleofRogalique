import random, math
from game.events.events import *

class Character:
    _maxhp = 100
    _mp = 0
    _attack = 10
    _exp = 0
    _lvl = 1
    _gold = 0
    _character = True
    _hp_item_bonus = 0
    _mp_item_bonus = 0
    _attack_item_bonus = 0
    _armour_item_bonus = 0

    def __init__(self):
        self._cls = 'Character'
        self._armour = 0
        self._inventory = {'Armour': None, 'Weapon': None, 'Helm': None, 'Boots': None, 'Ring': None}
        self._skills = []
        self._passives = {}
        self.recalculate_item_bonus()
        self._hp = self._maxhp = self.get_maxhp()

#   Class getters and setters #

    def get_class(self):
        """
        Returns character's class
        """
        return self._cls

    def set_class(self, cls):
        """
        Takes new value for character's class and sets it
        """
        self._cls = cls

    def get_character(self):
        """
        Check if it is a character
        """
        return self._character

#   HP getters and setters #

    def get_current_hp(self):
        """
        Returns character's hp
        """
        return self._hp

    def get_maxhp(self):
        """
        Returns character's maxhp
        """
        return self._maxhp + self.get_hp_modifier()

    def set_hp(self, hp):
        """
        Takes new value for character's hp and sets it
        """
        if hp <= self.get_maxhp():
            self._hp = hp
        else:
            self._hp = self.get_maxhp()

    def get_hp_modifier(self):
        """
        Returns character's hp modifier
        """
        return self._hp_item_bonus

    def set_hp_item_bonus(self, hp_bonus):
        """
        Sets character's hp modifier
        """
        self._hp_item_bonus = hp_bonus
        # if charater have max hp and unequips item with bonus hp,
        # current hp is recalclated
        if self.get_current_hp() > self.get_maxhp():
            self.set_hp(self.get_maxhp())

#   MP getters and setters #

    def get_mp(self):
        """
        Returns character's mp
        """
        return self._mp + self._mp_item_bonus

    def set_mp(self, mp):
        """
        Takes new value for character's mp and sets it
        """
        self._mp = mp

#   Gold getters and setters #

    def get_gold(self):
        """
        Returns character's mp
        """
        return self._gold

    def set_gold(self, gold):
        """
        Takes new value for character's mp and sets it
        """
        self._gold = gold

#   Attack getters and setters #

    def get_attack_stat(self):
        """
        Returns character's attack stat
        """
        return self._attack + self._attack_item_bonus

    def get_attack(self):
        """
        Returns character's attack (+-10%)
        """
        return random.uniform((self._attack + self._attack_item_bonus) * 0.9, (self._attack + self._attack_item_bonus) * 1.1)

    def set_attack(self, attack):
        """
        Takes new value for character's attack and sets it
        """
        self._attack = attack

    def get_attack_modifier(self):
        """
        Returns character's attack modifier
        Default modifier is 1 and used for player classes
        """
        return 1

#   Defence getters and setters #

    def get_armour(self):
        """
        Returns character's armour
        """
        return self._armour + self._armour_item_bonus

    def set_armour(self, armour):
        """
        Takes new value for character's armour and sets it
        """
        self._armour = armour

    def get_defence_modifier(self):
        """
        Returns character's defence modifier
        """
        return 1 - (math.log10(self.get_armour() + 1) / 3)

#   EXP getters and setters #

    def get_exp(self):
        """
        Returns character's exp
        """
        return self._exp

    def _set_exp(self, exp):
        """
        Takes new value for character's exp and sets it
        Not really intended to use
        Not until I fix problems with lvlup
        """
        self._exp = exp

    def get_exp_to_next_lvl(self):
        """
        Returns character's exp to the next lvl
        """
        return 100 * math.sqrt(self._lvl)

#   LVL getters and setters #

    def get_lvl(self):
        """
        Returns character's lvl
        """
        return self._lvl

    def set_lvl(self, lvl):
        """
        Sets character's lvl
        """
        self._lvl = lvl

#   Adding EXP and lvlup #

    def add_exp(self, exp):
        """
        Adds an amount of exp to character
        """
        self._exp += exp
        if self._exp >= self.get_exp_to_next_lvl():
            self._lvl += 1
            lvlup = DialogMessage('lvlup_CA', self, self.get_lvl()).get_message()
            self.lvlup()
            lvlup += StatusMessage(self).stats_message()
            return lvlup

    def lvlup(self):
        """
        Gives character a lvlup bonus
        """
        self._maxhp += 10
        self._hp = self.get_maxhp()
        self._mp += 1
        self._attack += 1
        self._exp = 0

#   Items and inventory #

    def add_item(self, item):
        """
        Adds an item to character inventory
        """
        if item is None:
            pass
        else:
            self._inventory[item.get_type()] = item
            self.recalculate_item_bonus()

    def get_inventory(self):
        """
        Returns character's inventory
        """
        return self._inventory

    def recalculate_item_bonus(self):
        """
        Recalculates all item bonuses
        """
        self._hp_item_bonus = 0
        self._mp_item_bonus = 0
        self._attack_item_bonus = 0
        self._armour_item_bonus = 0
        for i in range(0, len(self._inventory)):
            slot = list(self._inventory)[i]
            item = self._inventory[slot]
            if item is not None:
                self.set_hp_item_bonus(self.get_hp_modifier() + item.get_bonus_hp())
                self._mp_item_bonus += item.get_bonus_mp()
                self._attack_item_bonus += item.get_bonus_attack()
                self._armour_item_bonus += item.get_bonus_defence()

#   Skills #

    def get_skills(self):
        """
        Returns character's skills
        """
        return self._skills

    def add_skill(self, skill):
        """
        Adds skill to character
        """
        self._skills.append(skill)

    def is_skill_available(self):
        """
        Returns if any of skills are available
        """
        for skill in self.get_skills():
            if skill.get_current_cd() == 0:
                return True
        return False

    def first_available_skill(self):
        """
        Cycles through character's skills and returns first spell that is ready to be used
        Skills are in order of first added
        """
        for skill in self.get_skills():
            if skill.get_current_cd() == 0:
                return skill

    def use_attack_skill(self, skill, other):
        damage = skill.get_damage()
        return DialogMessage('used_skill_C', self).get_message() + "\n" + other.take_damage_pure(damage, self)

    def get_passives(self):
        """
        Returns character's passives (only names and descriptions)
        """
        return self._passives

#   is_alive check #

    def is_alive(self):
        """
        Returns True if character is alive and False if not
        """
        return self._hp > 0

#   Attacking and taking damage #

    def take_damage_from(self, damage, other):
        """
        Takes damage from other character
        Prints message about that attack
        """
        self._hp -= damage * self.get_defence_modifier()
        return DialogMessage('attack_CAT', other, damage * self.get_defence_modifier(), self).get_message()  + "\n"

    def take_damage_pure(self, damage, other):
        """
        Takes pure damage from skills
        """
        self._hp -= damage
        return DialogMessage('attack_pure_CAT', other, damage, self).get_message() + "\n"

    def attack(self, other):
        """
        Reduces other character's hp by self's attack
        """
        attack = self.get_attack() * self.get_attack_modifier()
        return other.take_damage_from(attack, self)

#   Getting character's stats #

    def get_stats(self):
        """
        Returns character's stats in a dictionary
        """
        stats = dict(CLS=self.get_class(),
                     HP=self.get_current_hp(),
                     MAX_HP=self.get_maxhp(),
                     MP=self.get_mp(),
                     ATT=round(self.get_attack_stat(), 2),
                     ATT_BONUS=round(self._attack_item_bonus, 2),
                     DEF=round(1 - self.get_defence_modifier(), 2),
                     LVL=self.get_lvl(),
                     EXP=round(self.get_exp(), 2),
                     EXPLVL=round(self.get_exp_to_next_lvl(), 2),
                     GOLD=self.get_gold(),
                     INV=self.get_inventory(),
                     SKILLS=self.get_skills(),
                     PASSIVES=self.get_passives())
        return stats

#   testing used stuff #

    def _print_stats(self):
        """
        Prints character's stats
        """
        print(self.get_stats())

    def _get_all_items(self):
        """
        Prints character's inventory
        """
        itemlist = "Slot | Equipped Item\n" \
                   "=========================\n"

        have_items = False
        for item in self.get_inventory():
            if self.get_inventory()[item] is not None:
                itemlist += f"{item} | {self.get_inventory()[item].get_full_name()}\n"
                have_items = True
        # while have_items:
        #     print("Show item stats? (N/Slot)")
        #     slot = input()
        #     if slot in list(self._inventory):
        #         item = self._inventory[slot]
        #         item._print_stats()
        #     else:
        #         break
        if not have_items:
            itemlist += "Your inventory is empty."
        return itemlist