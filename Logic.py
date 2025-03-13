
# Logic.py

import random

class Pokemon:
    def __init__(self, name, hp, moves, image_path):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.moves = moves
        self.image_path = image_path
        self.can_enemy_attack = True  # Flag to control enemy attacks

    def take_damage(self, damage):
        self.hp = max(0, self.hp - damage)

class BattleLogic:
    def __init__(self, player_pokemon, enemy_pokemon):
        self.player_pokemon = player_pokemon
        self.enemy_pokemon = enemy_pokemon

    def calculate_damage(self, attacker, defender, move):
        return attacker.moves.get(move, 0)  # Return move damage, default to 0 if move not found


    def attack(self, move):
        damage = self.player_pokemon.moves[move]
        self.enemy_pokemon.take_damage(damage)
        return f"{self.player_pokemon.name} used {move}!\n{self.enemy_pokemon.name} HP: {self.enemy_pokemon.hp}"
    
    def enemy_attack(self, move):
        damage = self.calculate_damage(self.enemy_pokemon, self.player_pokemon, move)
        self.player_pokemon.hp = max(0, self.player_pokemon.hp - damage)
        return f"{self.enemy_pokemon.name} used {move} and dealt {damage} damage!"

    def switch_pokemon(self, pikachu, greninja):
        if self.player_pokemon == pikachu:
            self.player_pokemon = greninja  # Switch Pikachu to Greninja
            
        else:
            self.player_pokemon = pikachu  # Switch back to Pikachu
        return f"Go! {self.player_pokemon.name}!"