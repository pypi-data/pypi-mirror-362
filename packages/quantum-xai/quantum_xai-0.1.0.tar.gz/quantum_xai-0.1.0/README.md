# Quantum-XAI: Explainable Quantum Machine Learning Library

Quantum-XAI is a comprehensive, production-ready toolkit for explainable quantum machine learning. It provides a suite of quantum-native explainability methods, quantum neural network models, advanced visualizations, benchmarking tools, and research-grade features to interpret and analyze quantum neural network decisions.

---

## Features

- **Quantum Neural Network Models**
  - Variational Quantum Classifier (VQC) implementation using PennyLane
  - Supports multiple quantum data encodings: Angle, Amplitude, and IQP encoding

- **Explainability Methods**
  - Quantum SHAP Explainer: SHAP-like sampling-based explanations
  - Quantum Gradient Explainer: Gradient-based explanations using parameter-shift rule
  - Quantum LIME Explainer: LIME-like local surrogate model explanations
  - Quantum Perturbation Explainer: Feature occlusion based explanations

- **Visualization Tools**
  - Feature importance bar charts
  - Side-by-side explanation method comparisons
  - Quantum circuit diagrams with explanation overlays
  - Radar charts for quantum feature importance

- **Datasets & Utilities**
  - Preprocessed quantum-ready datasets: Iris, Wine, Breast Cancer
  - Dataset loaders with normalization and binary classification options

- **Benchmarking & Evaluation**
  - Compare multiple explainers on test samples
  - Compute explanation consistency and quality metrics
  - Faithfulness, sparsity, stability, and top feature importance analysis

- **Research Extensions**
  - Quantum Fisher Information matrix computation
  - Quantum entanglement contribution analysis
  - Quantum feature interaction analysis beyond classical correlations

- **Save/Load Functionality**
  - Save trained models and explanations to JSON
  - Load models and explanations from JSON for reproducibility

- **Complete Demo**
  - End-to-end demonstration of training, explaining, visualizing, benchmarking, and reporting

---

## Installation

Ensure you have Python 3.7+ installed. Install required dependencies:

```bash
pip install pennylane numpy matplotlib seaborn scikit-learn pandas
```

---

## Usage

### Quick Start Demo

Run the complete demonstration with the Iris dataset:

```python
from quantum_xai import QuantumXAIDemo

demo = QuantumXAIDemo()
results = demo.run_complete_demo(dataset='iris', n_samples=80)
```

### Custom Model Training and Explanation

```python
from quantum_xai import QuantumNeuralNetwork, QuantumSHAPExplainer, QuantumGradientExplainer, QuantumXAIVisualizer
from sklearn.model_selection import train_test_split
from quantum_xai import QuantumDatasetLoader

# Load data
X, y, feature_names = QuantumDatasetLoader.load_iris_quantum(n_samples=100)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Create and train model
model = QuantumNeuralNetwork(n_features=X.shape[1], n_qubits=4, n_layers=2)
model.train(X_train, y_train, epochs=100, lr=0.1)

# Create explainers
shap_explainer = QuantumSHAPExplainer(model, X_train)
gradient_explainer = QuantumGradientExplainer(model)

# Generate explanation for a sample
explanation = shap_explainer.explain(X_test, 0)

# Visualize explanation
visualizer = QuantumXAIVisualizer()
fig = visualizer.plot_feature_importance(explanation, feature_names)
fig.show()
```

---

## Research Applications

- Benchmark quantum vs classical explainability methods
- Analyze quantum Fisher information and entanglement effects
- Extend to other quantum platforms (Qiskit, Cirq)
- Develop advanced quantum-specific explanation metrics
- Apply to real quantum datasets in chemistry, finance, and more

---

## Project Structure

- `QuantumNeuralNetwork`: Variational quantum classifier model
- `QuantumExplainer` and subclasses: Explainability methods (SHAP, Gradient, LIME, Perturbation)
- `QuantumXAIVisualizer`: Visualization utilities
- `QuantumDatasetLoader`: Dataset loading and preprocessing
- `QuantumXAIBenchmark`: Benchmarking and evaluation tools
- `QuantumXAIDemo`: Complete demo and example workflows
- `save_model_and_explanations` / `load_model_and_explanations`: Persistence utilities
- `QuantumXAIResearch`: Advanced research features

---

## License

This project is open-source and available for research, publication, and industry use.

---

## Contact

For questions, contributions, or collaborations, please open an issue or pull request on the GitHub repository.

---

# Acknowledgments

This library builds upon PennyLane and scikit-learn, leveraging quantum computing and classical ML explainability techniques.
