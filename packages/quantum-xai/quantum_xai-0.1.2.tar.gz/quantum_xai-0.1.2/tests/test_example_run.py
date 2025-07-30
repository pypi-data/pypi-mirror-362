import unittest
import numpy as np
from sklearn.model_selection import train_test_split
from quantum_xai import QuantumNeuralNetwork, QuantumSHAPExplainer, QuantumGradientExplainer, QuantumDatasetLoader

class TestQuantumXAIExample(unittest.TestCase):
    def test_training_and_explanation(self):
        # Load dataset
        X, y, _ = QuantumDatasetLoader.load_iris_quantum(n_samples=50)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        # Create and train model
        model = QuantumNeuralNetwork(n_features=X.shape[1], n_qubits=4, n_layers=2)
        model.train(X_train, y_train, epochs=10, lr=0.1)

        # Check if model is trained
        self.assertTrue(model.is_trained)

        # Create explainers
        shap_explainer = QuantumSHAPExplainer(model, X_train, n_samples=10)
        gradient_explainer = QuantumGradientExplainer(model)

        # Generate explanations
        explanation_shap = shap_explainer.explain(X_test, 0)
        explanation_grad = gradient_explainer.explain(X_test, 0)

        # Check explanation results
        self.assertEqual(len(explanation_shap.feature_importance), X.shape[1])
        self.assertEqual(len(explanation_grad.feature_importance), X.shape[1])

if __name__ == '__main__':
    unittest.main()
