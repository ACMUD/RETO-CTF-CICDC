import sys
import os

if not os.path.exists("$HOME/backup"):
    os.makedirs("$HOME/backup", exist_ok=True)

args = sys.argv[1:]
if len(args) == 0:
    print("No arguments provided.")

file = args[0]
try:
    os.system(f"cp -r {file} $HOME/backup")
except Exception as e:
    print(f"Error copying file: {e}")
    sys.exit(1)