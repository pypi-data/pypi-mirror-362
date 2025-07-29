from setuptools import setup, find_packages
from pathlib import Path

# read the long description from README.md
this_dir = Path(__file__).parent
long_description = (this_dir / "README.md").read_text(encoding="utf-8")

setup(
    name="speak2py",
    version="0.1.1",  # <-- bumped!
    description="MVP: Load CSV/Excel/JSON into a pandas DataFrame via speak2py()",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Varun Pulipati",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "pandas>=1.0.0",
        "matplotlib>=3.0.0",
        "google-genai>=0.5.0",  
    ],
    entry_points={
        "console_scripts": [
            "speak2py = speak2py.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
