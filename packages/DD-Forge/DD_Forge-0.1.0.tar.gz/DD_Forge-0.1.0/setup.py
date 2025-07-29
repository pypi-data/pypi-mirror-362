import pathlib
from setuptools import setup, find_packages

requirements = pathlib.Path("requirements.txt").read_text().splitlines()

setup(
    name='DD_Forge',
    version='0.1.0',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        requirements
        # Add other dependencies here
    ],
    entry_points={
        'console_scripts': [
            'run-DD_Forge = DD_Forge.__init__:main',
        ],
    },
)
