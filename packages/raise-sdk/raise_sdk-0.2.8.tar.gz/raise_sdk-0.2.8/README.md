# RAISE SDK
A software development kit for interacting with the core functionalities of the RAISE project.
At the moment, it includes two submodules, `revo` (i.e. Remote Execution Validation Operations), `code_checker` (i.e. Code Quality Checker), and a `utils` folder.

- <b> REVO (Remote Execution Validation Operations) </b> <br>
  The REVO module is designed to implement the core functionalities of the RAI Processing Script Manager, enabling seamless execution and management of Python scripts for experiments. It is designed to automate key tasks such as managing dependencies, handling dataset selection, and running the main Python script, while also ensuring proper validation throughout the process. By integrating these features, REVO ensures that experiments are executed efficiently and with accurate logging, while validating the execution environment and providing detailed results for further analysis.

- <b> Code_checker (Code Quality Checker) </b> <br>
  A lightweight module to enforce code quality across your project through two interchangeable back‑ends:
  1. **Ruff**  
     A zero‑plugin, Rust‑powered linter—fast and batteries‑included.
  2. **Flake8**  
     The classic Python linter, with support for custom plugins. Ships with a built‑in default config (`flake8-config.ini`) under `raise_sdk/code_checker/flake8/`.
     - **Custom plugins**:
          - `RCP01` disallows hard‑coded UUIDs
          - `RCP02` disallows literal backslashes in paths
  <!---
  3. **Pre-commit**  
     Wraps your project's own `.pre-commit-config.yaml`, or falls back to the shipped one under `raise_sdk/code_checker/precommit/`.
     - **Git requirement**: must be run inside a Git repo with `pre-commit` installed in the environment
  -->

- <b> Utils </b> <br>
  The `utils/` folder serves as a collection of utility modules that provide reusable, convenient, and well-structured functions to simplify common tasks across the application. These modules are designed to handle tasks such as file and folder operations, user interactions, and system-level dialogs. Below is an overview of the provided utilities and their purpose.



## Installation
You can install `raise_sdk` directly from PyPI using pip:

```bash
pip install raise_sdk
```

## Usage Examples
Code examples demonstrating how to use the `raise_sdk` package are provided in the `examples` folder of the repository. You can explore these examples to understand how to utilize the functionality of the SDK in different scenarios.

To get started, check the `examples` folder for various scripts and notebooks, such as:
- **`run_experiment.ipynb`**: A Jupyter Notebook with step-by-step instructions for running the experiment interactively.

## Documentation
For more detailed documentation, please visit the official documentation (link). You can also check the source code and contribute via the GitHub repository (link).

## License
This project is licensed under the European Union Public License (EUPL) version 1.2. See the LICENSE file for more details.

##  Contributing
We welcome contributions! If you'd like to contribute, please fork the repository, make changes, and submit a pull request. Contributions are subject to the terms of the EUPL license.

## Contact
For any inquiries, feel free to reach out via the following email: info@raise-science.eu.