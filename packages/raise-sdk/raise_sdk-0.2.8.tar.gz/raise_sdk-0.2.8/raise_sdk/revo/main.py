#%%
# ================================== IMPORTS ==================================
# Stdlib imports
import sys
from time import time
from datetime import timedelta

# Imports from your apps
from raise_sdk import code_checker
from .LocalCodeRunner import LocalCodeRunner
from raise_sdk.utils.ui_dialogs import select_files, show_popup
# =============================================================================

#%%
# ================================= PARAMETERS ================================

# =============================================================================

#%%
# ================================== CLASSES ==================================

# =============================================================================

#%%
# ================================= FUNCTIONS =================================
def processing_script_execution(
                                 script               = None,
                                 requirements         = None,
                                 dataset              = None,
                                 programming_language = "python",
                                 version              = "3.11",
                                 quality_check        = False,
                                ):
    """
    Orchestrates the execution of a processing script, with or without Docker, based on user input and system configuration.

    This function performs the following steps:
    1. Prompts the user to select necessary input files (script(s), requirements, and dataset(s)) if missing.
    2. If `quality_check` is True, runs a code quality check (with either Ruff or Flake8) on the provided script(s) and exits on failure.
    2. Initializes the `LocalCodeRunner` class with the selected files and the Docker image configuration parameters.
    3. Checks the connection to the Docker daemon and handles the user's response if Docker is unavailable.
    4. Prepares the environment for running the experiment, including setting up the experiment path and building the Docker image if Docker is available.
    5. Executes the experiment either within a Docker container (using the provided programming language and version for the image)
       or as a regular Python script using the local system configuration.
    6. Logs the execution time and status of the experiment.
    7. Verifies the experiment results.
    8. Cleans up resources by removing the Docker image (if used) and any temporary files created during the execution.

    Parameters:
        script (list of str, optional): A list of paths to the script file(s). If not provided, the user will be prompted to select it.
        requirements (list of str, optional): A list of paths to the `requirements.txt` file(s). If not provided, the user will be prompted to select it.
        dataset (list of str, optional): A list of paths to the dataset file(s). If not provided, the user will be prompted to select it.
        programming_language (str, optional): The programming language used to create the Docker image.
        version (str, optional): The version of the programming language or runtime to be used in the Docker image.
        quality_check (bool, optional): Whether to run a code quality check (using `raise_sdk.code_checker`). Defaults to False.

    Raises:
        SystemExit:
            - If Docker is unavailable and the user opts not to proceed with local execution.
            - If the quality check fails (exit code from the code checker).
    
    Notes:
        - If `quality_check` is enabled, failure in the static analysis tool will halt execution early.
        - The experiment can be run either inside a Docker container or as a regular Python script, depending on the availability of Docker.
            - When Docker is unavailable, the experiment will run using the local system configuration.
        - The execution time and status of the experiment are logged.
        - Temporary files and Docker images (if used) are cleaned up after the experiment finishes.
    """

    # Input selection (only if parameters are not provided)
    if script is None:
        script = select_files(
            title     = "Select the script(s) --- NOTE: the main file that will be executed must be named `main.*`",
            filetypes = [("All Files", "*.*")],
        )
    if requirements is None:
        requirements = select_files(
            title     = "Select the requirements file(s)",
            filetypes = [("Text Files", "*.txt"), ("JSON Files", "*.json")],
        )
    if dataset is None:
        dataset = select_files(
            title     = "Select the dataset file(s)",
            filetypes = [("All Files", "*.*")],
        )

    # Check script(s) content
    if quality_check is True:
        print("################### raise_sdk.code_checker - INFO - Running RAISE Code Quality Check...")
        try:
            code_checker.start(paths=script, tool="flake8")
        except Exception as e:
            print("################### raise_sdk.code_checker - ERROR - Quality Check not passed. Exiting.")
            sys.exit(e.returncode)
        else:
            print("################### raise_sdk.code_checker - INFO - Quality Check passed.")

    # Create the CodeRunner class
    code_runner = LocalCodeRunner(
                                   script               = script,
                                   requirements         = requirements,
                                   dataset              = dataset,
                                   programming_language = programming_language,
                                   version              = version,
                                  )
    
    # Check the connection to the Docker daemon

    if code_runner.docker_client is None:
        response = show_popup(
            title="Docker Connection Failed",
            message="Failed to connect to the Docker daemon. Do you want to proceed without Docker?")
        if response == True:
            # Proceed without Docker and execute the experiment as a standard Python script
            pass
        else:
            # Ending the execution without further steps
            code_runner.logger.error("Experiment could not be executed.")
            code_runner.status_code = 2
            raise SystemExit("Execution halted: User opted not to proceed without Docker.")

    # Prepare the experiment path that contains the files needed for running the code
    code_runner.prepare_experiment_path()
    
    if code_runner.docker_client is not None:
        # Build docker image for experiment
        code_runner.build_docker_image()
    
    # Execute the processing script
    start_time = time()
    if code_runner.docker_client is not None:
        # Run the experiment with docker
        code_runner.run_docker_container()
    elif code_runner.docker_client is not None and programming_language == "python":
        # Run the experiment without docker
        code_runner.run_python()
    else:
        raise SystemExit("Execution halted: Currently running without Docker is only supported with Python.")
    end_time   = time()
    duration   = timedelta(seconds=(end_time-start_time))
    code_runner.logger.info(f' Experiment results:\n\t- Execution time: {duration}\n\t- Status code: {code_runner.status_code}')

    # Check results
    code_runner.check_results()
    
    if code_runner.docker_client is not None:
        # Remove docker image
        code_runner.remove_image()

    # Remove no longer useful files
    # code_runner.clean_experiment_path()
# =============================================================================

#%%
# ==================================== MAIN ===================================

# =============================================================================