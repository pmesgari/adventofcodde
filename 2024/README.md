# Advent of Code 2024 Solutions

Day 1 - Historian Hysteria
--------------------------
### Part 1
We are asked to pair up numbers from two lists according to the rule that each pair corresponds to the minimum number in each list. We are then required to find the distance between each pair and sum it up.

We simply sort each list and pair them up. Python sort function takes `O(NlogN)`. Pairing up takes `O(N)` and calculating the distance is `O(1)`. Total runtime is `O(NlogN)`.

### Part 2
We need to calculate a similarity score which depends on how frequent numbers in the first list appear. We simply go through the second list and count how often each number appears. Finally we calculate the similarity score by going through each number in the first list and multiplying it by the frequency it appears in the second list.

Counting the frequency of of numbers in the second list takes `O(N)`. Calculating the similarity score requires to consider every number in first list, takes `O(N)`. Overall takes `O(N)`.

Day 2: Red-Nosed Reports
------------------------
### Part 1
We have to determine if the levels in each report are safe or not. To be considered safe the numbers should be increasing or decreasing and every pair of adjacent numbers should differ by at least 1 and no more than 3. We simply consider each adjacent pair and check if they are all increasing or decreasing.

```
# all increasing
a[i] < a[i+1] -> a[i+1] - a[i] > 0 in range(1, 4)

# all decreasing
a[i] > a[i+1] -> a[i] - a[i+1] > 0 in range(1, 4)
```

With `N` reports and `M` levels in each report, it takes `O(NM)` to determine safety for all reports.

### Part 2
We now need to consider a damping effect. That is a single bad level is allowed. To do this we consider all combinations of the levels by skipping exactly one item.

For a report with `M` levels, we need to iterate `M` times to consider all cases where 1 element is missing. This makes our runtime to be `O(NM^2)`.

Day 3: Mull It Over
-------------------
### Part 1
We are given a long string that contains instructions to multiply two numbers. We simply use regex to find all matching instances and then sum up their multiplications.

Since we have a simple regex, if there are `K` matches and `M` is the average length of a match then it takes `O(KM)` to find the matches. But, we also need to traverse the whole input string. So overall runtime is `O(N + KM)`.

### Part 2
We now skip or do a multiplication depending on the appearence of `do()` and `don't()` prefixes. We find all the appearences of `do()`, `dont't()` and `mul(X,Y)` and then process them one by one. Since a `do()` or `don't()` enables or disables future multiplications we use a flag to keep track of whether we need to multiply or not.

Runtime stays the same `O(N + KM)`, we are just performing more matches.

Day 4: Ceres Search
-------------------
### Part 1
We need to find all `XMAS` words which can appear in any direction as well as reversed. We iterate over the grid and everytime we notice an `X` we check in all eight directions if it forms `XMAS`.

Traversing the grid takes `O(NM)` and checking in all eight directions takes `O(1)` because `XMAS` has a costant length.

### Part 2
We now need to find a more difficult pattern of cross `XMAS`. We can have a cross in one of these four combinations:

```
    M   S
      A
    M   S

    M   M
      A
    S   S

    S   M
      A
    S   M

    S   S
      A
    M   M
```

To find these we consider a smaller moving 3x3 grid and then check if any of these combinations occur.

Runtime is similar i.e. `O(NM)`, creating the smaller 3x3 grid takes constant effort.

*NOTE: I looked for `MAS` and `SAM` patterns when checking the cross situations. However, there is a better and simpler way which looks at the `A` character and checks the other characters on its 4 corner.*

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


Day 11: Plutonian Pebbles
-------------------------
### Part 1
We are given a set of rules that determine what happens to each stone when we blink. We are asked to blink 25 times and count the final number of stones.

The stones will behave independently from each other during each blink. We just apply the transformation rules to each stone and we generate a new list of stones after each blink. We do this 25 times and count the final number of stones.

In the worst case scenario each stone will double. With 25 iterations, we will have `O(2^25)` effort. Naive counting will do fine.

### Part 2
We are now asked the same but with 75 iterations. Naive counting results in `O(2^75)`, so naive counting is not going to work. There must be a more efficient way of counting. Let's imagine on the `ith` iteration we know number `2` occurs `x` times. Then in the `(i+1)th` iteration number `2024` must appear `x` times. For each `2` we have we end up with a `2024`.

Let's take another example, imagine on the `ith` iteration `2022` occurs `x` times. Then in the `(i+1)th` iteration each of the `2022` numbers will split in two, so we have `20` and `22` each occuring `x` times.

In each blink we start a new counter. Then we apply the transformation rules to each stone and we know that transformation will occur as many times as the stone count in the current counter.

With each iteration we only perform a constant amount of work. Because applying the transformation rules is `O(1)` and updating the counter is also `O(1)`. With `N` iteration total runtime is `O(N)`.

Day 12: Garden Groups
---------------------
### Part 1
We are asked to determine each region and then calculate the total fencing price, i.e. `area x perimeter`. To determine each region we use a DFS approach. We begin at position `(0, 0)` and then explore all plots of the same type and then move onto next plot type. As we explore each plot, we mark them as seen to avoid going back there. This gives us the `area` of each plot. We now use the region we found and determine its perimeter. Each plot can contribute at most 4 to the perimeter. A perimeter is like a boundary and it exists when we go out of bounds or we have a plot of a different type as our neighbor. So for each plot in our region we look in all 4 directions and for each direction where one of the two conditions met we add 1 to our perimeter. Finally we calculate the total fencing price.

