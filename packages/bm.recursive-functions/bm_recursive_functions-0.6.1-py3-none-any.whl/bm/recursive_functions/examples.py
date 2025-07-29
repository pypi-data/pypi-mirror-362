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
Examples of recursive functions
===============================

Examples implementations for various recursive functions.

Ackermann function
------------------

Ackermann's function is an example of a function that is computable
but not primitively recursive. It quickly becomes computationally
intractable for relatively small values of m.

Ackermann function is defined recursively by

- ``ackermann(0,n)=n+1                               for n >= 0``
- ``ackermann(m,0)=ackermann(m-1,1)                  for m >= 0``
- ``ackermann(m,n)=ackermann(m-1, ackermann(m,n-1))  for m,n > 0``

Fibonacci sequences
-------------------

The Fibonacci sequence is usually taught in grade school as the
first recursive function that is not either an arithmetic or geometric
sequence.

    The Fibonacci sequence is traditionally defined as

    - ``f₁ = 1``
    - ``f₂ = 1``
    - ``fₙ₊₂ = fₙ₊₁ + fₙ``

    Actually, a Fibonacci extends can extend in both directions.

    - ..., 13, -8, 5, -3, 2, -1, 1, 0, 1, 1, 2, 3, 5, 6, 13, ...

"""

from __future__ import annotations

from collections.abc import Iterator

__all__ = ['ackermann_list', 'fibonacci_generator', 'rev_fibonacci_generator']


def ackermann_list(m: int, n: int) -> int:
    """Ackermann's Function.

    Evaluate Ackermann's function simulating recursion with a list.

    .. note::
        This implementation models the recursion with a Python list instead of Python's
        "call stack". It then evaluates the innermost ackermann function first. To
        naively use call stack recursion would result in the loss of stack safety.

    """
    acker = [m, n]

    while len(acker) > 1:
        mm, nn = acker[-2:]
        if mm < 1:
            acker[-1] = acker.pop() + 1
        elif nn < 1:
            acker[-2] = acker[-2] - 1
            acker[-1] = 1
        else:
            acker[-2] = mm - 1
            acker[-1] = mm
            acker.append(nn - 1)
    return acker[0]


def fibonacci_generator(fib0: int = 0, fib1: int = 1) -> Iterator[int]:
    """Fibonacci iterator.

    Generate a Fibonacci sequence instead of recursively evaluating it.

    - returns an iterator to a Fibonacci sequence
      - beginning fib0, fib1, fib0+fib1, ...
      - default yields 0, 1, 1. 2, 3, 5, 8, 13, ...

    """
    while True:
        yield fib0
        fib0, fib1 = fib1, fib0 + fib1


def rev_fibonacci_generator(fib0: int = 0, fib1: int = 1) -> Iterator[int]:
    """Reverse Fibonacci iterator.

    Generate a reverse Fibonacci sequence instead of recursively evaluating it.

    - Returns iterator iterating over the Fibonacci sequence in reverse order
      - beginning fib1, fib0, fib1-fib0, ...
      - default yields 1, -1, 2, -3, 5, -8, 13, ...

    """
    while True:
        fib0, fib1 = fib1, fib0 - fib1
        yield fib0
