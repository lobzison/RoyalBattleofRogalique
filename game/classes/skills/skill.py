class Skill:
    def __init__(self, character):
        self._owner = character
        self._cooldown = 0
        self._current_cd = 0

    def get_owner(self):
        """
        Returns skill's owner
        """
        return self._owner

    def get_name(self):
        """
        Returns skill's name
        """
        return self.__class__.__name__

    def get_cooldown_timer(self):
        """
        Returns spells's cd timer
        """
        return self._cooldown

    def set_cooldown_timer(self, cd):
        """
        Sets spells's cd timer
        """
        self._cooldown = cd

    def get_current_cd(self):
        """
        Returns spell's current cd
        """
        return self._current_cd

    def set_current_cd(self, cd):
        """
        Set new amount for current cd
        More then max cd = max cd
        Less then 0 = 0
        """
        if cd < 0:
            self._current_cd = 0
        elif cd <= self._cooldown:
            self._current_cd = cd
        else:
            self._current_cd = self._cooldown

    def is_available(self):
        """
        Returns if spell is ready to use
        """
        return self._current_cd == 0