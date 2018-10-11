from character import Character
from game.events.events import DialogMessage
from skills.fireball import Fireball
import random

class Mage(Character):
    _hp = 85
    _mp = 10
    _attack = 8

    def __init__(self):
        super().__init__()
        self._cls = 'Mage'
        self._es = self.get_es()
        self.add_skill(Fireball(self))
        self._passives['Energy Shield'] = "This passive allows Mage to absorb some of incoming damage.\n" \
                                          "ES scales with MP and lvl"

#   ES getter and setter #

    def get_es(self):
        """
        Returns character's es
        """
        return self._mp * (self.get_lvl() / 2)

    def _set_es(self, es):
        """
        Takes new value for character's es and sets it
        Not really intended to use
        """
        self._es = es

#   Class specific methods modifications #

    def lvlup(self):
        """
        Gives character a lvlup bonus
        """
        super().lvlup()
        self._es = self.get_es()

    def take_damage_from(self, damage, other):
        """
        Takes other character's attack and reduces self es or/and hp by it
        Prints message about that attack
        """
        if self._es > 0 and damage < self._es:
            self._es -= damage
            return DialogMessage('attack_es_CAT', other, damage, self).get_message() + "\n"
        elif 0 < self._es <= damage:
            if self._es == damage:
                self._es = 0
                return DialogMessage('broke_es_C', self).get_message() + "\n"
            else:
                leftoverdmg = damage - self._es
                self._hp -= leftoverdmg * self.get_attack_modifier()
                self._es = 0
                return DialogMessage('broke_es_dmg_hp_CAT', other, leftoverdmg * self.get_attack_modifier(), self).get_message() + "\n"
        else:
            return super().take_damage_from(damage, other)

    def get_stats(self):
        """
        Prints character's stats
        """
        stats = super().get_stats()
        stats['ES'] = self._es
        return stats
