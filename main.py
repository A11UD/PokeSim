# Main.py

import tkinter as tk
from Ui import PokemonBattleUI, PokemonSelectionUI
from Logic import Pokemon, BattleLogic

# Initialize the Tkinter root window
root = tk.Tk()

# Function to handle Pokémon selection and start the battle
def start_battle(selected_pokemon1, selected_pokemon2):
    # Destroy the Pokémon selection UI to transition to the battle UI
    pokemon_selection_ui.destroy()  # Close the selection UI

    # Initialize the battle logic with the selected Pokémon
    battle_logic = BattleLogic(selected_pokemon1, selected_pokemon2)

    # Initialize the battle UI
    pokemon_battle_ui = PokemonBattleUI(root, battle_logic, selected_pokemon1, selected_pokemon2)
    root.deiconify()  # Ensure the root window is visible after destroying the selection UI


# Initialize the Pokémon selection screen and pass start_battle as a callback
pokemon_selection_ui = PokemonSelectionUI(root, start_battle)

# Start the Tkinter main loop
root.mainloop()
