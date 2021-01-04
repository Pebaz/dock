import sys
from pathlib import Path

args = sys.argv[1:]

if not args:
    print('Dock - Python documentation generator')
    print('Usage: dock (<module filename> | <package path>)')
    quit()

given_path = Path(args[0])

if not given_path.exists():
    print(f"{given_path} doesn't exist")
    quit()

if given_path.is_dir():
    package = given_path
    print(package)
else:
    module = given_path
    print(module)
