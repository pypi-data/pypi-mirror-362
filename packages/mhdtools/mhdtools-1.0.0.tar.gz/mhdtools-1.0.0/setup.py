from setuptools import setup

install_requires = [
	"click",
	"matplotlib",
	"numpy",
	"scipy",
	"SimpleITK",
]

setup(
	name="mhdtools",
	version="0.1.0",
	description="Tools to manipulate MHD/RAW files",
	url="https://github.com/alexis-pereda/mhdtools",
	author="Alexis Pereda",
	author_email="alexis@pereda.fr",
	license="",
	packages=["mhdtools"],
	install_requires=install_requires,
)
