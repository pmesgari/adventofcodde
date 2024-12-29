# Advent of Code 2024 Solutions

Table of Contents
-----------------
- [Day 1 - Historian Hysteria][d01]
- [Day 2: Red-Nosed Reports][d02]
- [Day 3: Mull It Over][d03]
- [Day 4: Ceres Search][d04]
- [Day 5: Print Queue][d05]
- [Day 6: Guard Gallivant][d06]
- [Day 7: Bridge Repair][d07]
- [Day 8: Bridge Repair][d08]
- [Day 9: Disk Fragmenter][d09]
- [Day 10: Hoof It][d10]
- [Day 11: Plutonian Pebbles][d11]
- [Day 12: Garden Groups][d12]
- [Day 13: Claw Contraption][d13]
- [Day 14: Restroom Redoubt][d14]
- [Day 15: Warehouse Woes][d15]
- [Day 16: Reindeer Maze][d16]
- [Day 17: Chronospatial Computer][d17]
- [Day 18: Day 18: RAM Run][d18]
- [Day 19: Linen Layout][d19]
- [Day 20: Race Condition][d20]
- [Day 21: Keypad Conundrum][d21]
- [Day 22: Monkey Market][d22]
- [Day 23: LAN Party][d23]
- [Day 24: Crossed Wires][d24]
- [Day 25: Code Chronicle][d25]

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

Day 16: Reindeer Maze
---------------------
### Part 1
We have a maze with a start and end positions. In each iteration we either move in the current heading or rotate 90 degree clockwise or counter clockwise. Moving in the current heading costs 1 unit and rotating cost 1000. We can use A-star algorithm to find the lowest cost from start to end.

I couldn't find a proper way to formulate the runtime. Reading some literature points to a worst case runtime of `O(b^d)` and depending on the quality of the heuristic function this can be improved.

### Part 2
We now need to find all the lowest cost paths that leads start to finish and then find the total number of positions that are part of any lowest cost path.

To do this I omitted the heuristic function and then began to expand the states and the path. I continue with a path as long as its cost does not exceed the lowest best cost and the path reaches the end. Then I keep track of all the paths I found and finally return the length of their unions. I kept track of each state by using a tuple of `(current_cost, head, path)`. I then try to expand the head and check if the path is worth to continue. If yes, then I generate a new state and keep going further.

Similar to part 1, I couldn't easily formulate the runtime of this problem.

Day 17: Chronospatial Computer
------------------------------
### Part 1
We are asked to run a program using the opcodes and operands in the input. I just implemented each opcode and simply executed the program.

Each opcode takes `O(1)` so runtime is `O(N)` with `N` being the number of opcodes.

### Part 2
I struggled with understanding part 2, had to look at hints and solutions on the web. Eventually I understood all that matters are the 3 least significant bits of register `A` as they determine the output if read from the end. To find `A` I tried finding a set of candidates that generate the last number in my program and then for each of these candidates try to propagate further to generate the remaining numbers.

Assuming there can be `M` candidates we run the program for each candidate once, thus giving a total runtime `O(MN)`


Day 18: Day 18: RAM Run
-----------------------
### Part 1
We are given a search problem. We simulate the falling bytes and create the corresponding grid and then run BFS to find a path from start to end. Once we have a path, we will use backtracking to find the total length of the path.

Running BFS takes `O(N+M)` and the backtrack can take at most `O(N)` where `N = number of vertices` and `M = number of edges`. Overall runtime is `O(N+M)`.

### Part 2
We have to find the first byte which blocks the path from start to finish. This is a good place to use binary search. We are looking for the minimum number of bytes to block the path. We start our binary search with `left = 0` and `right = len(bytes)` and in each iteration use our solution from part 1 to detect if there is still a path or not. When binary search finishes, the left index will be the minimum number of bytes needed to block the path.

We run BFS at most `O(logB)` times with `B` the total number of falling bytes. In worst case scenario we need every cell in the grid to be blocked so `B = N`. This makes a total runtime of `O(N+m) * O(logN) = O(logN * (N + M))`.

Day 19: Linen Layout
--------------------
### Part 1
We are given some patterns and need to determine if we can make the needed designs. We use a recursive approach. We start with the initial design and everytime there is a pattern matching the beginning of the design we make a recursive call to see if we can make the reamining part of the design. If at any point we have an empty design it means we have created the design with the available patterns. We keep a count of the total number of times we reached an empty design. Finally we sum all instances where `total > 0`.

