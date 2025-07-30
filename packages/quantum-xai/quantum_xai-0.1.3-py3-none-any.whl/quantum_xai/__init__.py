# Quantum-XAI: Explainable Quantum Machine Learning Library
# Version 0.1.0

import numpy as np
import pennylane as qml
from pennylane import numpy as pnp
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Tuple, Optional, Union, Callable
import warnings
from sklearn.datasets import load_iris, load_wine, load_breast_cancer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pandas as pd
from dataclasses import dataclass
from abc import ABC, abstractmethod
import pickle
import json

# ============================================================================

@dataclass
class ExplanationResult:
    """Container for explanation results"""
    feature_importance: np.ndarray
    sample_idx: int
    prediction: float
    prediction_proba: Optional[np.ndarray] = None
    method: str = "unknown"
    metadata: Dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

class QuantumExplainer(ABC):
    """Abstract base class for quantum explainers"""
    
    def __init__(self, model, device=None):
        self.model = model
        self.device = device or qml.device('default.qubit', wires=4)
        self.feature_names = None
        
    @abstractmethod
    def explain(self, X: np.ndarray, sample_idx: int) -> ExplanationResult:
        """Explain a single prediction"""
        pass
    
    def explain_batch(self, X: np.ndarray, indices: List[int]) -> List[ExplanationResult]:
        """Explain multiple predictions"""
        return [self.explain(X, idx) for idx in indices]

# ============================================================================

class QuantumEncoder:
    """Handles different quantum state encodings"""
    
    @staticmethod
    def angle_encoding(features: np.ndarray, wires: List[int]):
        """Encode classical data using rotation angles"""
        for i, wire in enumerate(wires):
            if i < len(features):
                qml.RY(features[i], wires=wire)
    
    @staticmethod
    def amplitude_encoding(features: np.ndarray, wires: List[int]):
        """Encode classical data in quantum amplitudes"""
        features_normalized = features / np.linalg.norm(features)
        n_qubits = len(wires)
        target_size = 2**n_qubits
        if len(features_normalized) < target_size:
            features_normalized = np.pad(features_normalized, 
                                       (0, target_size - len(features_normalized)))
        qml.AmplitudeEmbedding(features_normalized[:target_size], wires=wires)
    
    @staticmethod
    def iqp_encoding(features: np.ndarray, wires: List[int], layers: int = 1):
        """Instantaneous Quantum Polynomial (IQP) encoding"""
        for layer in range(layers):
            for i, wire in enumerate(wires):
                if i < len(features):
                    qml.RZ(features[i], wires=wire)
            for i in range(len(wires)-1):
                qml.CNOT(wires=[wires[i], wires[i+1]])

# ============================================================================

class QuantumNeuralNetwork:
    """Variational Quantum Classifier (VQC) implementation"""
    
    def __init__(self, n_features: int, n_qubits: int = 4, n_layers: int = 2, 
                 encoding: str = 'angle', device_name: str = 'default.qubit'):
        self.n_features = n_features
        self.n_qubits = n_qubits
        self.n_layers = n_layers
        self.encoding = encoding
        self.device = qml.device(device_name, wires=n_qubits)
        self.params = self._init_parameters()
        self.is_trained = False
        self.qnode = qml.QNode(self._circuit, self.device, diff_method='parameter-shift')
        
    def _init_parameters(self) -> np.ndarray:
        return np.random.normal(0, 0.1, (self.n_layers, self.n_qubits, 3))
    
    def _circuit(self, features: np.ndarray, params: np.ndarray) -> float:
        if self.encoding == 'angle':
            QuantumEncoder.angle_encoding(features, list(range(self.n_qubits)))
        elif self.encoding == 'amplitude':
            QuantumEncoder.amplitude_encoding(features, list(range(self.n_qubits)))
        elif self.encoding == 'iqp':
            QuantumEncoder.iqp_encoding(features, list(range(self.n_qubits)))
        for layer in range(self.n_layers):
            for i in range(self.n_qubits):
                qml.RX(params[layer, i, 0], wires=i)
                qml.RY(params[layer, i, 1], wires=i)
                qml.RZ(params[layer, i, 2], wires=i)
            for i in range(self.n_qubits - 1):
                qml.CNOT(wires=[i, i + 1])
        return qml.expval(qml.PauliZ(0))
    
    def forward(self, X: np.ndarray) -> np.ndarray:
        if X.ndim == 1:
            return self.qnode(X, self.params)
        else:
            return np.array([self.qnode(x, self.params) for x in X])
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        outputs = self.forward(X)
        return (outputs > 0).astype(int)
    
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        outputs = self.forward(X)
        probs = 1 / (1 + np.exp(-outputs))
        return np.column_stack([1 - probs, probs])
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray, 
              epochs: int = 100, lr: float = 0.1):
        opt = qml.AdamOptimizer(stepsize=lr)
        def cost_fn(params):
            predictions = np.array([self.qnode(x, params) for x in X_train])
            labels = 2 * y_train - 1
            loss = np.mean(np.maximum(0, 1 - labels * predictions))
            return loss
        for epoch in range(epochs):
            self.params = opt.step(cost_fn, self.params)
            if epoch % 20 == 0:
                loss = cost_fn(self.params)
                print(f"Epoch {epoch}: Loss = {loss:.4f}")
        self.is_trained = True
        print("Training completed!")

