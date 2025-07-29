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
### Programs to evaluate Ackermann's function

.. note::
    The version of the Ackermann's function being used is defined recursively by

       ackermann(0,n) = n+1                                 for n >= 0
       ackermann(m,0) = ackermann(m-1,1)                    for m >= 0
       ackermann(m,n) = ackermann(m-1, ackermann(m, n-1))   for m,n > 0

    Ackermann's function is an example of a computable but not primitively
    recursive function.

- program **ackermann** uses a Python List to implement recursion

"""

from __future__ import annotations

import sys
from bm.recursive_functions.examples import ackermann_list


def ackermann_cli() -> None:
    """Evaluate Ackermann's function simulating recursion with a Python list.

    Usage: ``ackermann m n``

    - gets installed into the virtual environment
    - becomes numerically intractable after m=4 n=1

    """
    args = sys.argv[1:]
    if len(args) == 2:
        try:
            m = int(args[0])
            n = int(args[1])
            if m < 0 or n < 0:
                print('Error: Negative integer argument given', file=sys.stderr)
                sys.exit(1)
        except ValueError:
            print('Error: Non-integer argument given', file=sys.stderr)
            sys.exit(1)
    else:
        print('Error: ackermann.py takes 2 arguments', file=sys.stderr)
        sys.exit(1)

    print(ackermann_list(m, n))
