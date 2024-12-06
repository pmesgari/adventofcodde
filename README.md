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