Traversing the input grid takes `O(N x M)`. Running DFS takes `O(N + M)`. Calculating the area of each region is `O(1)` and finding all the perimeters in each region takes `O(N x M)`. Imagine a grid input where each plot is a different type, we then need to traverse each grid point one by one.

### Part 2
In part 2 we are asked to consider sides instead of perimeter. We again consider region by region. We use a similar idea to perimeter but call it a segment. Each plot can have at most 4 segments marked from 0 to 3.

```
   0
  +-+
3 |D| 1
  +-+
   2
```

A segment can have an edge and the definition of an edge is the same as a perimeter. Given a region, we first create a map of all the segments that act as an edge. We then pick a random point in the region that has an edge segment. We start walking along this edge segment in 90 and 270 degrees parallel to the edge direction for as long as we can. As we walk we cross out the segments we visit. For example when we have an edge in the up direction, we walk left and right. 

```
-- -- -- --
<- <- ^ -> ->
```

We have to make sure we only walk along continious segments. As soon as we do not have an edge segment in our walk we will stop. We can see this situation in the second example. Let's say we are at first row and 2nd plot while seeing an edge in the downward direction. We then move left and right. If we move right without checking for segment continuity we are going to cross the 2nd `O` in the 2nd row and get to the 2nd `X` plot and there we will see there is an edge segment and cross it out, and that would be incorrect.

```
OvOOO
OXOXO
```

Our runtime stays `O(N x M)` since in the worst case scenario we have a grid input where each cell is a different type and we will need to identify all its 4 edge segments.

Day 13: Claw Contraption
------------------------
### Part 1
We are asked to calculate the fewest number of tokens to reach the prize location by pushing the A and B buttons. Each button can be pushed at most 100 times. In this part we can simply use brute force. Press the A button once, see how far are we from target and check if we can get to target by prressing the B button an integer number of times. For every combination that gets us to target we calculate the tokens needed. We keep doing this until we have pushed A 100 times.

In each iteration we do `O(1)` work because we are just doing arithmetic calculations. We also have the 100 time restriction so our iteration are also limited. Makes the overall runtime `O(1)`.

### Part 2
In part 2 our prize location has moved by `10000000000000` units in both X and Y directions. Instead of the naive solution we can simply treat the problem as solving two linear equations in two variables.

```
xt = ca * xa + cb * xb
yt = ca * ya + cb * yb
```

These equations describe two lines. They are either parallel, the same or intersect and if they intersect they can only intersect in a single point. Doing a bit of algebra we can solve for `ca` and `cb` like so:

```
ca = (xt * yb - xb * yt) / (xa * yb - xb * ya)
cb = (xt * ya - xa * yt) / (xb * ya - xa * yb)
```

If both `ca` and `cb` are `>= 0` and are integer values we have an intersection.

It takes `O(1)` because again we are just doing arithmetic calculations.

Day 14: Restroom Redoubt
------------------------
### Part 1
We have several robots that move in straight lines and they can share the same position. We are asked to simulate the movement of the robots after 100 steps and then split the grid in 4 quadrants, count the robots in each quadrant and multiply the counts.

Robots can teleport, that is wrap around when they go out of bound. We are given the start position, velocity vector and we know the time so we can simply calculate the final position of each robot:

```
x2 = (x1 + vx * time) % width
y2 = (y1 + vy * time) % height
```

We use a counter that maps `position -> number of robots` and move all the robots. Finally we split the grid in 4 quadrants and count the number of robots in each and return their product.

When moving We are only perfoming `O(1)` arithmetics so runtime is bound by number of robots, thus `O(N)`. When calculating the product of quadrant counts we might have one robot per tile, giving a total runtime of `O(NM)` if `N=width` and `M=height`.

### Part 2
I found the question vague, and had to get some help from the web. At the end it was easier than I thought. We are looking for the timestamp in which a Christmas tree emerges. When that happens we are also told most of the robots arrange themselves into a Christmas tree. So, there will be a region in the grid where robots density is high.

We keep increasing the time steps and move the robots then calculate their density. We calculate the center of the robot's x and y positions by taking the mean of their x and y coordinates. Then we calculate the mean total distance of all robot positions from the center. We find the distance by simply using Manhattan distance. The time step at which we have the smallest mean total distance from center is probably a good sign that we have a Christmas tree as most robots will arrange themselves into that shape. It turned out this is indeed the case.

Runtime for moving robots and calculating is `O(N)` and now we might need a minimum of `K` time steps to arrange the robots in a Christmas tree, making the final runtime to be `O(KN)`.

Day 15: Warehouse Woes
----------------------
### Part 1
We have a robot which moves in a grid and possibly shifts boxes around. Everytime we detect a box ahead of our robot movement direction we perform a sweep to find all connected boxes. Then we determine the new positions of all the boxes and if none of the new positions coincides with a wall, then we move all the boxes and the robot to their new positions.

We have `M` moves to process. In the worse cast all boxes in the grid may be connected, so we will have to traverse the entire grid, that makes `O(MxRxC)` with `R` the number of rows and `C` the number of columns.

### Part 2
In part 2 everything doubles. This means our robot will face either the left `[` or the right `]` side of a box and that boxes could be connected with each other. So, we need to identify when facing half a box what are all the boxes that needs to move. Everytime we have a half box in front, we find its other half and that gives us a complete box. But, each half of our box could have another half box on top/below it. So, we check if each half of our complete box has another halft connected to it, if so we will add that half to our queue for processing.

The key point here is to understand connected boxes will move all together as a blob. Once we detect the entire blob, all we need to check is if any of the boxes in this blob coincide with a wall, if not we can move all of them at once.

Our runtime stays similar, the doubling effect is just a constant factor.