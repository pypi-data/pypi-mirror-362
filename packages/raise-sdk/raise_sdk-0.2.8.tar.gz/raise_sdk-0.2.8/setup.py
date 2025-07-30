from setuptools import setup, find_packages

def get_version():
    with open("raise_sdk/__init__.py") as f:
        for line in f:
            if line.startswith("__version__"):
                return line.split("=")[-1].strip().strip('"')
    return "0.0.0"

setup(
    name         = "raise_sdk",
    version      = get_version(),
    author       = "RAISE",
    author_email = "info@raise-science.eu",
    description  = "RAISE Software Development Kit",
    long_description              = open("README.md").read(),
    long_description_content_type = "text/markdown",
    url          = "https://repo.raise-science.eu/raise_dev/raise-sdk",
    packages     = find_packages(),
    classifiers  = [
        "Programming Language :: Python :: 3",     # Python Version: Specifies the versions of Python your package supports
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",  # License: Must match the license you are using
        "Operating System :: OS Independent",      # Operating System: Use Operating System :: OS Independent unless your package is platform-specific
        "Development Status :: 4 - Beta",          # Ranges from 1 - Planning to 6 - Mature. For most initial releases, use 4 - Beta or 3 - Alpha
        # Audience/Topic: Optional but useful for indicating who the package is for and what it does
    ],
    # The python_requires argument specifies the minimum and maximum Python versions your package supports.
    # This helps users know if the package is compatible with their environment.
    # It restricts installation on unsupported Python versions, while classifiers only provide metadata.
    python_requires  = ">=3.8, <4",
    # The install_requires argument lists the dependencies your package requires to work.
    # When a user installs your package, pip will also install the listed dependencies if they aren't already present.
    # --> install_requires is for runtime dependencies
    # --> requirements.txt typically includes all dependencies, including runtime, testing, and development dependencies
    install_requires = [
        "docker==7.1.0",
        "minio==7.1.0",
        "PyQt5",
        "ruff>=0.12.2",
        "flake8>=7.3.0",
        "pre-commit>=4.2.0"
    ],
    extras_require={
        'test': [
            'pytest>=6.0',
        ],
    },
    entry_points={
        "flake8.extension": [
            "RCP01 = raise_sdk.code_checker.flake8.plugin:HardcodedDatasetIDChecker",
            "RCP02 = raise_sdk.code_checker.flake8.plugin:PathSeparatorChecker",
        ],
    },
    include_package_data = True,  # Ensure that any data files are included
)