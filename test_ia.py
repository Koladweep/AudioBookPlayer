import sys
import os
# Get the absolute path of the current script
current_path = os.path.dirname(os.path.abspath(__file__))

# Get the absolute path of the project root
project_root = os.path.dirname(current_path)

# Add the project root to sys.path
sys.path.append(project_root)
from .ABPlayer.drivers.librivox import LibriVox as lv
def main():
    query=''
    if '-q' in sys.argv:
        query=sys.argv[sys.argv.index('-q')+1]
        return(list(lv.search_books(query)))
    else:
        return None

