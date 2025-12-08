import sys
import os

"""
NOTE: run scripts like this: python -m scripts.[scriptname]
"""

# enables absolute imports from project modules
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