# ============================================================================

class QuantumSHAPExplainer(QuantumExplainer):
    """SHAP-like explainer for quantum neural networks"""
    
    def __init__(self, model: QuantumNeuralNetwork, background_data: np.ndarray, 
                 n_samples: int = 100):
        super().__init__(model)
        self.background_data = background_data
        self.n_samples = n_samples
        self.baseline = np.mean(background_data, axis=0)
        
    def explain(self, X: np.ndarray, sample_idx: int) -> ExplanationResult:
        sample = X[sample_idx]
        n_features = len(sample)
        shap_values = np.zeros(n_features)
        baseline_pred = self.model.forward(self.baseline)
        sample_pred = self.model.forward(sample)
        for i in range(n_features):
            marginal_contributions = []
            for _ in range(self.n_samples):
                coalition = np.random.choice([0, 1], size=n_features, p=[0.5, 0.5])
                coalition_without = coalition.copy()
                coalition_without[i] = 0
                coalition_with = coalition.copy()
                coalition_with[i] = 1
                sample_without = self.baseline * (1 - coalition_without) + sample * coalition_without
                sample_with = self.baseline * (1 - coalition_with) + sample * coalition_with
                pred_without = self.model.forward(sample_without)
                pred_with = self.model.forward(sample_with)
                marginal_contributions.append(pred_with - pred_without)
            shap_values[i] = np.mean(marginal_contributions)
        return ExplanationResult(
            feature_importance=shap_values,
            sample_idx=sample_idx,
            prediction=sample_pred,
            prediction_proba=self.model.predict_proba(sample.reshape(1, -1))[0],
            method="quantum_shap",
            metadata={"n_samples": self.n_samples}
        )

# ============================================================================

class QuantumGradientExplainer(QuantumExplainer):
    """Gradient-based explainer for quantum neural networks"""
    
    def __init__(self, model: QuantumNeuralNetwork, method: str = 'parameter_shift'):
        super().__init__(model)
        self.method = method
        
    def explain(self, X: np.ndarray, sample_idx: int) -> ExplanationResult:
        sample = X[sample_idx]
        grad_fn = qml.grad(self._prediction_fn, argnum=0)
        gradients = grad_fn(sample, self.model.params)
        prediction = self.model.forward(sample)
        return ExplanationResult(
            feature_importance=gradients,
            sample_idx=sample_idx,
            prediction=prediction,
            prediction_proba=self.model.predict_proba(sample.reshape(1, -1))[0],
            method=f"quantum_gradient_{self.method}",
            metadata={"gradient_method": self.method}
        )
    
    def _prediction_fn(self, features: np.ndarray, params: np.ndarray) -> float:
        return self.model.qnode(features, params)

# ============================================================================

