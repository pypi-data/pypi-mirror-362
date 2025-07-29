from setuptools import setup, find_packages

setup(
    name="q1ram",  # Use hyphen for PyPI
    version="0.1.4",
    description="Q1RAM Python client for interacting with the Quantum RAM API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Ahmed Eisa",
    author_email="ahmed.m.easa@gmail.com",
    url="https://github.com/yourusername/q1ram-client",  # optional
    packages=find_packages(),
    install_requires=[
        "requests",
        "python-dotenv", 
        "qiskit>=2.0.0",
        "requests",
        "qiskit_qasm3_import",
        "pylatexenc",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
