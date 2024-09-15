from game.game_logic import play_game
import os
import pandas as pd

def main():
    result_file = 'data/game_results.csv'
    data_directory = os.path.dirname(result_file)

    # Check if the directory exists; create it if it doesn't
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)

    # Initialize an empty list to accumulate results during the session
    game_results = []

    player_wins = 0
    computer_wins = 0
    draws = 0

    while True:
        print("\n--- Rock-Paper-Scissors ---")
        player_choice = input('Choices: \n(R)ock \n(P)aper \n(S)cissors \n\nPick: ').lower()
        if player_choice not in ['r', 'p', 's']:
            print("Invalid choice, please try again.")
            continue

        # Play the game and get the computer's choice and result
        computer_choice, result = play_game(player_choice, result_file)


        print(f"Computer picked: {computer_choice}")
        print(f"You {result}!")

        # Update session statistics
        if result == 'win':
            player_wins += 1
            game_results.append({'Player Wins': 1, 'Computer Wins': 0, 'Draws': 0, 'Prediction Accuracy': None})
        elif result == 'lose':
            computer_wins += 1
            game_results.append({'Player Wins': 0, 'Computer Wins': 1, 'Draws': 0, 'Prediction Accuracy': None})
        else:
            draws += 1
            game_results.append({'Player Wins': 0, 'Computer Wins': 0, 'Draws': 1, 'Prediction Accuracy': None})


        cont = input("\nDo you want to play again? (y/n): ").lower()
        if cont != 'y':
            break

    # After the game session ends, display the summary of results
    print("\n--- Game Summary ---")
    print(f"Player Wins: {player_wins}")
    print(f"Computer Wins: {computer_wins}")
    print(f"Draws: {draws}")

    # Store the accumulated results in the CSV file
    if game_results:
        try:
            # If the file already exists, append the new results
            df_existing = pd.read_csv(result_file)
            df_new = pd.DataFrame(game_results)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)

            df_combined.dropna(subset=['Prediction Accuracy'], inplace=True)

            df_combined['Prediction Accuracy'] = df_combined['Prediction Accuracy'].round(2)

            # Remove duplicate rows based on all columns
            df_combined.drop_duplicates(inplace=True)

        except FileNotFoundError:
            # If the file doesn't exist, create a new DataFrame
            df_combined = pd.DataFrame(game_results)

        # Save the results to the CSV file
        df_combined.to_csv(result_file, index=False)
        print(f"Results saved to {result_file}.")

if __name__ == "__main__":
    main()
