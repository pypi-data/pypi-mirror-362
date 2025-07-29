import sys
import os

# Add the root directory to sys.path so autopylog is found
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from autopylog import log_this

@log_this
def add(x, y):
    return x + y

@log_this
def divide(a, b):
    return a / b

if __name__ == "__main__":
    print("Add Output:", add(3, 4))
    try:
        divide(10, 0)
    except:
        pass
