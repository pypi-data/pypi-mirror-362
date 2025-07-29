[project]
name = "%%PROJECT_NAME%%"
version = "%%PROJECT_VERSION%%"
description = "%%PROJECT_DESCRIPTION%%"
readme = "README.md"
requires-python = ">=3.9"
authors = [
  { name = "%%USER_NAME%%", email = "%%USER_EMAIL%%" }
]
maintainers = [
  { name = "%%USER_NAME%%", email = "%%USER_EMAIL%%" }
]
classifiers = [
  "Topic :: Software Development :: Build Tools",
  "Development Status :: 3 - Alpha",
  "Programming Language :: Python :: 3",
  "Programming Language :: Python :: 3.9",
  "Programming Language :: Python :: 3.10",
  "Programming Language :: Python :: 3.11",
  "Programming Language :: Python :: 3.12",
  "Programming Language :: Python :: 3.13",
  "Operating System :: OS Independent",
  "Environment :: Console",
  "Intended Audience :: Developers",
  "Natural Language :: English",
  "Typing :: Typed",
]
license = "MIT"
license-files = ["LICENSE"]

[project.urls]
Homepage = "https://github.com/%%GITHUB_ORG%%/python-%%PROJECT_NAME%%"
Documentation = "https://github.com/%%GITHUB_ORG%%/python-%%PROJECT_NAME%%/blob/%%DEFAULT_BRANCH%%/README.md"
Repository = "https://github.com/%%GITHUB_ORG%%/python-%%PROJECT_NAME%%"
Issues = "https://github.com/%%GITHUB_ORG%%/python-%%PROJECT_NAME%%/issues"
Changelog = "https://github.com/%%GITHUB_ORG%%/python-%%PROJECT_NAME%%/blob/%%DEFAULT_BRANCH%%/CHANGELOG.md"

[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"
