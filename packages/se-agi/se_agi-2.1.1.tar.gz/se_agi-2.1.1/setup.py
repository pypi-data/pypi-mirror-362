#!/usr/bin/env python3
"""
SE-AGI: Self-Evolving General AI System
The Holy Grail of Autonomous Intelligence

A modular, agent-based AI system capable of:
- Meta-learning and self-improvement
- Multi-modal reasoning and adaptation
- Autonomous goal formulation and execution
- Continuous capability evolution
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="se-agi",
    version="2.1.1",
    author="SE-AGI Research Team",
    author_email="bajpaikrishna715@gmail.com",
    description="Self-Evolving General AI: The Holy Grail of Autonomous Intelligence",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/krish567366/se-agi",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
            "flake8>=6.0.0",
        ],
        "vision": [
            "opencv-python>=4.8.0",
            "pillow>=10.0.0",
            "transformers[vision]>=4.30.0",
        ],
        "audio": [
            "librosa>=0.10.0",
            "soundfile>=0.12.0",
            "whisper>=1.0.0",
        ],
        "simulation": [
            "gymnasium>=0.29.0",
            "pybullet>=3.2.5",
            "mujoco>=2.3.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "se-agi=se_agi.cli:main",
            "se-agi-train=se_agi.training.cli:main",
            "se-agi-evolve=se_agi.evolution.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "se_agi": ["configs/*.yaml", "prompts/*.txt", "schemas/*.json"],
    },
)
