from character import Character
from game.events.events import DialogMessage
import random

class Rogue(Character):
    _crit_chance = 0.2
    _evade_chance = 0.2
    _attack = 15

    def __init__(self):
        super().__init__()
        self._cls = 'Rogue'
        self._evade_chance = self._evade_chance + 0.001 * self.get_mp()
        self._passives['Evasion'] = "This passive allows Rogue to evade some of incoming damage.\n" \
                                    "EV scales with MP"
        self._passives['Critical Strike'] = "This passive allows Rogue to double the damage some of his attacks.\n" \
                                            "Crit chance scales with MP"

#   Evasion getters and setters #

    def get_evasion(self):
        """
        Returns character's evade chance
        """
        return self._evade_chance + 0.001 * self.get_mp()

    def set_evasion(self, ev):
        """
        Sets character's evade chance
        """
        self._evade_chance = ev

    def get_dodge(self):
        """
        Returns evasion proc True or False
        """
        return random.random() < self.get_evasion()

#   Crit getters and setters #

    def get_crit_chance(self):
        """
        Returns character's evade chance
        """
        return self._crit_chance + 0.001 * self.get_mp()

    def set_crit_chance(self, chance):
        """
        Takes new value for character's evade chance and sets it
        """
        self._crit_chance = chance

    def get_crit(self):
        """
        Returns crit proc True or False
        """
        return random.random() < self.get_crit_chance()

#   Class specific methods modifications #

    def take_damage_from(self, damage, other):
        """
        Takes damage from other character
        Prints message about that attack
        """
        if self.get_dodge():
            return DialogMessage('evaded_CA', self, damage).get_message() + "\n"
        else:
            return super().take_damage_from(damage, other)

    def attack(self, other):
        """
        Reduces other character's hp by self's attack
        """
        if self.get_crit():
            attack = self.get_attack() * self.get_attack_modifier() * 2
            return DialogMessage('crit', self, attack).get_message() + "\n" + other.take_damage_from(attack, self)
        else:
            attack = self.get_attack() * self.get_attack_modifier()
            return other.take_damage_from(attack, self)

    def add_item(self, item):
        """
        Adds an item to character inventory
        """
        if item is None:
            pass
        else:
            if item.get_type() == 'Weapon':
                item.set_name('Dagger')
            super().add_item(item)

    def get_stats(self):
        """
        Returns character's stats in a dictionary
        """
        stats = super().get_stats()
        stats['EV_CHANCE'] = self.get_evasion()
        stats['CRIT_CHANCE'] = self.get_crit_chance()
        return stats
