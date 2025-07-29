# utils.py

import sys

def is_in_virtualenv():
    """
    Checks if the current Python environment is a virtual environment.
    """
    return (hasattr(sys, 'prefix') and sys.prefix != sys.base_prefix) or \
           (hasattr(sys, 'real_prefix'))