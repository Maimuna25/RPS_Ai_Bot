import tkinter as tk
from tkinter import messagebox
from game.game_logic import play_game
import os
import pandas as pd

class RockPaperScissorsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock-Paper-Scissors")
        self.root.geometry("500x300")

        # Path to store game results
        self.result_file = 'data/game_results.csv'
        self.data_directory = os.path.dirname(self.result_file)  # Extract directory path

        # Check if the directory exists; create it if it doesn't
        if not os.path.exists(self.data_directory):
            os.makedirs(self.data_directory)

        # Initialize state
        self.game_results = []
        self.game_started = False

        # Create the GUI components
        self.create_widgets()

    def create_widgets(self):
        """Create GUI widgets and arrange them in the window."""
        # Create a label for the game title
        self.title_label = tk.Label(self.root, text="Rock-Paper-Scissors", font=("Arial", 20))
        self.title_label.pack(pady=10)

        # Create buttons for Rock, Paper, and Scissors
        self.rock_button = tk.Button(self.root, text="Rock", font=("Arial", 14), command=lambda: self.handle_choice('r'), state=tk.DISABLED)
        self.rock_button.pack(pady=5)

        self.paper_button = tk.Button(self.root, text="Paper", font=("Arial", 14), command=lambda: self.handle_choice('p'), state=tk.DISABLED)
        self.paper_button.pack(pady=5)

        self.scissors_button = tk.Button(self.root, text="Scissors", font=("Arial", 14), command=lambda: self.handle_choice('s'), state=tk.DISABLED)
        self.scissors_button.pack(pady=5)

        # Label to display the result of each round
        self.result_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.result_label.pack(pady=20)

        # Create buttons to start the game, end the game, and view results
        self.start_button = tk.Button(self.root, text="Start Game", font=("Arial", 14), command=self.start_game)
        self.start_button.pack(pady=10)

        self.end_button = tk.Button(self.root, text="End Game", font=("Arial", 14), command=self.end_game, state=tk.DISABLED)
        self.end_button.pack(pady=10)

        self.view_results_button = tk.Button(self.root, text="View Results", font=("Arial", 14), command=self.view_results)
        self.view_results_button.pack(pady=10)

    def start_game(self):
        """Initialize the game and enable player choices."""
        if not self.game_started:
            self.game_started = True
            self.result_label.config(text="Game has started! Choose Rock, Paper, or Scissors.")
            # Update the button states
            self.rock_button.config(state=tk.NORMAL)
            self.paper_button.config(state=tk.NORMAL)
            self.scissors_button.config(state=tk.NORMAL)
            self.start_button.config(state=tk.DISABLED)
            self.end_button.config(state=tk.NORMAL)
        else:
            messagebox.showinfo("Game Status", "Game is already running.")

    def handle_choice(self, player_choice):
        """Handle the player's choice, play the game, and update the GUI with results."""
        if not self.game_started:
            messagebox.showwarning("Game Status", "Please start the game first.")
            return

        # Play the game
        computer_choice, result = play_game(player_choice, self.result_file)

        # Display the result on the GUI
        self.result_label.config(text=f"Computer picked: {computer_choice}\nYou {result}!")

        # Store the result in the list
        if result == 'win':
            self.game_results.append({'Player Wins': 1, 'Computer Wins': 0, 'Draws': 0})
        elif result == 'lose':
            self.game_results.append({'Player Wins': 0, 'Computer Wins': 1, 'Draws': 0})
        else:
            self.game_results.append({'Player Wins': 0, 'Computer Wins': 0, 'Draws': 1})

    def end_game(self):
        """Save game results and close the application."""
        if self.game_results:
            try:
                # If the file already exists, append the new results
                df_existing = pd.read_csv(self.result_file)
                df_new = pd.DataFrame(self.game_results)
                df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            except FileNotFoundError:
                # If the file doesn't exist, create a new DataFrame and save it
                df_combined = pd.DataFrame(self.game_results)

            # Save the results to the CSV file
            df_combined.to_csv(self.result_file, index=False)
            messagebox.showinfo("Game Status", f"Results saved to {self.result_file}.")
            self.game_results.clear()  # Clear results for the next session

        self.game_started = False
        self.result_label.config(text="Game has ended. Start a new game or view results.")
        # Update the button states
        self.rock_button.config(state=tk.DISABLED)
        self.paper_button.config(state=tk.DISABLED)
        self.scissors_button.config(state=tk.DISABLED)
        self.start_button.config(state=tk.NORMAL)
        self.end_button.config(state=tk.DISABLED)

    def view_results(self):
        """Display the results from the CSV file."""
        if not os.path.exists(self.result_file):
            messagebox.showwarning("No Results", "No game results found.")
            return

        try:
            df = pd.read_csv(self.result_file)
            results_str = df.to_string(index=False)
            messagebox.showinfo("Game Results", results_str)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

# Create the GUI window
root = tk.Tk()
app = RockPaperScissorsApp(root)

# Start the GUI event loop
root.mainloop()
