# Boring Math Library - Integer math package

Package of Python integer math libraries.

- [Number theory](#number-theory-module): `bm.integer_math.num_theory`
- [Combinatorics](#combinatorics-module): `bm.integer_math.combinatorics`

## Repos and Documentation

### Repositories

- [bm.integer-math][1] project on *PyPI*
- [Source code][2] on *GitHub*

### Detailed documentation

- [Detailed API documentation][3] on *GH-Pages*

This project is part of the
[Boring Math][4] **bm.** namespace project.

## Modules

### Number Theory Module

- Number Theory
  - *function* gcd(int, int) -> int
    - greatest common divisor of two integers
    - always returns a non-negative number greater than 0
  - *function* lcm(int, int) -> int
    - least common multiple of two integers
    - always returns a non-negative number greater than 0
  - *function* coprime(int, int) -> tuple(int, int)
    - make 2 integers coprime by dividing out gcd
    - preserves signs of original numbers
  - *function* iSqrt(int) -> int
    - integer square root
    - same as math.isqrt
  - *function* isSqr(int) -> bool
    - returns true if integer argument is a perfect square
  - *function* primes(start: int, end: int) -> Iterator[int]
    - now using *Wilson's Theorem*
  - *function* legendre_symbol(a: int, p: int) ->datastructures int
    - where `p > 2` is a prime number
  - *function* jacobi_symbol(a: int, n: int) -> int
    - where `n > 0`

______________________________________________________________________

### Combinatorics Module

- Combinatorics
  - *function* comb(n: int, m: int) -> int
    - returns number of combinations of n items taken m at a time
    - pure Python implementation of math.comb
      - reasonably performant
  - *function* perm(n: int, m: int) -> int
    - returns number of permutations of n items taken m at a time
    - pure Python implementation of math.perm
      - about 5x slower than `math.perm`
      - keeping around for PyPy 3.12+

______________________________________________________________________

[1]: https://pypi.org/project/bm.integer-math/
[2]: https://github.com/grscheller/bm-integer-math/
[3]: https://grscheller.github.io/boring-math-docs/integer-math/
[4]: https://github.com/grscheller/boring-math-docs
