import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "raise_sdk")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "raise_sdk", "revo")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "raise_sdk", "revo", "app")))

from pathlib import Path
import pytest
from raise_sdk.revo.LocalCodeRunner import LocalCodeRunner
from raise_sdk.utils.file_utils import find_local_paths

# ===============================================================
# --- Fixtures for setting up dummy files and runner instance ---
# ===============================================================
# In these tests we use pytest's temporary directory fixture (tmp_path) to avoid
# polluting your real filesystem and we "dummy‐patch" external dependencies (such
# as the docker connection and file lookup) so that our tests are self‑contained.

@pytest.fixture
def dummy_files(tmp_path):
    """
    Create dummy script, requirements, and dataset files in a temporary directory.
    Returns three lists (each containing one file path as a string).
    """
    script_file = tmp_path / "main.py"
    script_file.write_text("print('Hello from script')")
    
    req_file = tmp_path / "requirements.txt"
    req_file.write_text("package1==1.0")
    
    dataset_file = tmp_path / "datafile.csv"
    dataset_file.write_text("id,value\n1,100")
    
    return [str(script_file)], [str(req_file)], [str(dataset_file)]

@pytest.fixture
def local_runner(tmp_path, dummy_files, monkeypatch):
    """
    Instantiate a LocalCodeRunner with dummy file paths.
    Patch os.getcwd so that the experiment directory is created in tmp_path.
    Also, patch external dependencies like connect_with_docker and find_local_paths.
    """
    # Ensure that os.getcwd() returns our temporary directory.
    monkeypatch.setattr(os, "getcwd", lambda: str(tmp_path))
    
    """# Patch connect_with_docker to always return None (simulate no Docker available)
    monkeypatch.setattr(
        LocalCodeRunner,
        "connect_with_docker",
        lambda logger: None
    )"""

    # Patch find_local_paths to return a mapping from each file's Path to its basename
    def dummy_find_local_paths(paths):
        return {Path(p): os.path.basename(p) for p in paths}
    
    monkeypatch.setattr(
        "raise_sdk.utils.file_utils.find_local_paths",  # Correct patching path
        dummy_find_local_paths  # The mock function
    )
    
    script_paths, req_paths, dataset_paths = dummy_files
    # Instantiate LocalCodeRunner with our dummy file paths.
    runner = LocalCodeRunner(
        script               = script_paths,
        requirements         = req_paths,
        dataset              = dataset_paths,
        programming_language = "python",
        version              = "3.11",
    )
    return runner
