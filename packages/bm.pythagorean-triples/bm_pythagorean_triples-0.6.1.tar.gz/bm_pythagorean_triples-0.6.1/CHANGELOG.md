# CHANGELOG

PyPI bm.pythagorean-triples project.

## Semantic Versioning

Strict 3 digit semantic versioning.

- **MAJOR** version incremented for incompatible API changes
- **MINOR** version incremented for backward compatible added functionality
- **PATCH** version incremented for backward compatible bug fixes

See [Semantic Versioning 2.0.0](https://semver.org).

## Releases and other important milestones

### Version 0.6.1 - PyPI release date 2025-07-14

- Fixed munged CHANGELOG and Documentation links for PyPI

### Version 0.6.0 - PyPI release date 2025-07-14

- First version to use pythonic_fp namespace
- no longer using dtools namespace packages

### Version 0.5.0 - PyPI release date 2025-01-18

- First PyPI release as bm.pythagorean-triples

### Version 0.4.7 - PyPI release date 2024-11-18

- Some minor additions
- consistency changes across all grscheller namespace PyPI repos

### Version 0.2.1.0 - commit date 2024-02-27

- Updated pythag3 cli script to provide more functionality
- docstring and README.md improvements

### Version 0.2.0.0 - commit date 2024-02-21

- All implementations going forward for integer_math module will use
  just integer based algorithms. I can't really compete with C based
  code from the Python standard library. The algorithms will then be
  of use if ported to a platform without floating point arithmetic.
- added two new functions to the integer_math module
  - iSqrt() finds the int square root of an int
    - does same thing as math.isqrt()
  - isSqr() return true if integer argument is a perfect square
- changed integer_math pythag3() function into a class method
  - pythag3() -> Pythag3.triples()
  - preliminary steps
  - fould unrelated tweak to increase speed by 2X
  - removed use of floating point numbers

### Version 0.1.0 - PyPI release date 2024-01-17

- initial PyPI grscheller.boring-math release
- updated pyproject.toml to align with grscheller.datastructures

### Version 0.0.9 - commit date 2024-01-14

- changed project's name from boring_math to boring-math
- both GitHub repo and future PyPI repo
- more in alignment with what I see on PyPI
- project is grscheller.boring-math
- package is still grscheller.boring_math

### Version 0.0.8 - commit date 2024-01-14

- working on pyproject.toml infrastructure for PyPI releases
- will use Flit as the packaging/publishing tool
- replaced bin/ scripts with `boring_math.integer_math_cli` entry-points

### Version 0.0.4 - commit date 2024-01-10

- first coding changes in years!
- gh-pages configured

### Version 0.0.0.3 - commit date 2023-12-06

- added pyproject.toml

### Version 0.0.0.2 - commit date 2023-12-06

- got package working again
  - did not understand iterators that well when I first wrote this package
- replaced my `take` with `itertools.islice`
- generated docs from docstrings with pdoc3

### Version 0.0.0.1 - commit date 2023-12-06

- fixed Markdown issues with first commit
- Added .gitignore file to anticipate pytest & __pycache__ directories

### Version 0.0.0.0 - commit date 2023-12-06

- first commit of source code with with the old pipfile build
  infrastructure removed.
