from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in dox_frappe/__init__.py
from dox_frappe import __version__ as version

setup(
	name="dox_frappe",
	version=version,
	description="DOX app for improving frappe framework",
	author="Digital Box Agency",
	author_email="rng.bakraldubai@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
