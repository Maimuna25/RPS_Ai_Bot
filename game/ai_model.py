import numpy as np
from sklearn.tree import DecisionTreeClassifier

CHOICES = ['r', 'p', 's']

# Initialize the DecisionTree model
model = DecisionTreeClassifier()

# Store player choices and AI's predictions for evaluation
player_choices = []
predicted_choices = []


def add_player_choice(choice):

    global player_choices
    player_choices.append(choice)


def update_model():
    """Train the model based on player choices."""
    # Need at least two moves to train the model
    if len(player_choices) < 2:
        return

    # Prepare the data for model training
    X = np.array([CHOICES.index(player_choices[i-1]) for i in range(1, len(player_choices))]).reshape(-1, 1)
    y = np.array([CHOICES.index(player_choices[i]) for i in range(1, len(player_choices))])

    # Train the model on the historical data
    model.fit(X, y)


def predict_computer_choice():
    """Predict the player's next choice and counter it."""
    update_model()

    if len(player_choices) < 2:

        return np.random.choice(CHOICES)

    last_choice = CHOICES.index(player_choices[-1])

    try:
        # Predict player's next move based on their last move and store it for evaluation
        prediction = model.predict([[last_choice]])[0]
        predicted_choices.append(CHOICES[prediction])

        # AI counters player's predicted move
        if prediction == 0:
            return 'p'
        elif prediction == 1:
            return 's'
        else:
            return 'r'
    except Exception:
        # If the model fails or is not ready, fall back to random choice
        return np.random.choice(CHOICES)


def evaluate_model():
    """Evaluate the model's accuracy."""
    if len(predicted_choices) == 0:
        return 0

    # Compare predicted player moves against their actual next moves
    correct_predictions = sum(1 for i in range(1, len(player_choices)) if predicted_choices[i-1] == player_choices[i])
    accuracy = correct_predictions / (len(player_choices) - 1) if len(player_choices) > 1 else 0

    return accuracy
