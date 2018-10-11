from skill import Skill

class Fireball(Skill):
    def __init__(self, character):
        super().__init__(character)
        self._cooldown = 5
        self._current_cd = 0

    def get_damage(self):
        """
        Returns spell's damage
        """
        return self._owner.get_mp() * 1.5