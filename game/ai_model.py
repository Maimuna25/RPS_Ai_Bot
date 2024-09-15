import numpy as np
from sklearn.tree import DecisionTreeClassifier

CHOICES = ['r', 'p', 's']

class RockPaperScissorsAI:
    def __init__(self):
        # Initialize the DecisionTree model
        self.model = DecisionTreeClassifier()
        self.player_choices = []
        self.predicted_choices = []

    def add_player_choice(self, choice):
        """Add the player's choice to the list."""
        self.player_choices.append(choice)

    def update_model(self):
        """Train the model based on player choices."""
        # Need at least two moves to train the model
        if len(self.player_choices) < 2:
            return

        # Prepare the data for model training
        X = np.array([CHOICES.index(self.player_choices[i-1]) for i in range(1, len(self.player_choices))]).reshape(-1, 1)
        y = np.array([CHOICES.index(self.player_choices[i]) for i in range(1, len(self.player_choices))])

        # Train the model on the historical data
        self.model.fit(X, y)

    def predict_computer_choice(self):
        """Predict the player's next choice and counter it."""
        self.update_model()

        if len(self.player_choices) < 2:
            return np.random.choice(CHOICES)

        last_choice = CHOICES.index(self.player_choices[-1])

        try:
            # Predict player's next move based on their last move and store it for evaluation
            prediction = self.model.predict([[last_choice]])[0]
            self.predicted_choices.append(CHOICES[prediction])

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

    def evaluate_model(self):
        """Evaluate the model's accuracy."""
        if len(self.predicted_choices) == 0:
            return 0

        # Compare predicted player moves against their actual next moves
        correct_predictions = sum(1 for i in range(1, len(self.player_choices)) if self.predicted_choices[i-1] == self.player_choices[i])
        accuracy = correct_predictions / (len(self.player_choices) - 1) if len(self.player_choices) > 1 else 0

        return accuracy
