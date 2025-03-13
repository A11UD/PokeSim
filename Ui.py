# Ui.py
import random
import tkinter as tk
from PIL import Image, ImageTk
import os
import sys
from Logic import Pokemon, BattleLogic




# Define a list of all available Pokémon
available_pokemons = [
    Pokemon("Pikachu", 100, {"Thunderbolt": 25, "Quick Attack": 15}, "pikachu.png"),
    Pokemon("Charmander", 100, {"Flamethrower": 30, "Scratch": 10}, "charmander.png"),
    Pokemon("Greninja", 100, {"Water Gun": 20, "Quick Attack": 15}, "greninja.png"),
    Pokemon("Ultra Necrozma", 200, {"Photon Geysir": 50, "Splash": 0}, "necro.png"),
    Pokemon("Milotic", 100, {"Water Gun": 20, "Recover": 0}, "milotic.png"),
    Pokemon("Darkrai", 100, {"Nightmare": 40, "Shadow Ball": 25}, "darkrai.png"),
    Pokemon("Incineroar", 100, {"Flamethrower": 30, "Darkest Lariat": 50}, "kitty.png"),
    Pokemon("Giratina", 150, {"Shadow Force": 40, "Dragon Claw": 30}, "giratina.png")
    
]

# Global dictionary to store images and prevent garbage collection issues
image_cache = {}

def resize_image(image_path, size=(180, 180)):
    if not os.path.exists(image_path):
        print(f"Error: Image file not found -> {image_path}")
        return None

    img = Image.open(image_path).convert("RGBA")  # Ensure it's in RGBA mode

    img = img.resize(size, Image.Resampling.LANCZOS)  # Resize with high quality

    # Make white parts fully transparent
    img_data = img.getdata()
    new_img_data = [
        (r, g, b, 0) if (r > 200 and g > 200 and b > 200) else (r, g, b, a)
        for (r, g, b, a) in img_data
    ]
    img.putdata(new_img_data)

    return ImageTk.PhotoImage(img)  # Convert to Tkinter format

class PokemonSelectionUI:
    def __init__(self, root, on_pokemon_selected):
        self.root = root
        self.on_pokemon_selected = on_pokemon_selected
        self.selected_pokemons = []
        self.create_ui()

    def start_battle(self):
        print("Battle is starting with Pokémon:", self.selected_pokemons[0].name, "and", self.selected_pokemons[1].name)
        self.on_pokemon_selected(self.selected_pokemons[0], self.selected_pokemons[1])
        # Create the battle window after selecting Pokémon
        battle_window = tk.Toplevel(self.root)  # This creates a new window for the battle
        battle_ui = PokemonBattleUI(battle_window, self.on_pokemon_selected, self.selected_pokemons[0], self.selected_pokemons[1])
        # Close the selection screen
        self.root.destroy()  # Close the selection screen

    def create_ui(self):
        self.root.title("Select Your Pokémon")
        self.root.geometry("1000x600")

        # Load background image
        self.bg_image = resize_image("background.png", (1000, 600))
        if self.bg_image:
            self.bg_label = tk.Label(self.root, image=self.bg_image)
            self.bg_label.place(relwidth=1, relheight=1)  # Cover full window

        # Ensure background label is stored as an instance variable to prevent garbage collection
        self.bg_label.image = self.bg_image  

        # Display available Pokémon
        self.pokemon_buttons = []
        button_y = 100
        for pokemon in available_pokemons:
            button = tk.Button(self.root, text=pokemon.name, command=lambda p=pokemon: self.select_pokemon(p), font=("Courier New", 16), bg="lightgray")
            button.place(x=50, y=button_y)
            self.pokemon_buttons.append(button)
            button_y += 50

        self.select_label = tk.Label(self.root, text="Select 2 Pokémon", font=("Courier New", 20), bg="lightgray")
        self.select_label.place(x=50, y=30)

    def select_pokemon(self, pokemon):
        if len(self.selected_pokemons) < 2:
            self.selected_pokemons.append(pokemon)
            self.show_selected_pokemon()

        if len(self.selected_pokemons) == 2:
            self.start_battle()

    def show_selected_pokemon(self):
        # Display the selected Pokémon
        selected_text = f"Selected: {', '.join([p.name for p in self.selected_pokemons])}"
        self.select_label.config(text=selected_text)

    # In PokemonSelectionUI class




