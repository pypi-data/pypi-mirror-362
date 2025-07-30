from setuptools import setup, find_packages

setup(
    name='quantum_xai',
    version='0.1.2',
    description='Explainable Quantum Machine Learning Library',
    author='Quantum-XAI Contributors',
    author_email='harshagowda2318@gmail.com , manvithareddy3004@gmail.com',
    url='https://github.com/Harsha2318/QUANTUM-XAI-library',
    packages=find_packages(),
    install_requires=[
        'pennylane',
        'numpy',
        'matplotlib',
        'seaborn',
        'scikit-learn',
        'pandas',
        'qiskit'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
