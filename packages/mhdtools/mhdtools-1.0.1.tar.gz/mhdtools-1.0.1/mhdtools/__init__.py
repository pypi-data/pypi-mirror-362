import pathlib

root = pathlib.Path(__file__).parent.resolve()

__author__ = "Alexis Pereda"
with open(f"{root}/.pkginfo/version", "r") as f:
	__version__ = f.read().strip()