class QuantumLIMEExplainer(QuantumExplainer):
    """LIME-like explainer for quantum neural networks"""
    
    def __init__(self, model: QuantumNeuralNetwork, n_samples: int = 1000, 
                 kernel_width: float = 0.25):
        super().__init__(model)
        self.n_samples = n_samples
        self.kernel_width = kernel_width
        
    def explain(self, X: np.ndarray, sample_idx: int) -> ExplanationResult:
        sample = X[sample_idx]
        n_features = len(sample)
        perturbed_samples = []
        distances = []
        for _ in range(self.n_samples):
            perturbation = np.random.normal(0, 0.1, size=n_features)
            perturbed_sample = sample + perturbation
            distance = np.linalg.norm(perturbation)
            perturbed_samples.append(perturbed_sample)
            distances.append(distance)
        perturbed_samples = np.array(perturbed_samples)
        distances = np.array(distances)
        predictions = self.model.forward(perturbed_samples)
        weights = np.exp(-(distances ** 2) / (self.kernel_width ** 2))
        from sklearn.linear_model import LinearRegression
        interpretable_samples = perturbed_samples - sample
        linear_model = LinearRegression()
        linear_model.fit(interpretable_samples, predictions, sample_weight=weights)
        original_pred = self.model.forward(sample)
        return ExplanationResult(
            feature_importance=linear_model.coef_,
            sample_idx=sample_idx,
            prediction=original_pred,
            prediction_proba=self.model.predict_proba(sample.reshape(1, -1))[0],
            method="quantum_lime",
            metadata={
                "n_samples": self.n_samples,
                "kernel_width": self.kernel_width,
                "r2_score": linear_model.score(interpretable_samples, predictions, sample_weight=weights)
            }
        )

# ============================================================================

class QuantumPerturbationExplainer(QuantumExplainer):
    """Perturbation-based explainer using feature occlusion"""
    
    def __init__(self, model: QuantumNeuralNetwork, baseline_strategy: str = 'mean'):
        super().__init__(model)
        self.baseline_strategy = baseline_strategy
        
    def explain(self, X: np.ndarray, sample_idx: int) -> ExplanationResult:
        sample = X[sample_idx]
        n_features = len(sample)
        if self.baseline_strategy == 'mean':
            baseline_values = np.mean(X, axis=0)
        elif self.baseline_strategy == 'zero':
            baseline_values = np.zeros(n_features)
        else:
            baseline_values = np.zeros(n_features)
        original_pred = self.model.forward(sample)
        feature_importance = np.zeros(n_features)
        for i in range(n_features):
            occluded_sample = sample.copy()
            occluded_sample[i] = baseline_values[i]
            occluded_pred = self.model.forward(occluded_sample)
            feature_importance[i] = original_pred - occluded_pred
        return ExplanationResult(
            feature_importance=feature_importance,
            sample_idx=sample_idx,
            prediction=original_pred,
            prediction_proba=self.model.predict_proba(sample.reshape(1, -1))[0],
            method="quantum_perturbation",
            metadata={"baseline_strategy": self.baseline_strategy}
        )

# ============================================================================

