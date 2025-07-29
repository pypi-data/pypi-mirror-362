import pathlib
from setuptools import setup, find_packages
requirements = pathlib.Path("requirements.txt").read_text().splitlines()

setup(
    name="aider_rag",
    version="0.1.0",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        requirements
    ],
    entry_points={
        "console_scripts": [
            "aider-rag=aider_rag.cli:main"
        ]
    },
)
