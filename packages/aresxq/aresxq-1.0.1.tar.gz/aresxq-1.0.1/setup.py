from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="aresxq",
    version="1.0.1",  # <-- bump version from 1.0.0
    author="Joaquin Martinez",
    author_email="your@email.com",  # optional
    description="ARES-X/Q: Quantum-safe encryption with ARX cipher, Kyber-style KEM, and AEAD",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fb6si15/aresxq",
    license="MIT",
    packages=find_packages(),
    install_requires=["pycryptodome"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Security :: Cryptography",
    ],
    python_requires=">=3.7",
)