class QuantumXAIVisualizer:
    """Visualization tools for quantum explainability"""
    
    @staticmethod
    def plot_feature_importance(explanation: ExplanationResult, 
                              feature_names: Optional[List[str]] = None,
                              title: str = None) -> plt.Figure:
        fig, ax = plt.subplots(figsize=(10, 6))
        importance = explanation.feature_importance
        n_features = len(importance)
        if feature_names is None:
            feature_names = [f"Feature {i}" for i in range(n_features)]
        sorted_idx = np.argsort(np.abs(importance))
        sorted_importance = importance[sorted_idx]
        sorted_names = [feature_names[i] for i in sorted_idx]
        colors = ['red' if x < 0 else 'blue' for x in sorted_importance]
        bars = ax.barh(range(n_features), sorted_importance, color=colors, alpha=0.7)
        ax.set_yticks(range(n_features))
        ax.set_yticklabels(sorted_names)
        ax.set_xlabel('Feature Importance')
        ax.set_title(title or f'Feature Importance ({explanation.method})')
        ax.axvline(x=0, color='black', linestyle='-', linewidth=0.5)
        for i, (bar, value) in enumerate(zip(bars, sorted_importance)):
            ax.text(value + 0.01 * np.sign(value), i, f'{value:.3f}', 
                   va='center', fontsize=9)
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_explanation_comparison(explanations: List[ExplanationResult],
                                  feature_names: Optional[List[str]] = None,
                                  title: str = "Method Comparison") -> plt.Figure:
        fig, axes = plt.subplots(len(explanations), 1, 
                                figsize=(12, 4 * len(explanations)))
        if len(explanations) == 1:
            axes = [axes]
        for i, explanation in enumerate(explanations):
            ax = axes[i]
            importance = explanation.feature_importance
            n_features = len(importance)
            if feature_names is None:
                feature_names = [f"Feature {j}" for j in range(n_features)]
            colors = ['red' if x < 0 else 'blue' for x in importance]
            bars = ax.bar(range(n_features), importance, color=colors, alpha=0.7)
            ax.set_xticks(range(n_features))
            ax.set_xticklabels(feature_names, rotation=45, ha='right')
            ax.set_ylabel('Importance')
            ax.set_title(f'{explanation.method} (Pred: {explanation.prediction:.3f})')
            ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
            for bar, value in zip(bars, importance):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.01 * np.sign(height),
                       f'{value:.3f}', ha='center', va='bottom' if height > 0 else 'top',
                       fontsize=8)
        plt.suptitle(title, fontsize=16)
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_quantum_circuit_explanation(model: QuantumNeuralNetwork,
                                       sample: np.ndarray,
                                       explanation: ExplanationResult) -> plt.Figure:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        ax1.set_title("Quantum Circuit Structure")
        n_qubits = model.n_qubits
        qubit_positions = np.arange(n_qubits)
        for i in range(n_qubits):
            ax1.axhline(y=i, color='black', linewidth=2)
            ax1.text(-0.5, i, f'q{i}', ha='center', va='center', fontsize=12)
        for i in range(min(len(sample), n_qubits)):
            importance = explanation.feature_importance[i] if i < len(explanation.feature_importance) else 0
            color_intensity = min(abs(importance) / max(abs(explanation.feature_importance)), 1.0)
            color = plt.cm.RdBu(0.5 + 0.5 * np.sign(importance) * color_intensity)
            rect = plt.Rectangle((0.5, i-0.2), 0.4, 0.4, 
                               facecolor=color, edgecolor='black', linewidth=2)
            ax1.add_patch(rect)
            ax1.text(0.7, i, f'R({sample[i]:.2f})', ha='center', va='center', fontsize=8)
        for layer in range(model.n_layers):
            x_pos = 2 + layer * 2
            for i in range(n_qubits):
                rect = plt.Rectangle((x_pos, i-0.15), 0.3, 0.3, 
                                   facecolor='lightblue', edgecolor='black')
                ax1.add_patch(rect)
                ax1.text(x_pos + 0.15, i, 'U', ha='center', va='center', fontsize=10)
            for i in range(n_qubits - 1):
                ax1.plot([x_pos + 0.5, x_pos + 0.5], [i, i+1], 'ro-', markersize=8)
        x_pos = 2 + model.n_layers * 2
        rect = plt.Rectangle((x_pos, -0.2), 0.4, 0.4, 
                           facecolor='yellow', edgecolor='black', linewidth=2)
        ax1.add_patch(rect)
        ax1.text(x_pos + 0.2, 0, 'M', ha='center', va='center', fontsize=12)
        ax1.set_xlim(-1, x_pos + 1)
        ax1.set_ylim(-0.5, n_qubits - 0.5)
        ax1.set_aspect('equal')
        ax1.axis('off')
        ax2.set_title("Feature Importance in Quantum Context")
        importance = explanation.feature_importance
        n_features = len(importance)
        feature_names = [f"x{i}" for i in range(n_features)]
        angles = np.linspace(0, 2*np.pi, n_features, endpoint=False).tolist()
        angles += angles[:1]
        importance_normalized = importance / (np.max(np.abs(importance)) + 1e-8)
        importance_plot = importance_normalized.tolist()
        importance_plot += importance_plot[:1]
        ax2_polar = plt.subplot(122, projection='polar')
        ax2_polar.plot(angles, importance_plot, 'o-', linewidth=2)
        ax2_polar.fill(angles, importance_plot, alpha=0.25)
        ax2_polar.set_xticks(angles[:-1])
        ax2_polar.set_xticklabels(feature_names)
        ax2_polar.set_ylim(-1, 1)
        ax2_polar.set_title("Feature Importance (Quantum)", pad=20)
        ax2_polar.grid(True)
        plt.tight_layout()
        return fig

# ============================================================================

