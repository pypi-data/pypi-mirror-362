#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
  name="termr",
  version="1.2.0",
  description="Terminal-based radio player with TUI",
  author="Sebastian Westberg",
  author_email="sebastian@westberg.io",
  url="https://github.com/Hibbins/termr",
  license="MIT",
  packages=find_packages(),
  include_package_data=True,
  install_requires=[
    "textual",
    "requests",
    "rich",
  ],
  python_requires=">=3.10",
  entry_points={
    "console_scripts": [
      "termr = termr.main:main"
    ]
  },
)
