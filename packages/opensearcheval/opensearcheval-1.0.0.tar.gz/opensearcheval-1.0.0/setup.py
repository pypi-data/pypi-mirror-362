"""
Setup configuration for OpenSearchEval
"""
import os
from setuptools import setup, find_packages

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# Read version from __init__.py
def get_version():
    with open(os.path.join(this_directory, "opensearcheval", "__init__.py")) as f:
        for line in f:
            if line.startswith("__version__"):
                return line.split("=")[1].strip().strip('"').strip("'")
    return "1.0.0"

# Production dependencies
install_requires = [
    # Core dependencies
    "pydantic>=2.4.0",
    "pydantic-settings>=2.0.0",
    "python-dotenv>=1.0.0",
    
    # Web framework
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.23.2",
    "httpx>=0.24.0",
    "aiofiles>=23.0.0",
    
    # Data processing
    "pandas>=2.0.0",
    "numpy>=1.24.0",
    "scikit-learn>=1.3.0",
    "scipy>=1.10.0",
    
    # MLX for Apple Silicon optimization
    "mlx>=0.0.5",
    
    # Visualization
    "matplotlib>=3.7.0",
    "seaborn>=0.12.0",
    "plotly>=5.14.0",
    
    # Database
    "sqlalchemy>=2.0.0",
    "alembic>=1.12.0",
    
    # Big data processing
    "pyspark>=3.4.0",
    
    # Web UI
    "flask>=2.3.0",
    "flask-cors>=4.0.0",
    "dash>=2.11.0",
    "dash-bootstrap-components>=1.4.0",
    
    # Async support
    "asyncio-mqtt>=0.11.0",
    
    # Configuration
    "click>=8.0.0",
    "rich>=13.0.0",
    "typer>=0.9.0",
    
    # Caching
    "redis>=4.5.0",
    
    # Monitoring
    "prometheus-client>=0.17.0",
    "psutil>=5.9.0",
    
    # ML/LLM
    "transformers>=4.30.0",
    "torch>=2.0.0",
    "openai>=1.0.0",
    
    # Date/time
    "python-dateutil>=2.8.0",
    
    # Security
    "cryptography>=41.0.0",
    "passlib>=1.7.4",
    "python-jose[cryptography]>=3.3.0",
    
    # File handling
    "openpyxl>=3.1.0",
    "xlsxwriter>=3.1.0",
    
    # JSON handling
    "orjson>=3.9.0",
    
    # Logging
    "structlog>=23.0.0",
]

# Development dependencies
extras_require = {
    "dev": [
        # Testing
        "pytest>=7.4.0",
        "pytest-asyncio>=0.21.0",
        "pytest-cov>=4.1.0",
        "pytest-mock>=3.11.0",
        "pytest-xdist>=3.3.0",
        "coverage>=7.2.0",
        "factory-boy>=3.3.0",
        
        # Code quality
        "black>=23.3.0",
        "isort>=5.12.0",
        "flake8>=6.0.0",
        "mypy>=1.3.0",
        "pre-commit>=3.3.0",
        "bandit>=1.7.5",
        
        # Documentation
        "sphinx>=7.0.0",
        "sphinx-rtd-theme>=1.2.0",
        "sphinx-autodoc-typehints>=1.23.0",
        "myst-parser>=2.0.0",
        
        # Jupyter
        "jupyter>=1.0.0",
        "ipykernel>=6.25.0",
        "notebook>=6.5.0",
        
        # Performance profiling
        "memory-profiler>=0.61.0",
        "line-profiler>=4.0.0",
        
        # Development tools
        "watchdog>=3.0.0",
        "python-dotenv>=1.0.0",
    ],
    
    "gpu": [
        # GPU acceleration
        "torch[cuda]>=2.0.0",
        "tensorflow-gpu>=2.13.0",
        "cupy-cuda12x>=12.0.0",
    ],
    
    "spark": [
        # Extended Spark support
        "pyspark[sql]>=3.4.0",
        "delta-spark>=2.4.0",
        "koalas>=1.8.0",
    ],
    
    "all": [
        # All optional dependencies
        "torch[cuda]>=2.0.0",
        "tensorflow-gpu>=2.13.0",
        "pyspark[sql]>=3.4.0",
        "delta-spark>=2.4.0",
        "koalas>=1.8.0",
        "cupy-cuda12x>=12.0.0",
    ]
}

# Entry points for CLI
entry_points = {
    "console_scripts": [
        "opensearcheval=opensearcheval.cli:main",
        "ose=opensearcheval.cli:main",
        "opensearcheval-api=opensearcheval.api.main:main",
        "opensearcheval-ui=opensearcheval.ui.app:main",
    ],
}

setup(
    name="opensearcheval",
    version=get_version(),
    author="Nik Jois",
    author_email="nikjois@llamasearch.ai",
    description="A comprehensive search evaluation platform with agent architecture and MLX integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/llamasearchai/OpenSearchEval",
    project_urls={
        "Bug Tracker": "https://github.com/llamasearchai/OpenSearchEval/issues",
        "Documentation": "https://opensearcheval.readthedocs.io/",
        "Source Code": "https://github.com/llamasearchai/OpenSearchEval",
        "Changelog": "https://github.com/llamasearchai/OpenSearchEval/blob/main/CHANGELOG.md",
    },
    packages=find_packages(exclude=["tests*", "docs*", "examples*"]),
    include_package_data=True,
    package_data={
        "opensearcheval": [
            "ui/static/**/*",
            "ui/templates/**/*",
            "data/**/*",
            "models/**/*",
            "*.json",
            "*.yaml",
            "*.yml",
        ],
    },
    install_requires=install_requires,
    extras_require=extras_require,
    entry_points=entry_points,
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Database :: Database Engines/Servers",
        "Typing :: Typed",
    ],
    keywords=[
        "search",
        "evaluation",
        "a/b testing",
        "mlx",
        "llm",
        "machine learning",
        "information retrieval",
        "search quality",
        "metrics",
        "analytics",
        "experiment",
        "ranking",
        "click-through rate",
        "precision",
        "recall",
        "ndcg",
        "mrr",
        "agent architecture",
        "fastapi",
        "dashboard",
        "visualization",
    ],
    license="MIT",
    zip_safe=False,
    platforms=["any"],
    test_suite="tests",
    
    # Metadata for PyPI
    maintainer="Nik Jois",
    maintainer_email="nikjois@llamasearch.ai",
    
    # Build configuration
    options={
        "build_ext": {
            "inplace": True,
        },
        "bdist_wheel": {
            "universal": False,
        },
    },
    
    # Data files for configuration
    data_files=[
        ("config", ["opensearcheval/config/default.yaml"]),
    ] if os.path.exists("opensearcheval/config/default.yaml") else [],
)