class QuantumDatasetLoader:
    """Utility functions for loading and preprocessing datasets for quantum ML"""
    
    @staticmethod
    def load_iris_quantum(n_samples: int = None, binary: bool = True) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        iris = load_iris()
        X, y = iris.data, iris.target
        if binary:
            binary_mask = y < 2
            X = X[binary_mask]
            y = y[binary_mask]
        scaler = StandardScaler()
        X = scaler.fit_transform(X)
        if n_samples is not None:
            X = X[:n_samples]
            y = y[:n_samples]
        return X, y, iris.feature_names
    
    @staticmethod
    def load_wine_quantum(n_samples: int = None, binary: bool = True) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        wine = load_wine()
        X, y = wine.data, wine.target
        if binary:
            binary_mask = y < 2
            X = X[binary_mask]
            y = y[binary_mask]
        scaler = StandardScaler()
        X = scaler.fit_transform(X)
        if n_samples is not None:
            X = X[:n_samples]
            y = y[:n_samples]
        return X, y, wine.feature_names
    
    @staticmethod
    def load_breast_cancer_quantum(n_samples: int = None) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        bc = load_breast_cancer()
        X, y = bc.data, bc.target
        scaler = StandardScaler()
        X = scaler.fit_transform(X)
        if n_samples is not None:
            X = X[:n_samples]
            y = y[:n_samples]
        return X, y, bc.feature_names

# ============================================================================

class QuantumXAIBenchmark:
    """Benchmarking tools for quantum explainability methods"""
    
    def __init__(self, model: QuantumNeuralNetwork, X_test: np.ndarray, 
                 y_test: np.ndarray, feature_names: List[str]):
        self.model = model
        self.X_test = X_test
        self.y_test = y_test
        self.feature_names = feature_names
        
    def compare_explainers(self, explainers: List[QuantumExplainer], 
                          sample_indices: List[int]) -> Dict:
        results = {}
        for explainer in explainers:
            explainer_name = explainer.__class__.__name__
            results[explainer_name] = []
            for idx in sample_indices:
                explanation = explainer.explain(self.X_test, idx)
                results[explainer_name].append(explanation)
        return results
    
    def compute_explanation_consistency(self, explanations: List[ExplanationResult]) -> float:
        if len(explanations) < 2:
            return 1.0
        correlations = []
        for i in range(len(explanations)):
            for j in range(i + 1, len(explanations)):
                corr = np.corrcoef(explanations[i].feature_importance, 
                                 explanations[j].feature_importance)[0, 1]
                if not np.isnan(corr):
                    correlations.append(abs(corr))
        return np.mean(correlations) if correlations else 0.0
    
    def evaluate_explanation_quality(self, explanation: ExplanationResult, 
                                   sample_idx: int) -> Dict:
        sample = self.X_test[sample_idx]
        original_pred = self.model.forward(sample)
        faithfulness_scores = []
        for i in range(len(sample)):
            modified_sample = sample.copy()
            modified_sample[i] = 0
            modified_pred = self.model.forward(modified_sample)
            pred_change = abs(original_pred - modified_pred)
            faithfulness_scores.append(pred_change)
        faithfulness_corr = np.corrcoef(np.abs(explanation.feature_importance), 
                                       faithfulness_scores)[0, 1]
        return {
            'faithfulness_correlation': faithfulness_corr if not np.isnan(faithfulness_corr) else 0.0,
            'explanation_sparsity': np.sum(np.abs(explanation.feature_importance) > 0.01) / len(explanation.feature_importance),
            'explanation_stability': np.std(explanation.feature_importance),
            'top_feature_importance': np.max(np.abs(explanation.feature_importance))
        }

# ============================================================================