We need to use a cache as the number of possibilities will be exponential.

### Part 2
We use the same solution as part 1 but instead of summing all instances where `total > 0`, we simply sum all the returned totals.

Day 20: Race Condition
----------------------
### Part 1
We are given two points and asked to find the shortest path with the twist that we can cheat once. A cheat allows us to ignore a wall cell and go through it. We can use Dijkstra algorithm to find the shortest path from start to every other node. Then we will simulate what would happen if along this shortest path we would go through a wall.

Imagine the following cheat, we are at position `X` and decide to go through the wall. We call position `X` as `p1` and the dot we arrive at as `p3`.  We are also given a critical piece of information, *there is a single path from start to end*. This means after Dijkstra has finished, we only have the distances for the points that are along the path from start to finish.

```
..X#.
```

If we split our paths in parts **without** cheating and while going through `p1`, we will have:

```
distance S -> p1 + distance p1 -> E
```

Now, by cheating we will have:

```
distance S -> p1 + distance p1 -> p3 + distance p3 -> E
```

If we want to save at least 100 seconds then we have to find the pairs `(p1, p3)` where `distance S -> p1 - distance S -> p3 >= 102`. This formula is telling how many cells we save if we were to go through a wall from `p1` and end up on `p3`. Going through the wall itself will take 2 steps, that's why we have 102 as the lower limit.

We can find the pairs `(p1, p3)` by checking all the points along the path that have a wall as their neighbors. For all those points we then use our formula to calculate the time savings and if its at least `>= 102` we increment our count.

Dijkstra takes `O(M + NlogN)`, finding the pairs takes at most `O(N)`, overall we have `O(M + NlogN)`.

### Part 2
In part 2 we are allowed an extended cheat, up to 20 cells. We can use the same approach, we just have more pairs that could save us time. Considering we are at position `X` our cheat cells would follow one of these patterns with up to 20 cells.

```
---X---- # horizontal

  |      # vertical
  |
  X
  |
  |
           
      |  # L-Shaped
      |
---X--|   ---X--|
                |
                |
```

For each of these patterns, and for each pair within such pattern we again calculate our time savings and increment our count. To find the time savings we will now use the Manhttan distance.

Runtime for Dijkstra stays the same, but we now have way more pairs to consider. For each point along our path, we consider all cheat pairs, `O(N * C^2)` where `C` is the cheat length. Overall runtime would be `O(M + NlogN) + O(NC^2)`.

Day 21: Keypad Conundrum
------------------------
### Part 1
We have multiple robots and keypads which we need to manouver. The numerical keypad is the one we will need to insert the code on. There are two other directional keypads that eventually control the numerical keypad. Its easier to use a level view of the keypads.

```
Level 1
    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+

Level 2
    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+

Level 3
+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+

```

Lets say we want to press the `0` button on the numeric keypad. This is what needs to happen:

```
On level 3, move from A to 0 and press 0, giving us the path = <A
  to move <
    On level 2, move from A to < and press <, giving us the path = v<<A
      to move v
        On level 1, move from A to v and press v, giving us the path = <vA # pressing A here pushes down v key on level 1 which triggers the robot on level 2 to move v
      to move <
        On level 1, move from v to < and press <, giving us the path = <A 
      to move <
        On level 1, move from < to < and press <, giving us the path = A # we are already on < so no move is required
      to press A
        On level 1, move from < to A, giving us the path = >>^A # pressing A here, pushes down A on level 2 which finally moves the robot arm on level 1 to move 3
  the total path to move < is <vA<AA>>^A on level 1
  to press A
    On level 2, move from < to A and press A, giving us the path = >>^A
      to move >
        On level 1, move from A to v and press v, giving us the path = vA
      to move >
        On level 1, move from A to A and press A, giving us the path = A
      to move ^
        On level 1, move from > to ^ and press ^, giving us the path = <^A
      to press A
        On level 1, move from ^ to A and press A, giving us the path = >A
  the total path to press A is vAA<^A>A

The entire path to move from A to 0 and press A is <vA<AA>>^AvAA<^A>A
  ```

Some key observations are:
- On every keypad we move to a target key and press it. This measn we start at key `A` and end on key `A` on that keypad.
- When moving to target key on level 1 and pressing `A`, we cause the robot arm on level 2 to move or to press 'A' but we stay on target key on level 1.

