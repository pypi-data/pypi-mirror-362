#%%
# ================================== IMPORTS ==================================
import ast
import re
# =============================================================================

#%%
# ================================= PARAMETERS ================================
# Pre‑compile a GUID pattern (matches typical UUID strings)
_GUID_RE = re.compile(
    r"\b[0-9a-fA-F]{8}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{12}\b"
)
# =============================================================================

#%%
# ================================== CLASSES ==================================
class HardcodedDatasetIDChecker:
    """
    RCP01: Disallow hard-coded dataset UUIDs in code.
    Instead, code should read from the RAISE_DATASET_ID_LIST environment variable.
    """
    name    = "hardcoded-dataset-id"
    version = "0.1.0"
    # Define a unique error code + message template
    _error_code    = "RCP01"
    _error_message = f"{_error_code} Found hard-coded dataset ID; use RAISE_DATASET_ID_LIST env var instead"

    def __init__(self, tree, filename=None):
        self.tree = tree

    def run(self):
        for node in ast.walk(self.tree):
            # look for literal string constants
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                text = node.value
                if _GUID_RE.search(text):
                    yield (
                        node.lineno,
                        node.col_offset,
                        self._error_message,
                        type(self),
                    )

class PathSeparatorChecker:
    """
    RCP02: Disallow literal Windows path separators in string literals.
    Paths should be built with os.path.join or os.path.sep (or pathlib).
    """
    name    = "path-separator-checker"
    version = "0.1.0"
    # Define a unique error code + message template
    _error_code    = "RCP02"
    _error_message = f"{_error_code} Found literal '\\\\' in path; use os.path.join or os.path.sep"

    def __init__(self, tree, filename=None):
        self.tree = tree

    def run(self):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                text = node.value
                # if there's a backslash (Windows sep) in the literal
                if "\\" in text:
                    yield (
                        node.lineno,
                        node.col_offset,
                        self._error_message,
                        type(self),
                    )
# =============================================================================

#%%
# ================================= FUNCTIONS =================================

# =============================================================================

#%%
# ==================================== MAIN ===================================

# =============================================================================