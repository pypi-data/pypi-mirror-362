# Copyright 2023-2025 Geoffrey R. Scheller
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Programs to generate Pythagorean Triples
========================================

Program **pythag3**  outputs lists of primitive triples

"""

from __future__ import annotations

import sys
from bm.pythagorean_triples.pythag3 import Pythag3


def pythag3_cli() -> None:
    """Prints tuples of primitive Pythagorean triples

    - Pythagorean triples are three integers ``a, b, c`` where ``a² + b² = c²``
    - such a triple is primitive when ``a,b,c > 0`` and ``gcd(a,b,c) = 1``
    - geometrically ``a, b, c`` represent the sides of a right triangle

    Usage: ``pythag3 [m [n [max]]]``

    +-----------+---------------------------------------------------+
    | # of args | Prints all possible triples (a, b, c) satisfying  |
    +===========+===================================================+
    |     3     |  m <= a <= n and a,b,c <= max                     |
    |     2     |  m <= a <= n                                      |
    |     1     |  a <= m                                           |
    |     0     |  3 <= a <= 100                                    |
    +-----------+---------------------------------------------------+

    """
    pythag3 = Pythag3()

    args = sys.argv[1:]

    if len(args) > 2:
        pythagTriples = pythag3.triples(
            a_start=int(args[0]), a_max=int(args[1]), max=int(args[2])
        )
    elif len(args) == 2:
        pythagTriples = pythag3.triples(a_start=int(args[0]), a_max=int(args[1]))
    elif len(args) == 1:
        pythagTriples = pythag3.triples(a_start=3, a_max=int(args[0]))
    else:
        pythagTriples = pythag3.triples(a_start=3, a_max=100)

    # Print out Pythagorean Triples
    for triple in pythagTriples:
        print(triple)
