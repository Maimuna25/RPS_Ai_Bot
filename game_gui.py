import tkinter as tk
from game.game_logic import play_game  # Import the play_game logic
import os
import pandas as pd

# Path to store game results
result_file = 'data/game_results.csv'
data_directory = os.path.dirname(result_file)  # Extract directory path

# Check if the directory exists; create it if it doesn't
if not os.path.exists(data_directory):
    os.makedirs(data_directory)

# Initialize an empty list to accumulate results during the session
game_results = []


def handle_choice(player_choice):
    """Handle the player's choice, play the game, and update the GUI with results."""
    global game_results

    # Play the game
    computer_choice, result = play_game(player_choice, result_file)

    # Display the result on the GUI
    result_label.config(text=f"Computer picked: {computer_choice}\nYou {result}!")

    # Store the result in the list
    if result == 'win':
        game_results.append({'Player Wins': 1, 'Computer Wins': 0, 'Draws': 0})
    elif result == 'lose':
        game_results.append({'Player Wins': 0, 'Computer Wins': 1, 'Draws': 0})
    else:
        game_results.append({'Player Wins': 0, 'Computer Wins': 0, 'Draws': 1})


def end_game():
    """Save game results and close the application."""
    if game_results:
        try:
            # If the file already exists, append the new results
            df_existing = pd.read_csv(result_file)
            df_new = pd.DataFrame(game_results)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        except FileNotFoundError:
            # If the file doesn't exist, create a new DataFrame and save it
            df_combined = pd.DataFrame(game_results)

        # Save the results to the CSV file
        df_combined.to_csv(result_file, index=False)
        print(f"Results saved to {result_file}.")

    # Close the application
    root.quit()


# Create the GUI window
root = tk.Tk()
root.title("Rock-Paper-Scissors")

root.geometry("500x300")  # Adjust these values to set the desired width and height

# Create a label for the game title
title_label = tk.Label(root, text="Rock-Paper-Scissors", font=("Arial", 20))
title_label.pack(pady=10)

# Create buttons for Rock, Paper, and Scissors
rock_button = tk.Button(root, text="Rock", font=("Arial", 14), command=lambda: handle_choice('r'))
rock_button.pack(pady=5)

paper_button = tk.Button(root, text="Paper", font=("Arial", 14), command=lambda: handle_choice('p'))
paper_button.pack(pady=5)

scissors_button = tk.Button(root, text="Scissors", font=("Arial", 14), command=lambda: handle_choice('s'))
scissors_button.pack(pady=5)

# Label to display the result of each round
result_label = tk.Label(root, text="", font=("Arial", 14))
result_label.pack(pady=20)

# Create a button to end the game and save results
end_button = tk.Button(root, text="End Game", font=("Arial", 14), command=end_game)
end_button.pack(pady=20)

# Start the GUI event loop
root.mainloop()
