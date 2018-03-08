# http://docs.python-guide.org/en/latest/writing/structure/
import os
import sys

os.environ['PY_ENV'] = 'test'

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
