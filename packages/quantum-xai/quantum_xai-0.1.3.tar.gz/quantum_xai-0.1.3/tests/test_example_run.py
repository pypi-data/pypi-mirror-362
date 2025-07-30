import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from quantum_xai import QuantumNeuralNetwork, QuantumSHAPExplainer, QuantumGradientExplainer, QuantumDatasetLoader

def test_basic_training():
    # Basic test to check training and prediction
    X, y, _ = QuantumDatasetLoader.load_iris_quantum(n_samples=50)
    model = QuantumNeuralNetwork(n_features=X.shape[1], n_qubits=4, n_layers=2)
    model.train(X, y, epochs=10, lr=0.1)
    preds = model.predict(X)
    assert len(preds) == len(y)
    assert all(p in [0, 1] for p in preds)
