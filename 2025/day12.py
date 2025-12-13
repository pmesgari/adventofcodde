import sys

sys.setrecursionlimit(10000)


class BitmaskGrid:
    """
    Manages the board state using a single integer (self.mask).
    Handles the 'magic' of 2D coordinates -> 1D bit operations.
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.mask = 0  # 0 = empty, 1 = filled
        self.size = width * height

    def find_first_empty(self):
        """Returns the index of the first 0 bit, or -1 if full."""
        for i in range(self.size):
            if not (self.mask & (1 << i)):
                return i
        return -1

    def can_place(self, piece_mask, idx, piece_w, piece_h, min_c):
        """Checks collision AND boundary wrap-around."""
        # Shift piece to target index
        shifted_piece = piece_mask << idx

        # Check collision
        if (self.mask & shifted_piece) != 0:
            return False

        # Check horizontal boundary
        current_col = idx % self.width
        if current_col + piece_w > self.width:
            return False

        if current_col + min_c < 0:
            return False

        # Check vertical boundary
        current_row = idx // self.width
        if current_row + piece_h > self.height:
            return False

        return True

    def place(self, piece_mask, idx):
        self.mask |= piece_mask << idx

    def remove(self, piece_mask, idx):
        self.mask ^= piece_mask << idx


# g = BitmaskGrid(4, 4)
# # Place horizontal domino ## at index 0
# g.place(3, 0)
# print(bin(g.mask))
# print(g.find_first_empty())


def parse_shapes(lines):
    """
    Reads the visual shape diagrams.
    Returns a Dictionary: { index: [(r, c), (r, c)...] }
    """
    shapes_raw = {}
    current_id = -1
    buffer = []

    def save_buffer():
        if current_id != -1 and buffer:
            coords = []
            for r, row_str in enumerate(buffer):
                for c, char in enumerate(row_str):
                    if char == "#":
                        coords.append((r, c))
            shapes_raw[current_id] = generate_variants(coords)

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.endswith(":"):
            save_buffer()
            current_id = int(line[:-1])
            buffer = []
        else:
            buffer.append(line)

    save_buffer()

    return shapes_raw


def normalize_shape(coords):
    """
    Shifts coordinates so the top-left-most # is at (0,0).
    Critical for the 'First Empty Cell' algorithm.
    """
    if not coords:
        return tuple()

    sorted_coords = sorted(coords)

    r0, c0 = sorted_coords[0]

    normalized = tuple(sorted([(r - r0, c - c0) for r, c in sorted_coords]))
    return normalized


def generate_variants(base_coords):
    """
    Takes one shape (list of coords) and generates all 8 rotations/flips.
    Returns a List of unique coordinate lists.
    """
    variants = set()

    current = base_coords

    # 2 flips
    for _ in range(2):
        # 4 rotations
        for _ in range(4):
            variants.add(normalize_shape(current))

            # rotate 90 degrees clockwise: (r, c) -> (c, -r)
            current = [(c, -r) for r, c in current]

        # flip vertically: (r, c) -> (-r, c)
        current = [(-r, c) for r, c in base_coords]

    return list(variants)


# sample_input = """
# 0:
# ##
# #.
# """
# shapes = parse_shapes(sample_input.splitlines())
# print(f"Shape 0 has {len(shapes[0])} variants.")


def solve_recursive(grid: BitmaskGrid, inventory, shape_masks, priority_order):
    """
    The recursive heart of the algorithm.
    grid: BitmaskGrid instance
    inventory: Dict { shape_id: count_remaining }
    shape_masks: Dict { shape_id: [ (mask, w, h), ... ] }
    """
    if all(c == 0 for c in inventory.values()):
        return True

    idx = grid.find_first_empty()
    if idx == -1:
        return False

    for shape_id in priority_order:
        count = inventory[shape_id]
        if count > 0:
            for mask, max_c, max_r, min_c in shape_masks[shape_id]:
                if grid.can_place(mask, idx, max_c + 1, max_r + 1, min_c):
                    grid.place(mask, idx)

                    inventory[shape_id] -= 1

                    if solve_recursive(grid, inventory, shape_masks, priority_order):
                        return True

                    inventory[shape_id] += 1

                    grid.remove(mask, idx)

    return False


def solve_region(region_line, shapes):
    """
    Parses a single region line (e.g., "12x5: 1 0..."),
    prepares the Bitmasks for that specific width,
    and runs the solver.
    """
    try:
        dims, counts_str = region_line.split(": ")
    except ValueError:
        return False

    w, h = map(int, dims.split("x"))
    counts = list(map(int, counts_str.split()))

    inventory = {}
    compiled_masks = {}
    total_present_area = 0

    for shape_id, count in enumerate(counts):
        if count == 0:
            continue
        inventory[shape_id] = count

        variants_compiled = []
        base_coords_list = shapes[shape_id]

        shape_area = len(base_coords_list[0])
        total_present_area += shape_area * count

        for coords in base_coords_list:
            mask = 0
            max_r, max_c = 0, 0
            min_c = 0

            for r, c in coords:
                index = r * w + c
                mask |= 1 << index

                max_r = max(max_r, r)
                max_c = max(max_c, c)
                min_c = min(min_c, c)

            variants_compiled.append((mask, max_c, max_r, min_c))

        compiled_masks[shape_id] = variants_compiled

    board_area = w * h
    if total_present_area > board_area:
        return False

    gap = board_area - total_present_area
    if gap > 0:
        # Add ghost 1x1 pieces to fill the holes
        inventory[-1] = gap
        compiled_masks[-1] = [(1, 0, 0, 0)]

    def get_priority(sid):
        if sid == -1:
            return (-1, -1)

        area = bin(compiled_masks[sid][0][0]).count("1")
        return (1, area)

    priority_order = sorted(inventory.keys(), key=get_priority, reverse=True)

    grid = BitmaskGrid(w, h)

    return solve_recursive(grid, inventory, compiled_masks, priority_order)


def part1():
    # Read all lines
    with open(0) as f:
        content = f.read()
        parts = content.strip().split("\n\n")

    # 1. Parse Shapes
    shape_lines = []
    for part in parts[:-1]:
        shape_lines.extend(part.strip().splitlines())
    shape_data = parse_shapes(shape_lines)

    # 2. Solve each Region
    region_lines = parts[-1].strip().splitlines()
    total_solvable = 0
    for i, line in enumerate(region_lines):
        if solve_region(line, shape_data):
            total_solvable += 1

    print(total_solvable)


part1()
