#%%
# ================================== IMPORTS ==================================
import sys
from .ruff import run as run_ruff
from .ruff import RuffCheckError
from .flake8 import run as run_flake8
from .flake8 import FlakeCheckError
# =============================================================================

#%%
# ================================= PARAMETERS ================================

# =============================================================================

#%%
# ================================== CLASSES ==================================

# =============================================================================

#%%
# ================================= FUNCTIONS =================================
def code_check(
        paths,
        tool        : str  = "flake8",
        config_file : str  = None,
        extra_args  : list = None,
    ):
    """
    Run quality checks on the given files or directories.

    Depending on `tool`, this will either run Ruff or Flake8.

    Args:
        paths (str or List[str]):
            One or more file or directory paths to check.
        tool (str): 
            Which checker to use. Must be either "ruff" or "flake8".  
            Defaults to "flake8".
        config_file (str, optional): 
            Path to a configuration file (e.g. pyproject.toml for Ruff, setup.cfg
            or .flake8 for Flake8).
        extra_args (List[str], optional): 
            Additional arguments passed to Ruff or Flake8.

    Raises:
        SystemExit: 
            Exits with the tool's return code if any issues are found.
        ValueError: 
            If `tool` is not one of "ruff" or "flake8".
    """
    try:
        if tool == "ruff":
            output = run_ruff(
                paths       = paths,
                config_file = config_file,
                args        = extra_args,
            )
            print("Ruff passed with no issues\n")
            print(output)
        elif tool == "flake8":
            output = run_flake8(
                paths       = paths,
                config_file = config_file,
                args        = extra_args,
            )
            print("Flake8 passed with no issues\n")
            print(output)
        else:
            raise ValueError(f"Unknown tool: {tool!r}. Expected 'ruff' or 'flake8'.")
    # Print the lint errors and exit with non-zero status
    except RuffCheckError as e:
        print("Ruff found problems:\n", e.output, file=sys.stderr)
        raise e
    except FlakeCheckError as e:
        print("Flake8 found problems:\n", e.output, file=sys.stderr)
        raise e
# =============================================================================

#%%
# ==================================== MAIN ===================================

# =============================================================================