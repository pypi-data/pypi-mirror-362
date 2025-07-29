# Boring Math Library - Pythagorean triples

Package containing a class to generate Pythagorean triples along
with a CLI executable.

## Repos and Documentation

### Repositories

- [bm.pythagorean-triples][1] project on *PyPI*
- [Source code][2] on *GitHub*

### Detailed documentation

- [Detailed API documentation][3] on *GH-Pages*

## Overview

Geometrically, a *Pythagorean* triangle is a right triangle with
positive integer sides.

This project is part of the [Boring Math][4] **bm.** namespace project.

### Library modules

#### Pythagorean Triple Class

- Pythagorean Triple Class
  - Method `Pythag3.triples(a_start: int, a_max: int, max: Optional[int]) -> Iterator[int]`
    - Returns an iterator of tuples of primitive *Pythagorean* triples
  - A Pythagorean triple is a tuple in positive integers (a, b, c)
    - such that `a² + b² = c²`
    - `a, b, c` represent integer sides of a right triangle
    - a *Pythagorean* triple is primitive if gcd of `a, b, c` is `1`
  - Iterator finds all primitive Pythagorean Triples
    - where `0 < a_start <= a < b < c <= max` where `a <= a_max`
    - if `max` not given, find all theoretically possible triples with `a <= a_max`

______________________________________________________________________

### CLI Applications

- program [pythag3](#cli-program-pythag3)

These programs are implemented in an OS and package
build tool independent way via the `project.scripts` section of
`pyproject.toml`.

#### CLI program pythag3

- Generates primitive Pythagorean triples
- **Usage:** `pythag3 [m [n [max]]`
  - 3 args print all triples with `m <= a <= n` and `a < b < c <= max`
  - 2 args print all theoretically possible triples with `m <= a <= n`
  - 1 arg prints all theoretically possible triples with `a <= m`
  - 0 args print all triples with `3 <= a <= 100`

______________________________________________________________________

[1]: https://pypi.org/project/bm.pythagorean-triples/
[2]: https://github.com/grscheller/bm-pythagorean-triples/
[3]: https://grscheller.github.io/boring-math-docs/pythagorean-triples/
[4]: https://github.com/grscheller/boring-math-docs