class PokemonBattleUI:
    def __init__(self, root, battle_logic, pikachu, greninja):
        self.root = root
        self.battle_logic = battle_logic
        self.pikachu = pikachu
        self.greninja = greninja
        self.attack_buttons = []
        self.player_lives = 2
        self.enemy_lives = 2

        self.create_ui()

    def create_ui(self):
        self.root.title("Pokémon Battle")
        self.root.geometry("1000x600")

        # Load background image
        self.bg_image = resize_image("background.png", (1000, 600))
        if self.bg_image:
            self.bg_label = tk.Label(self.root, image=self.bg_image)
            self.bg_label.place(relwidth=1, relheight=1)  # Cover full window

        # Ensure background label is stored as an instance variable to prevent garbage collection
        self.bg_label.image = self.bg_image  

        # Pokémon UI
        self.pokemon_label = tk.Label(self.root, text=f"{self.battle_logic.player_pokemon.name} HP: {self.battle_logic.player_pokemon.hp}", font=("Courier New", 14), bg="gray")
        self.pokemon_label.place(x=20, y=20)

        self.player_pokemon_label = tk.Label(self.root, bd=0, bg = 'lightgreen')
        self.player_pokemon_label.place(x=50, y=350)

        self.enemy_pokemon_label = tk.Label(self.root, bd=0, bg = 'lightgreen')
        self.enemy_pokemon_label.place(x=750, y=20)

        self.enemy_hp_label = tk.Label(self.root, text=f"Enemy HP: {self.battle_logic.enemy_pokemon.hp}", font=("Courier New", 14), bg="gray")
        self.enemy_hp_label.place(x=600, y=20)

        self.message_label = tk.Label(self.root, text="A wild Charmander appears!", font=("Courier New", 12), fg="black", bg="gray")
        self.message_label.place(x=50, y=250)

        self.switch_button = tk.Button(self.root, text="Switch Pokémon", command=self.switch_pokemon, font=("Courier New", 16), bg="gray")
        self.switch_button.place(x=50, y=550)

        self.create_health_bar()  # Create health bars for both Pokémon

        # Add player lives label to show the number of lives
        self.player_lives_label = tk.Label(self.root, text=f"Player Lives: {self.player_lives}", font=("Courier New", 14), bg="gray")
        self.player_lives_label.place(x=800, y=550)

        self.enemy_lives_label = tk.Label(self.root, text=f"Enemy Lives: {self.enemy_lives}", font=("Courier New", 14), bg="gray")
        self.enemy_lives_label.place(x=800, y=500)

        self.update_attack_buttons()
        self.update_pokemon_images()


    def create_lives_display(self):
        # Display player and enemy lives
        self.player_lives_label = tk.Label(self.root, text=f"Player Lives: {self.player_lives}", font=("Courier New", 14), bg="gray")
        self.player_lives_label.place(x=20, y=100)

        self.enemy_lives_label = tk.Label(self.root, text=f"Enemy Lives: {self.enemy_lives}", font=("Courier New", 14), bg="gray")
        self.enemy_lives_label.place(x=600, y=100)


    def update_attack_buttons(self):
        # Remove old buttons
        for btn in self.attack_buttons:
            btn.destroy()

        self.attack_buttons = []  # Reset the list of attack buttons

        # Create new buttons based on the new Pokémon's moves
        button_y = 300
        for move in self.battle_logic.player_pokemon.moves:
            btn = tk.Button(self.root, text=move, command=lambda m=move: self.attack(m), font=("Courier New", 16), bg="gray")
            btn.place(x=50, y=button_y)
            self.attack_buttons.append(btn)  # Store the button to remove it later
            button_y += 30

    def update_lives_display(self):
        # Update the displayed lives
        self.player_lives_label.config(text=f"Player Lives: {self.player_lives}")
        self.enemy_lives_label.config(text=f"Enemy Lives: {self.enemy_lives}")

    def attack(self, move):
        message = self.battle_logic.attack(move)
        self.message_label.config(text=message)
        self.enemy_hp_label.config(text=f"Enemy HP: {self.battle_logic.enemy_pokemon.hp}")

        self.update_health_bar(self.battle_logic.enemy_pokemon, self.enemy_health_bar)

        if self.battle_logic.enemy_pokemon.hp == 0:
            self.message_label.config(text=f"{self.battle_logic.enemy_pokemon.name} fainted!")
            self.change_enemy()
            self.enemy_lives -= 1  # Reduce enemy lives when they lose a Pokémon
            self.update_lives_display()

            if self.check_game_over():
                return  # Stop further game action if game is over
            return
        self.root.after(1000, self.enemy_attack)  # Call enemy_attack with a slight delay

    def flash_effect(self, pokemon_label):
    
        original_color = pokemon_label.cget("bg")
        pokemon_label.config(bg="red")  # Change to red for the flash effect
        self.root.after(100, lambda: pokemon_label.config(bg=original_color))  # Revert after 100ms


    def enemy_flash_effect(self, pokemon_label):

        original_color = pokemon_label.cget("bg")
        pokemon_label.config(bg="red")  # Change to red for the flash effect
        self.root.after(100, lambda: pokemon_label.config(bg=original_color))  # Revert after 100ms


    def enemy_attack(self):
        enemy_moves = self.battle_logic.enemy_pokemon.moves
        if not enemy_moves:
            return  # Prevent crash if enemy has no moves

        enemy_move = random.choice(list(enemy_moves.keys()))  # Get a random move
        damage = self.battle_logic.calculate_damage(self.battle_logic.enemy_pokemon, self.battle_logic.player_pokemon, enemy_move)
        enemy_message = self.battle_logic.enemy_attack(enemy_move)
        self.message_label.config(text=enemy_message)
        self.pokemon_label.config(text=f"{self.battle_logic.player_pokemon.name} HP: {self.battle_logic.player_pokemon.hp}")

        # Trigger movement effect for enemy Pokémon
        self.animate_attack(self.enemy_pokemon_label, -20)  # Move a little bit
        self.flash_effect(self.player_pokemon_label)

        # Update player's health bar
        self.update_health_bar(self.battle_logic.player_pokemon, self.player_health_bar)

        if self.battle_logic.player_pokemon.hp == 0:
            self.message_label.config(text=f"{self.battle_logic.player_pokemon.name} fainted!")
            self.switch_pokemon()
            self.update_health_bar(self.battle_logic.enemy_pokemon, self.enemy_health_bar)
            self.player_lives -= 1  # Reduce player lives when they lose a Pokémon
            self.update_lives_display()

            if self.check_game_over():
                return  # Stop further game action if game is over

    def check_game_over(self):
        """Check if the game is over (both Pokémon are dead)."""
        if self.player_lives == 0:
            self.show_game_over("LOSE")
            return True
        elif self.enemy_lives == 0:
            self.show_game_over("WIN")
            return True
        return False


    def animate_attack(self, pokemon_label, move_distance):
        """Move the Pokémon slightly during the attack to show movement."""
        current_x = pokemon_label.winfo_x()
        current_y = pokemon_label.winfo_y()

        # Move Pokémon a little bit
        pokemon_label.place(x=current_x + move_distance, y=current_y)

        # After 100ms, move it back to its original position
        self.root.after(100, lambda: pokemon_label.place(x=current_x, y=current_y))


    def change_enemy(self):

     # Randomly select an enemy Pokémon from the available pool (excluding the current one)
     available_for_enemy = [p for p in available_pokemons if p != self.battle_logic.enemy_pokemon]
     self.battle_logic.enemy_pokemon = random.choice(available_for_enemy)
     
     # Update the enemy Pokémon's image and health bar
     enemy_pokemon_image = resize_image(self.battle_logic.enemy_pokemon.image_path, (200, 200))
     if enemy_pokemon_image:
         self.enemy_pokemon_label.config(image=enemy_pokemon_image)
         self.enemy_pokemon_label.image = enemy_pokemon_image  # Store reference
         self.update_health_bar(self.battle_logic.enemy_pokemon, self.enemy_health_bar)



    def switch_pokemon(self):
        message = self.battle_logic.switch_pokemon(self.pikachu, self.greninja)
        self.message_label.config(text=message)
        self.update_pokemon_images()
        self.update_attack_buttons()

        self.root.after(1000, self.enemy_attack)


    def update_pokemon_images(self):
        # Update player's Pokémon image
        player_pokemon_image = resize_image(self.battle_logic.player_pokemon.image_path, (200, 200))
        if player_pokemon_image:
            self.player_pokemon_label.config(image=player_pokemon_image)
            self.player_pokemon_label.image = player_pokemon_image  # Store reference

        # Update enemy's Pokémon image
        enemy_pokemon_image = resize_image(self.battle_logic.enemy_pokemon.image_path, (200, 200))
        if enemy_pokemon_image:
            self.enemy_pokemon_label.config(image=enemy_pokemon_image)
            self.enemy_pokemon_label.image = enemy_pokemon_image  # Store reference

    def create_health_bar(self):
        # Create health bars for both player and enemy Pokémon
        self.player_health_bar = tk.Canvas(self.root, width=200, height=20, bg="lightgray")
        self.player_health_bar.place(x=50, y=50)
        self.update_health_bar(self.battle_logic.player_pokemon, self.player_health_bar)

        self.enemy_health_bar = tk.Canvas(self.root, width=200, height=20, bg="lightgray")
        self.enemy_health_bar.place(x=600, y=50)
        self.update_health_bar(self.battle_logic.enemy_pokemon, self.enemy_health_bar)

    def update_health_bar(self, pokemon, health_bar):
        hp_percentage = pokemon.hp / pokemon.max_hp
        health_bar.delete("all")  # Clear the canvas
        health_bar.create_rectangle(0, 0, 200 * hp_percentage, 20, fill="green", width=0)
        # Optionally, you can change the color based on the remaining HP (e.g., red when low HP)
        if hp_percentage < 0.2:
            health_bar.create_rectangle(0, 0, 200 * hp_percentage, 20, fill="red", width=0)
        else:
            health_bar.create_rectangle(0, 0, 200 * hp_percentage, 20, fill="green", width=0)

    def show_game_over(self, result):
        """Display the game over screen with WIN/LOSE message and Restart button."""
        # Create a full-screen overlay
        self.overlay = tk.Frame(self.root, bg="black", width=1000, height=600)
        self.overlay.place(x=0, y=0)

        # Add the WIN/LOSE label
        result_label = tk.Label(self.overlay, text=f"YOU {result}!", font=("Courier New", 32), fg="white", bg="black")
        result_label.place(relx=0.5, rely=0.4, anchor="center")

        # Add the Restart button
        restart_button = tk.Button(self.overlay, text="Restart", font=("Courier New", 16), command=self.restart_game)
        restart_button.place(relx=0.5, rely=0.5, anchor="center")


    def restart_game(self):
        """Restart the game by closing the current window and reopening a new instance."""
        self.root.destroy()  # Close the current game window
        os.execv(sys.executable, ['python'] + sys.argv)  # Restart the script