class QuantumXAIDemo:
    """Complete demonstration of the Quantum XAI library"""
    
    def __init__(self):
        self.model = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.feature_names = None
        
    def run_complete_demo(self, dataset: str = 'iris', n_samples: int = 100):
        print("="*80)
        print("QUANTUM XAI LIBRARY - COMPLETE DEMONSTRATION")
        print("="*80)
        print("\n1. Loading and preparing dataset...")
        if dataset == 'iris':
            X, y, feature_names = QuantumDatasetLoader.load_iris_quantum(n_samples)
        elif dataset == 'wine':
            X, y, feature_names = QuantumDatasetLoader.load_wine_quantum(n_samples)
        elif dataset == 'breast_cancer':
            X, y, feature_names = QuantumDatasetLoader.load_breast_cancer_quantum(n_samples)
        else:
            raise ValueError(f"Unknown dataset: {dataset}")
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.3, random_state=42
        )
        self.feature_names = feature_names
        print(f"Dataset: {dataset}")
        print(f"Training samples: {len(self.X_train)}")
        print(f"Test samples: {len(self.X_test)}")
        print(f"Features: {len(feature_names)}")
        print("\n2. Creating and training quantum neural network...")
        self.model = QuantumNeuralNetwork(
            n_features=X.shape[1],
            n_qubits=4,
            n_layers=2,
            encoding='angle'
        )
        self.model.train(self.X_train, self.y_train, epochs=100, lr=0.1)
        train_acc = np.mean(self.model.predict(self.X_train) == self.y_train)
        test_acc = np.mean(self.model.predict(self.X_test) == self.y_test)
        print(f"Training accuracy: {train_acc:.3f}")
        print(f"Test accuracy: {test_acc:.3f}")
        print("\n3. Initializing explainers...")
        explainers = {
            'SHAP': QuantumSHAPExplainer(self.model, self.X_train, n_samples=50),
            'Gradient': QuantumGradientExplainer(self.model),
            'LIME': QuantumLIMEExplainer(self.model, n_samples=500),
            'Perturbation': QuantumPerturbationExplainer(self.model)
        }
        print("\n4. Generating explanations...")
        sample_idx = 0
        sample = self.X_test[sample_idx]
        explanations = {}
        for name, explainer in explainers.items():
            print(f"   Computing {name} explanation...")
            explanation = explainer.explain(self.X_test, sample_idx)
            explanations[name] = explanation
        print("\n5. Creating visualizations...")
        visualizer = QuantumXAIVisualizer()
        for name, explanation in explanations.items():
            fig = visualizer.plot_feature_importance(
                explanation, 
                feature_names=feature_names[:len(explanation.feature_importance)],
                title=f"{name} Explanation"
            )
            plt.show()
        fig = visualizer.plot_explanation_comparison(
            list(explanations.values()),
            feature_names=feature_names[:len(explanations['SHAP'].feature_importance)],
            title="Explainer Method Comparison"
        )
        plt.show()
        fig = visualizer.plot_quantum_circuit_explanation(
            self.model, sample, explanations['SHAP']
        )
        plt.show()
        print("\n6. Benchmarking explainers...")
        benchmark = QuantumXAIBenchmark(self.model, self.X_test, self.y_test, feature_names)
        sample_indices = [0, 1, 2, 3, 4]
        comparison_results = benchmark.compare_explainers(
            list(explainers.values()), sample_indices
        )
        for idx in sample_indices:
            sample_explanations = [comparison_results[name][idx] for name in comparison_results.keys()]
            consistency = benchmark.compute_explanation_consistency(sample_explanations)
            print(f"Sample {idx} explanation consistency: {consistency:.3f}")
        print("\n7. Generating comprehensive report...")
        self.generate_report(explanations, comparison_results, benchmark)
        print("\n" + "="*80)
        print("DEMONSTRATION COMPLETED SUCCESSFULLY!")
        print("="*80)
        return {
            'model': self.model,
            'explanations': explanations,
            'benchmark_results': comparison_results,
            'test_accuracy': test_acc
        }
    
    def generate_report(self, explanations: Dict, comparison_results: Dict, 
                       benchmark: QuantumXAIBenchmark):
        print("\n" + "="*60)
        print("QUANTUM XAI ANALYSIS REPORT")
        print("="*60)
        print(f"\nModel Performance:")
        print(f"- Test Accuracy: {np.mean(self.model.predict(self.X_test) == self.y_test):.3f}")
        print(f"- Model Type: Variational Quantum Classifier")
        print(f"- Encoding: {self.model.encoding}")
        print(f"- Qubits: {self.model.n_qubits}")
        print(f"- Layers: {self.model.n_layers}")
        print(f"\nExplainer Methods Comparison:")
        for name, explanation in explanations.items():
            importance = explanation.feature_importance
            print(f"\n{name}:")
            print(f"  - Top feature: {self.feature_names[np.argmax(np.abs(importance))]}")
            print(f"  - Max importance: {np.max(np.abs(importance)):.4f}")
            print(f"  - Importance range: [{np.min(importance):.4f}, {np.max(importance):.4f}]")
            print(f"  - Sparsity: {np.sum(np.abs(importance) > 0.01) / len(importance):.3f}")
        print(f"\nFeature Ranking Comparison:")
        print(f"{'Rank':<6} {'SHAP':<15} {'Gradient':<15} {'LIME':<15} {'Perturbation':<15}")
        print("-" * 75)
        for method_name, explanation in explanations.items():
            importance = explanation.feature_importance
            sorted_indices = np.argsort(np.abs(importance))[::-1]
            for rank, idx in enumerate(sorted_indices[:5]):
                if rank == 0:
                    print(f"{rank+1:<6} {self.feature_names[idx]:<15}", end="")
                else:
                    print(f"{rank+1:<6} {self.feature_names[idx]:<15}", end="")
                if method_name == 'SHAP':
                    print()
        print(f"\nMethod-specific Insights:")
        shap_exp = explanations['SHAP']
        print(f"\nSHAP Analysis:")
        print(f"  - Samples used: {shap_exp.metadata['n_samples']}")
        print(f"  - Most influential feature: {self.feature_names[np.argmax(np.abs(shap_exp.feature_importance))]}")
        grad_exp = explanations['Gradient']
        print(f"\nGradient Analysis:")
        print(f"  - Method: {grad_exp.metadata['gradient_method']}")
        print(f"  - Steepest gradient: {self.feature_names[np.argmax(np.abs(grad_exp.feature_importance))]}")
        lime_exp = explanations['LIME']
        print(f"\nLIME Analysis:")
        print(f"  - R² score: {lime_exp.metadata['r2_score']:.3f}")
        print(f"  - Samples used: {lime_exp.metadata['n_samples']}")
        print(f"\nQuantum-Specific Observations:")
        print(f"  - Quantum encoding affects feature interpretation")
        print(f"  - Entanglement creates non-linear feature interactions")
        print(f"  - Parameter-shift rule enables exact gradient computation")
        print(f"  - Quantum superposition allows parallel feature evaluation")

