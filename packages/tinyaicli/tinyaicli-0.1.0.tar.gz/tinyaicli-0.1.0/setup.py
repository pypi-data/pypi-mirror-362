from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requirements = [
    "torch>=2.0.0",
    "torchvision>=0.15.0",
    "torchaudio>=2.0.0",
    "hydra-core>=1.3.0",
    "hydra-colorlog>=1.2.0",
    "wandb>=0.15.0",
    "omegaconf>=2.3.0",
    "datasets>=2.14.0",
    "transformers>=4.30.0",
    "tokenizers>=0.13.0",
    "numpy>=1.24.0",
    "pandas>=2.0.0",
    "matplotlib>=3.7.0",
    "seaborn>=0.12.0",
    "tqdm>=4.65.0",
    "pyyaml>=6.0",
    "click>=8.1.0",
    "rich>=13.0.0",
    "tensorboard>=2.13.0",
    "pillow>=10.0.0",
    "scikit-learn>=1.3.0",
    "accelerate>=0.20.0",
    "peft>=0.4.0",
    "bitsandbytes>=0.41.0",
]

setup(
    name="tinyaicli",
    version="0.1.0",
    author="Nathan Heinstein",
    author_email="nathan.heinstein@dal.ca",
    description="A CLI tool for training small LLMs and vision models with reproducible research",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nheinstein/tinyai",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "tinyai=tinyai.train:main",
        ],
    },
    include_package_data=True,
    package_data={
        "tinyai": ["configs/*.yaml"],
    },
) 