We begin with finding all the shortest path for each pair of keys on each keypad. We are essentially building a giant cache of all the possibilities. Our cache tells us to get from key A to key B on level X and it will take a minimum of N steps. We then run each code through our cache to find sum up all the sequences needed on level 1.

Building the cache takes `O(LN^2)` assuming each side of the largest keypad is `N` and having `L` levels.

### Part 2
We have more levels, this means we need a to build a bigger cache by including more levels. Runtime stays the same.

Day 22: Monkey Market
---------------------
### Part 1
We need to calculate the 2000th element of a sequence. We just follow the sequence generation rules to generate the 2000th element for each initial secret and then sum those up.

The generation rules take `O(1)`. So, total runtime is `O(N)` with `N` being the total number of initial secrets.

### Part 2
We are now asked to find the optimal sequence of price changes that give us the most bananas. We can use a `deque` of maximum length 4 to implement a fixed sliding window of size 4. We then record each 4 tuple of price deltas and the bananas we get, which is the ones digit of the 4th element in our current sliding window.

We get the price deltas for each initial secret and then use a `Counter` to sum up all the bananas across all the monkeys for each price delta. The final answer is the max value in the counter.

If we were to brute force this part, our deltas could range from -9 to +9 so we have 19 numbers. We then need to consider a 4-tuple of deltas, giving `19^4` possibilities. Doing this for each monkey (1685) and for each secret number (total 2000) would come around 400 billion. By using a sliding window approach we sweep through the 2000 secrets once, and then summing up over the counter is another final sweep. So, runtime stays linear `O(N)`.

Day 23: LAN Party
-----------------
### Part 1
We are asked to find sets of 3 computers that are connected to each other. We can treat this as a graph problem. We parse our input data into an adjacency list and then traverse this list to find all 3 vertices that are connected to each other. A nice trick here is to sort the 3 vertices and use a set to avoid over counting, because order does not matter.

It takes `O(NM)` to build the adjaceny list and traversing it also takes `O(NM)`.

### Part 2
We need to find the largest set of computers that are all connected to each other. This is the same as finding the largest clique in a graph which is an NP-complete problem. I used the `networkx` library to find the largest clique and it was quite neat.

Day 24: Crossed Wires
---------------------
### Part 1
We have a list of logic gates to evaluate. Each gate could have one or more dependencies on other gates. We are only interested in finding the output to `z` gates. We use a recursive approach where we look for the signal value of our gate in the provided signals, if there is a value we are fine, otherwise we recursively find the other gates that define the value for our signal. We keep doing this until we have a gate that all its signals are available in our signals list. I also implemented a signal cache to avoid recalculating signal values.

Evaluating each gate could make `N` other recursive calls to find all its dependencies. With `N` gates we will have `O(N^2)` runtime.

### Part 2
*TODO*

Day 25: Code Chronicle
----------------------
The last puzzle, we need to match keys with locks. We parse each key and lock block and then we count the number of `#` in each column. A key will match a lock iff there are no overlapping `#` cells. This requires the sum of `#` in each column of a given key and a lock should be `<= 5` since we have at most 5 rows.


[top]: #advent-of-code-2024-solutions
[d01]: #day-1---historian-hysteria
[d02]: #day-2-red-nosed-reports
[d03]: #day-3-mull-it-over
[d04]: #day-4-ceres-search
[d05]: #day-5-print-queue
[d06]: #day-6-guard-gallivant
[d07]: #day-7-bridge-repair
[d08]: #day-8-bridge-repair
[d09]: #day-9-disk-fragmenter
[d10]: #day-10-hoof-it
[d11]: #day-11-plutonian-pebbles
[d12]: #day-12-garden-groups
[d13]: #day-13-claw-contraption
[d14]: #day-14-restroom-redoubt
[d15]: #day-15-warehouse-woes
[d16]: #day-16-reindeer-maze
[d17]: #day-17-chronospatial-computer
[d18]: #day-18-day-18-ram-run
[d19]: #day-19-linen-layout
[d20]: #day-20-race-condition
[d21]: #day-21-keypad-conundrum
[d22]: #day-22-monkey-market
[d23]: #day-23-lan-party
[d24]: #day-24-crossed-wires
[d25]: #day-25-code-chronicle

