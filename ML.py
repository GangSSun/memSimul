import numpy as np
from sklearn.ensemble import RandomForestRegressor

# 지도학습 기반 프리페처
class AIMLPrefetcher:
    def __init__(self):
        """Initialize AI-based ML prefetcher."""
        self.model = RandomForestRegressor(n_estimators=10)
        self.training_data = []
        self.training_labels = []
        self.address_history = []  # Track recent address history
        self.name = "ML"

    def train(self):
        """Train the ML model."""
        if len(self.training_data) > 10:  # Train only if sufficient data
            self.model.fit(self.training_data, self.training_labels)

    def prefetch(self, address):
        """Predict next address."""
        # Add the address to history
        self.address_history.append(address)
        if len(self.address_history) < 2:
            return []  # Not enough data to make predictions

        # Use the last two addresses as features
        features = [self.address_history[-2:]]
        if len(self.training_data) > 10:
            predicted_address = int(self.model.predict(features)[0])
            return [predicted_address]
        return []

    def add_training_data(self, address_sequence, next_address):
        """Add training data for supervised learning."""
        if len(address_sequence) < 2:
            return
        self.training_data.append(address_sequence[-2:])
        self.training_labels.append(next_address)
        if len(self.training_data) > 10000:  # Limit training data size
            self.training_data = self.training_data[-1000:]
            self.training_labels = self.training_labels[-1000:]

