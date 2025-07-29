import os
import warnings

SHOW_DEPRECATION_WARNINGS = os.getenv("SHOW_DEPRECATION_WARNINGS")

if not bool(SHOW_DEPRECATION_WARNINGS):
    warnings.filterwarnings("ignore", category=DeprecationWarning)
