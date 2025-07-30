#%%
# ================================== IMPORTS ==================================
import sys
import subprocess
from pathlib import Path
# =============================================================================

#%%
# ================================= PARAMETERS ================================

# =============================================================================

#%%
# ================================== CLASSES ==================================
class FlakeCheckError(Exception):
    """Raised when Flake8 reports errors or fails to run."""
    def __init__(self, returncode, output):
        super().__init__(f"Flake8 exited with code {returncode}")
        self.returncode = returncode
        self.output = output
# =============================================================================

#%%
# ================================= FUNCTIONS =================================
def run(paths, config_file=None, args=None):
    """
    Run Flake8 on the given files or directories.

    Args:
        paths (List[str] or str): File or list of files/dirs to lint.
        config_file (str): Optional path to a Falke8 config file (e.g. setup.cfg or .flake8).
        args (List[str]): Additional ad-hoc arguments for Flake8.

    Returns:
        str: Combined stdout/stderr from Flake8.

    Raises:
        FlakeCheckError: If Flake8 exits non-zero.
    """
    # Resolve default config if none provided: same dir as this file
    if config_file is None:
        # https://flake8.pycqa.org/en/latest/user/configuration.html
        # Flake8 supports storing its configuration in your project
        # in one of setup.cfg, tox.ini, or .flake8.
        config_file = Path(__file__).parent / 'flake8-config.ini'

    if isinstance(paths, (str, Path)):
        paths = [str(paths)]

    # command definition
    cmd = [sys.executable, '-m', 'flake8']
    if config_file:
        cmd += ['--config', str(config_file)]
    if args:
        cmd += list(args)
    cmd += paths

    # process run
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = (result.stdout or '') + (result.stderr or '')
    if result.returncode != 0:
        raise FlakeCheckError(result.returncode, output)
    return output
# =============================================================================

#%%
# ==================================== MAIN ===================================

# =============================================================================