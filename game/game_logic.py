import pandas as pd
from game.ai_model import predict_computer_choice, add_player_choice, evaluate_model

# Track the accuracy of AI's predictions
predicted_choices = []

def update_results(result_file, result):
    """Update the results of the game in a CSV file."""
    # Initialize the game result counts
    player_wins = 0
    computer_wins = 0
    draws = 0

    # Update win/loss/draw counts based on the result
    if result == 'win':
        player_wins = 1
    elif result == 'lose':
        computer_wins = 1
    else:
        draws = 1

    # Get the current prediction accuracy from the AI model
    accuracy = evaluate_model()

    # Create a new DataFrame row for the current game's result and AI accuracy
    new_row = pd.DataFrame([{
        'Player Wins': player_wins,
        'Computer Wins': computer_wins,
        'Draws': draws,
        'Prediction Accuracy': accuracy
    }])

    try:
        # Try reading the existing result file
        df_existing = pd.read_csv(result_file)
    except FileNotFoundError:
        # If the file doesn't exist, create an empty DataFrame with the appropriate columns
        df_existing = pd.DataFrame(columns=['Player Wins', 'Computer Wins', 'Draws', 'Prediction Accuracy'])

    # Concatenate the new row with the existing DataFrame
    df_combined = pd.concat([df_existing, new_row], ignore_index=True)

    # Remove duplicate rows (if necessary)
    df_combined.drop_duplicates(inplace=True)

    # Save the updated results back to the CSV file
    df_combined.to_csv(result_file, index=False)

def play_game(player_choice, result_file):
    """Main game logic to handle player and computer moves, and update the result."""
    # Add player's choice to the AI training history
    add_player_choice(player_choice)

    # Predict the computer's next move using the AI model
    computer_choice = predict_computer_choice()

    # Determine the result of the game based on Rock-Paper-Scissors rules
    if player_choice == computer_choice:
        result = 'draw'
    elif (player_choice == 'r' and computer_choice == 's') or \
            (player_choice == 's' and computer_choice == 'p') or \
            (player_choice == 'p' and computer_choice == 'r'):
        result = 'win'
    else:
        result = 'lose'

    # Track the predicted choices for evaluation
    predicted_choices.append(computer_choice)

    # Update the game results in the CSV file
    update_results(result_file, result)

    # Return the computer's choice and the result of the game
    return computer_choice, result
