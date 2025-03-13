# Main.py

import tkinter as tk
from Ui import PokemonBattleUI, PokemonSelectionUI
from Logic import Pokemon, BattleLogic

# Initialize the Tkinter root window
root = tk.Tk()

# Function to handle Pokémon selection
def start_battle(selected_pokemon1, selected_pokemon2):
    battle_logic = BattleLogic(selected_pokemon1, selected_pokemon2)
    pokemon_battle_ui = PokemonBattleUI(root, battle_logic, selected_pokemon1, selected_pokemon2)
    root.mainloop()

# Initialize the Pokémon selection screen
pokemon_selection_ui = PokemonSelectionUI(root, start_battle)

# Start the Tkinter main loop
root.mainloop()
