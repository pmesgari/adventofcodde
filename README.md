# Advent of Code Solutions
My solutions to advent of code challenges.

# Usage

- Store the cookie in `env.sh` as `AOC_COOKIE`.
- Download the input data using `./download.sh <year> <day>`.
- Solve it using `python solve.py <year> <day>`. To solve using example input, put the data in `test.txt` and pass `--test` flag.


Day 1 - Historian Hysteria
--------------------------

Day 2: Red-Nosed Reports
------------------------

Day 3: Mull It Over
-------------------

Day 4: Ceres Search
-------------------

Day 5: Print Queue
------------------
### Part 1
For each page apply the rules to determine if page is valid.
A rule `X | Y` requires `X` to appear before `Y`, which means position of `X` in the list is smaller than position of `Y`. If all the rules are satisfied the page is valid and we can include its middle page in the sum

Lets assume `|page|=n` then there can be at most `n-1` rules. Imagine `1, 2, 3, ..., n` then we have `1|2, 2|3, ..., n-1|n`. Checking all the rules for 1 number in page takes `O(n)`, doing this for `n` numbers will take `O(n^2)`. 

### Part 2
For every page out of order, we apply the rules. If a rule fails, then we swap (fix) the page for that rule. We keep doing this until no more swaps remain which means the page is now in order.

Swapping takes `O(1)`, so runtime stays `O(n^2)`.

Day 6: Guard Gallivant
----------------------
### Part 1
We represent the state of the guard by its row, column and current direction. We continue generating a next state until the guard is out of bounds.

If the grid is of size `M x N`, in the worst case scenario, the guard will traverse all the grid points, giving `O(MN)`.

### Part 2
If the guard will be trapped in a loop, we should put an obstruction on the cells the guard will visit without an obstruction. We can find all those positions from part 1. We then try putting an obustrction for each position one at a time and check if the guard is trapped in a loop.

To check for a loop, there should be one repeating state, i.e. same row, column and direction.

Each simulation will take `O(MN)`, in the worst case scenario we have to try every possible cell, giving `O((MN)^2)`. If `M=N`, we have an `O(N^4)` which explains why it takes around 40 seconds to complete.

Day 7: Bridge Repair
--------------------
### Part 1
We solve it using dynamic programming approach. The recurrence relation is:

```
T[0] = [equation[0]]
T[i] = [
    T[i-1][j] + equation[i],
    T[i-1][j] * equation[i]
]
1 <= i < len(equation)
1 <= j < len(T[i-1])

return test_val if any T[-1] == test_val otherwise 0
```

We can do this because operators are always evaluated left-to-right. This allows us to take a bottom up approach and build a table of all the calculated values up to a prefix of length `i`. At each step we either multiply or add the previous values to the current value.

Lets assume we have `N` numbers. The number of values we calculate increase exponentially, see below example. At prefix `i` we have `2^i` values. This makes for a terrible runtime of `O(2^N)`.

```
292 11, 6, 16, 20
    11
        11
    11 6
        11 * 6
        11 + 6
    11 6 16
        11 * 6 + 16
        11 + 6 + 16
        11 * 6 * 16
        11 + 6 * 16
    11 6 16 20
        11 * 6 + 16 + 20
        11 + 6 + 16 + 20
        11 * 6 * 16 + 20
        11 + 6 * 16 + 20
        11 * 6 + 16 * 20
        11 + 6 + 16 * 20
        11 * 6 * 16 * 20
        11 + 6 * 16 * 20
```

### Part 2
To add the concat operator we slightly modify our recurrence relation.

```
T[i] = [
    T[i-1][j] + equation[i],
    T[i-1][j] * equation[i],
    equation[i-1] || equation[i], if i == 1
    T[i-1][j] || equation[i], if i >= 2
]
1 <= i < len(equation)
1 <= j < len(T[i-1])
```

Runtime stays the same as before.

