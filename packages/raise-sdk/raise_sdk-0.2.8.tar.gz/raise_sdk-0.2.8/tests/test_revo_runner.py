import os
import shutil
import time
from pathlib import Path

# --- Dummy Docker Client for testing remove_image ---
class DummyDockerClient:
    class Images:
        def remove(self, image):
            # Simulate successful image removal.
            return True
    images = Images()
    # For run_docker_container tests, you could add dummy methods if needed.
    def containers(self):
        pass

# ===============================================================
# ---------- Tests for LocalCodeRunner functionalities ----------
# ===============================================================

def test_prepare_experiment_path(local_runner):
    """
    Verify that prepare_experiment_path creates the proper experiment folder structure
    and copies the input files into the experiment directory.
    """
    local_runner.prepare_experiment_path()
    
    experiment_path = Path(local_runner.experiment_path)
    # Check that the experiment directory exists.
    assert experiment_path.exists(), "Experiment folder was not created."
    
    # Check that logs and results directories were created.
    assert (experiment_path / "logs").exists(), "Logs folder not created."
    assert (experiment_path / "results").exists(), "Results folder not created."
    
    # For each type of input file, ensure a copy exists in the experiment directory.
    for file_list in [local_runner.cfg["script_path"], local_runner.cfg["requirements_path"], local_runner.cfg["dataset_path"]]:
        for file_path in file_list:
            filename = os.path.basename(file_path)
            dest_file = experiment_path / filename
            assert dest_file.exists(), f"File {filename} was not copied to the experiment path."
            # Optionally, check that the contents match.
            with open(file_path, "r") as src, open(dest_file, "r") as dst:
                assert src.read() == dst.read(), f"Contents of {filename} do not match."

def test_check_results_empty(local_runner):
    """
    Verify that check_results sets the status code to 1 when the results folder is empty.
    """
    # Prepare the experiment path so that the logs and results folders exist.
    local_runner.prepare_experiment_path()
    results_path = Path(local_runner.results_path)
    
    # Ensure the results directory is empty.
    for item in results_path.iterdir():
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            shutil.rmtree(item)
    
    local_runner.check_results()
    # Expect status_code 1 when no result files are present.
    assert local_runner.status_code == 1, "Expected status code 1 when results folder is empty."

def test_remove_image(local_runner, monkeypatch):
    """
    Test remove_image by assigning a dummy Docker client that simulates image removal.
    """
    # Create a dummy Docker client and assign it.
    dummy_docker = DummyDockerClient()
    local_runner.docker_client = dummy_docker
    
    # Patch time.sleep to avoid delay in the test.
    monkeypatch.setattr(time, "sleep", lambda x: None)
    
    # Call remove_image and verify that it returns True.
    result = local_runner.remove_image()
    assert result is True, "remove_image did not return True on successful removal."