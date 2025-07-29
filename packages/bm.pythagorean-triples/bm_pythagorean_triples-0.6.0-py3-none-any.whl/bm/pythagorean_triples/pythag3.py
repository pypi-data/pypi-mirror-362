# Copyright 2016-2025 Geoffrey R. Scheller
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
Pythagorean triples
===================

Pythagorean triples are three integers ``a, b, c``  where ``a² + b² = c²``.
Such a triple is primitive when ``a, b, c > 0`` and ``gcd(a, b, c) = 1``.
Geometrically, ``a, b, c`` represent the sides of a right triangle.

"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from bm.integer_math.num_theory import gcd, iSqrt

__all__ = ['Pythag3']


class Pythag3:
    """Pythagorean Triple Iterator Class.

    Supports the generation of primitive Pythagorean triples.

    """

    def __init__(self, last_square: int = 500, /):
        last_h = last_square if last_square % 2 == 1 else last_square - 1
        last_h = max(last_h, 5)

        # Perfect square lookup dictionary
        self.squares = {h * h: h for h in range(5, last_h + 1, 2)}
        self.last_h = last_h

    def extend_squares(self, last_to_square: int, /) -> None:
        """Extend the self.squares perfect square lookup table."""
        last_h = last_to_square if last_to_square % 2 == 1 else last_to_square - 1
        if last_h > self.last_h:
            for h in range(self.last_h + 2, last_h + 1, 2):
                self.squares[h * h] = h
            self.last_h = last_h

    @staticmethod
    def _cap_sides(
        a_max: int, abc_max: int | None = None, /
    ) -> tuple[int, Callable[[int], int], int]:
        def mk_caps(
            amax: int, cap: int | None
        ) -> tuple[int, Callable[[int], int], int]:
            a_cap = 2 if amax < 3 else amax

            def b_final(a: int) -> int:  # Theoretical max
                return (a**2 - 1) // 2

            b_cap = b_final

            if cap is not None:
                cap = 4 if cap < 5 else cap
                if cap < a_cap - 2:
                    a_cap = cap - 2

                def b_capped(a: int) -> int:
                    return min(b_final(a), iSqrt(cap**2 - a**2))

                b_cap = b_capped

            c_cap = iSqrt(a_cap**2 + b_cap(a_cap) ** 2) + 1

            return (a_cap, b_cap, c_cap)

        return mk_caps(a_max, abc_max)

    def triples(
        self, a_start: int = 3, a_max: int = 3, abc_max: int | None = None
    ) -> Iterator[tuple[int, int, int]]:
        """Returns an iterator of all possible primitive Pythagorean triples.

        - tuple ``(a, b, c)``

          - where ``a_start <= a <= a_max``
          - and ``0 < a < b < c < abc_max``

        - if ``abc_max`` not given, returns all theoretically possible triples

        """
        a_init = max(a_start, 3)
        a_cap, b_cap, c_cap = Pythag3._cap_sides(a_max, abc_max)
        self.extend_squares(c_cap)

        # Calculate Pythagorean triples
        for side_a in range(a_init, a_cap + 1):
            for side_b in range(side_a + 1, b_cap(side_a) + 1, 2):
                csq = side_a**2 + side_b**2
                if csq in self.squares:
                    if gcd(side_a, side_b) == 1:
                        yield side_a, side_b, self.squares[csq]
