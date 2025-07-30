
from setuptools import setup, find_packages

setup(
    name="aresxq",
    version="1.0.0",
    author="Joaquin Martinez",
    description="ARES-X/Q: A quantum-safe encryption library",
    packages=find_packages(),
    install_requires=[
        "pycryptodome"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
