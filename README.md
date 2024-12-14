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

Day 8: Bridge Repair
--------------------
### Part 1
We need to consider all pairs of antennas with the same frequency. Then for each pair we get two antinodes, one on each side. We can find the position of the antinodes using simple vectors and geometry. Since all pairs and antinodes must be on the same line, this means they follow a linear relation.

For part 1 the antinodes must be a distance of 2 apart. If we have a pair `ab`, we can use this linear relation to find the antinode positions.

```
dir_ab = (rb - ra, cb - ca) # direction vector from a -> b
# we now place an antinode using this direction vector and a distance of 2
dr, dc = dir_ab
antinode_position = (ra + distance * dr, ca + distance * dc) # where distance = 2
```

Collecting same frequencies requires traversing the entire grid once, takes `O(MN)`. In the worst case scenario we end up with antennas on every cell, calculating the antinode positions is a constant time operation, so it takes `O(MN)`.

### Part 2
We drop the 2 distance away constraint. We basically put antinodes on both directions of the line connecting pairs `ab` as long as we stay within the grid. We have the direction vector from part 1, we now simply keep incrementing the distance. The maximum distance will never be larger than the `max(height, width)` of the grid.

Runetime stays the same, `O(MN)`.


Day 9: Disk Fragmenter
----------------------
### Part 1
Reprsent the dense layout as a string layout. Use two pointers, one pointing at the next free space, the other pointing at the beginning of a file. Then move file blocks one by one from right to left.

Parsing the input takes `O(N)`. Using the two pointer approach, we are seeing each position at least once, and for some we do a constant number of work, we also need to calculate the checksum. Overall takes `O(N)`.

### Part 2
We are restricted to only move files if there is a space that fits the file size. I took a naive approach. Find all file blocks and for each file block search for a free space that fits the file. If there is a space then move the file. For each file this takes `O(N)` effort. If there are `N` files, it will be `O(N^2)`.

A more efficient approach would have been representing the files and free spaces as ranges, and use arithmetics to move/find blocks around.


Day 10: Hoof It
---------------
### Part 1
We are asked to find from each 0-height position how many 9-height positions we can reach given every step we take must be gradual and even. We can treat this problem as a graph problem. Each position is mapped to a vertex and we add an edge `u -> v` if `height[v] - height[u] == 1`. We then use a BFS approach to explore the graph, and everytime we see a 9-height position we increment the score.

BFS takes `O(N+M)`. Reading the input though takes `O(MN)`.

### Part 2
We are now asked to find all distinct paths from a trailhead to a 9-height position. We can still use BFS with a few modifications. Now there can be multiple paths leading to a 9-height position. Previously we marked a 9-height position as seen as soon as we reached it. Everytime we pull a position from our queue to explore, if its a 9-height position then we have found a trail and increase the rating. A trail always ends in a 9-height position and there is nowhere to go from that position. Its the end. So, we just reset our seen array to allow starting a new trail.

Runtime stays the same.