# ============================================================================

def main():
    print("Running Quick Start Example...")
    demo = QuantumXAIDemo()
    results = demo.run_complete_demo(dataset='iris', n_samples=80)
    print("\n\nRunning Advanced Example...")
    X, y, feature_names = QuantumDatasetLoader.load_wine_quantum(n_samples=100)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    model = QuantumNeuralNetwork(
        n_features=X.shape[1],
        n_qubits=6,
        n_layers=3,
        encoding='iqp'
    )
    model.train(X_train, y_train, epochs=150, lr=0.05)
    shap_explainer = QuantumSHAPExplainer(model, X_train, n_samples=100)
    gradient_explainer = QuantumGradientExplainer(model)
    explanations = []
    for i in range(5):
        shap_exp = shap_explainer.explain(X_test, i)
        grad_exp = gradient_explainer.explain(X_test, i)
        explanations.append((shap_exp, grad_exp))
    visualizer = QuantumXAIVisualizer()
    for i, (shap_exp, grad_exp) in enumerate(explanations):
        fig = visualizer.plot_explanation_comparison(
            [shap_exp, grad_exp],
            feature_names=feature_names[:len(shap_exp.feature_importance)],
            title=f"Sample {i} Explanation Comparison"
        )
        plt.show()
    print("\n\nRunning Benchmarking Example...")
    benchmark = QuantumXAIBenchmark(model, X_test, y_test, feature_names)
    for i in range(3):
        explanation = shap_explainer.explain(X_test, i)
        quality_metrics = benchmark.evaluate_explanation_quality(explanation, i)
        print(f"\nSample {i} Explanation Quality:")
        for metric, value in quality_metrics.items():
            print(f"  {metric}: {value:.4f}")
    print("\n" + "="*80)
    print("ALL EXAMPLES COMPLETED SUCCESSFULLY!")
    print("="*80)

# ============================================================================

if __name__ == "__main__":
    import numpy as np
    import warnings
    np.random.seed(42)
    warnings.filterwarnings('ignore')
    main()
