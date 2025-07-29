from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="quantum_xai",
    version="0.1.1",
    description="Explainable Quantum Machine Learning Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Harsha P, B Manvitha Reddy",
    author_email="harshagowda2318@gmail.com, bmanvitha.reddy@example.com",
    url="https://github.com/Harsha2318/quantum_xai",
    py_modules=['quantum_xai'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pennylane",
        "numpy",
        "matplotlib",
        "seaborn",
        "scikit-learn",
        "pandas"
    ],
    include_package_data=True,
)
