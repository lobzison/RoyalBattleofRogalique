from classes import *
from events import PrintMessage
import random


class Game:
    @staticmethod
    def game_start():
        """
        Character selection string
        Returns playerchar
        """
        PrintMessage('start_game')
        global playerchar
        global playerstatus
        playerchar = eval("{}()".format(input()))
        PrintMessage('stats')
        playerchar.print_stats()
        Game.adventure(playerchar)

    @staticmethod
    def battle_encounter(attacker, defender):
        """
        Takes attacker's and defender's characters and battles them until one of them is dead
        attacker is attacking first
        returns the winner
        """
        while attacker.is_alive() and defender.is_alive():
            attacker.deal_damage(defender)
            if not defender.is_alive():
                PrintMessage('won_C', attacker)
                break
            defender.deal_damage(attacker)
            if not attacker.is_alive():
                PrintMessage('won_C', defender)
                break
        if not playerchar.is_alive():
            PrintMessage('dead')
            PrintMessage('end_game')
        else:
            if random.randint(1, 6) % 3 == 0:
                item = 'Healing Potion'
                print(f"You found a {item}!")
                # PrintMessage('found_item_I', item)
                item_healing = random.randint(10, 30)
                PrintMessage('healed_CA', playerchar, item_healing)
                playerchar.set_hp(round(playerchar.get_hp() + item_healing))
            if random.randint(1, 6) > 4:
                item = CommonItem()
                PrintMessage('found_item_I', item)
                item.print_stats()
                if playerchar.get_inventory()[item.get_type()]:
                    print("Your Item:")
                    playerchar.get_inventory()[item.get_type()].print_stats()
                print("Would you like to equip item? (Y/N)")
                if input() == 'Y':
                    playerchar.add_item(item)

    @staticmethod
    def adventure(playerchar):
        """
        Starts adventure part of game with character 'playerchar'
        Breaks on death or N input
        """
        while playerchar.is_alive():
            playerchar.print_exp_lvl()
            PrintMessage('find_enemy')
            player_input = input()
            if player_input == 'I':
                playerchar.print_inventory()
                Game.adventure(playerchar)
            elif player_input == 'N':
                PrintMessage('end_game')
                break
            else:
                enemy = Monster(playerchar.get_lvl())
                if random.random() > 0.5:
                    PrintMessage('see_enemy_C', enemy)
                    enemy.print_stats()
                    PrintMessage('attack_enemy')
                    if input() == 'Y':
                        Game.battle_encounter(playerchar, enemy)
                    else:
                        Game.adventure(playerchar)

                else:
                    PrintMessage('enemy_attack_C', enemy)
                    enemy.print_stats()
                    Game.battle_encounter(enemy, playerchar)
                if not playerchar.is_alive():
                    break
            playerchar.add_exp(enemy.get_maxhp())
            PrintMessage('stats')
            playerchar.print_stats()

# test = Mage()
# test.get_inventory()['Ring'].print_stats()

Game.game_start()

# TODO skills: Mage Fireball
# TODO skills: Rogue Confusion
# TODO enemies: Boss Enemy
# TODO items: Rare Items
# TODO game: save state
# TODO game: console choice
# TODO mp: whatever the fuck i can do