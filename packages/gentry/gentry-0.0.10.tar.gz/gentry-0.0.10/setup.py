from setuptools import setup

from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="gentry",
    version="0.0.10",
    description="Generic tree with visitors and nice markdown/mermaid representation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://varkenvarken.github.io/gentrypy/",
    author="varkenvarken",
    author_email="test@example.com",
    license="GPLv3",
    packages=["gentry"],
    python_requires=">=3.11",
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
