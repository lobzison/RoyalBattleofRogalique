from character import Character
import math

class Warrior(Character):
    _hp = 100
    hp_mult = 1.1

    def __init__(self):
        super().__init__()
        self._cls = 'Warrior'
        self._maxhp = self._hp = self.get_maxhp()
        self._passives['Warrior Blood'] = "This passive adds Warrior additional defence for every missing HP.\n"
        self._passives['Great Health'] = "This passive adds additional defence for Warrior.\n"

#   HP modifier, but with passive #

    def get_hp_modifier(self):
        """
        Returns character's attack modifier
        """
        return self._hp_item_bonus

    def get_maxhp(self):
        """
        Returns character's maxhp
        """
        return (self._maxhp + self.get_hp_modifier()) * self.hp_mult

#   Armour passive getter #

    def get_passive_defence_bonus(self):
        """
        Returns warrior's passive defence bonus
        """
        return math.log10(self.get_maxhp() - self.get_current_hp() + 1) / 10

#   Class specific methods modifications #

    def get_defence_modifier(self):
        """
        Returns character's defence modifier
        """
        return 1 - (math.log10(self.get_armour() + 1) / 3) - self.get_passive_defence_bonus()

    def get_stats(self):
        """
        Returns character's stats in a dictionary
        """
        stats = super().get_stats()
        stats['DEF_BONUS'] = round(self.get_passive_defence_bonus(), 2)
        stats['HP_BONUS'] = self.hp_mult
        return stats
