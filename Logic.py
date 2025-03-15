import random

class Pokemon:
    def __init__(self, name, hp, moves, image_path):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.moves = moves  # Dictionary: {move_name: damage}
        self.image_path = image_path
        self.can_enemy_attack = True  # Flag to control enemy attacks

    def take_damage(self, damage):
        self.hp = max(0, self.hp - damage)  # Prevents HP from going negative

class BattleLogic:
    def __init__(self, player_pokemon1, player_pokemon2, enemy_pokemon1, enemy_pokemon2):
        self.player_pokemon1 = player_pokemon1
        self.player_pokemon2 = player_pokemon2
        self.enemy_pokemon1 = enemy_pokemon1
        self.enemy_pokemon2 = enemy_pokemon2
        
        # Start with player_pokemon1 and enemy_pokemon1
        self.player_pokemon = self.player_pokemon1
        self.enemy_pokemon = self.enemy_pokemon1

    def calculate_damage(self, attacker, defender, move):
        return attacker.moves.get(move, 0)  # Return move damage, default to 0 if move not found

    def enemy_attack(self):
        if not self.enemy_pokemon.can_enemy_attack:
            return f"{self.enemy_pokemon.name} cannot attack this turn!"

        move = random.choice(list(self.enemy_pokemon.moves.keys()))  # Random AI move
        damage = self.calculate_damage(self.enemy_pokemon, self.player_pokemon, move)
        self.player_pokemon.take_damage(damage)

        # Display remaining HP
        return (f"{self.enemy_pokemon.name} used {move} and dealt {damage} damage!\n"
                f"{self.player_pokemon.name} HP: {self.player_pokemon.hp}/{self.player_pokemon.max_hp}")

    def attack(self, move):
        if move not in self.player_pokemon.moves:
            return f"{self.player_pokemon.name} tried to use {move}, but it's not a valid move!"

        damage = self.player_pokemon.moves[move]
        self.enemy_pokemon.take_damage(damage)
        return (f"{self.player_pokemon.name} used {move}!\n"
                f"{self.enemy_pokemon.name} HP: {self.enemy_pokemon.hp}/{self.enemy_pokemon.max_hp}")

    def switch_pokemon(self, new_pokemon):
        """Switch to another Pokémon."""
        if new_pokemon == self.player_pokemon:
            return f"{new_pokemon.name} is already in battle!"
        
        if new_pokemon == self.player_pokemon1:
            self.player_pokemon = self.player_pokemon1
        elif new_pokemon == self.player_pokemon2:
            self.player_pokemon = self.player_pokemon2
        else:
            return "Invalid Pokémon!"

        return f"Go! {self.player_pokemon.name}!"

    def enemy_switch_pokemon(self, new_pokemon):
        """Switch to another enemy Pokémon."""
        if new_pokemon == self.enemy_pokemon:
            return f"{new_pokemon.name} is already in battle!"
        
        if new_pokemon == self.enemy_pokemon1:
            self.enemy_pokemon = self.enemy_pokemon1
        elif new_pokemon == self.enemy_pokemon2:
            self.enemy_pokemon = self.enemy_pokemon2
        else:
            return "Invalid Pokémon!"

        return f"{self.enemy_pokemon.name} has entered the battle!"
