import os, re
from setuptools import setup

with open("ReadMe.md", encoding='utf-8') as f:
    mdstr = f.read()

def capture_sgfutil_readme(s):
    # Capture paragraph from the ReadMe.md
    first_paragraph = re.search('(?<=\n).*?library.*?(?=\n)', s).group()
    install_section = re.search('(?<=\n)## Install.*?(?=##)', s, re.DOTALL).group().strip()
    return '\n\n'.join(["# sgfutil", first_paragraph, install_section])
_long_description = capture_sgfutil_readme(mdstr)

# Main
setup(
    name = "sgfutil",
    version = '0.2.0-r4',
    packages = ['sgfutil'],
    include_package_data = True,
    install_requires = ["ply"],
    # Meta
    author = "wklchris",
    author_email="wklchris@hotmail.com",
    url = "https://github.com/wklchris/python-sgfutil",
    description = "An SGF utilization library for Go/chess game players.",
    long_description = _long_description,
    long_description_content_type = "text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)