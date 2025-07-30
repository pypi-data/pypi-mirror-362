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
class RuffCheckError(Exception):
    """Raised when Ruff reports errors or fails to run."""
    def __init__(self, returncode, output):
        super().__init__(f"Ruff exited with code {returncode}")
        self.returncode = returncode
        self.output = output
# =============================================================================

#%%
# ================================= FUNCTIONS =================================
# Ruff today is a zero‑plugin Python linter: everything you get comes "built‑in",
# and there isn't a public plugin API yet.
# https://docs.astral.sh/ruff/faq/
# https://github.com/astral-sh/ruff/discussions/8409
def run(paths, config_file=None, args=None):
    """
    Run Ruff linter on the given files or directories.

    Uses the `check` subcommand to explicitly invoke lint checks.

    Args:
        paths (List[str] or str): File or list of files/dirs to lint.
        config_file (str): Optional path to a Ruff config.
        args (List[str]): Additional ad-hoc arguments for Ruff.

    Returns:
        str: Combined stdout/stderr from Ruff.

    Raises:
        RuffCheckError: If Ruff exits non-zero.
    """
    if isinstance(paths, (str, Path)):
        paths = [str(paths)]

    # command definition
    cmd = [sys.executable, '-m', 'ruff', 'check']
    if config_file:
        cmd += ['--config', str(config_file)]
    if args:
        cmd += list(args)
    cmd += paths

    # process run
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = (result.stdout or '') + (result.stderr or '')
    if result.returncode != 0:
        raise RuffCheckError(result.returncode, output)
    return output
# =============================================================================

#%%
# ==================================== MAIN ===================================

# =============================================================================