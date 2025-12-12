from typing import Tuple, Dict


Position = Tuple[int, int]
Grid = Dict[Tuple[int, int], str | int]
Table = Dict[Tuple[int, int], int]


with open(0, encoding="utf-8") as f:
    red_tiles = []
    for line in f.readlines():
        red_tiles.append(tuple(map(int, line.strip().split(","))))

areas = []
for i in range(len(red_tiles)):
    x1, y1 = red_tiles[i]
    for j in range(i + 1, len(red_tiles)):
        x2, y2 = red_tiles[j]
        area = abs((x1 - x2 + 1) * (y1 - y2 + 1))
        areas.append((area, i, j))

sorted_areas = sorted(areas, key=lambda v: v[0], reverse=True)
print(sorted_areas[0][0])


min_x = min(red_tiles, key=lambda v: v[0])[0] - 1
max_x = max(red_tiles, key=lambda v: v[0])[0] + 1
min_y = min(red_tiles, key=lambda v: v[1])[1] - 1
max_y = max(red_tiles, key=lambda v: v[1])[1] + 1

print(min_x, max_x, min_y, max_y)


def build_boundary_segments(red_tiles):
    segments = []

    def make_seg(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return ((min(x1, x2), min(y1, y2)), (max(x1, x2), max(y1, y2)))

    for i in range(len(red_tiles) - 1):
        segments.append(make_seg(red_tiles[i], red_tiles[i + 1]))

    segments.append(make_seg(red_tiles[0], red_tiles[-1]))

    return segments


def segments_intersect(seg1, seg2):
    (x1, y1), (x2, y2) = seg1
    (x3, y3), (x4, y4) = seg2

    if x1 == x2 and y3 == y4:
        return (x3 < x1 < x4) and (y1 < y3 < y2)
    elif y1 == y2 and x3 == x4:
        return (x1 < x3 < x2) and (y3 < y1 < y4)

    return False


def rect_crosses_boundary(p1, p2, boundary_segments):
    x1, y1 = p1
    x2, y2 = p2

    xmin = min(x1, x2)
    ymin = min(y1, y2)
    xmax = max(x1, x2)
    ymax = max(y1, y2)

    rect_segments = [
        ((xmin, ymin), (xmax, ymin)),
        ((xmax, ymin), (xmax, ymax)),
        ((xmin, ymax), (xmax, ymax)),
        ((xmin, ymin), (xmin, ymax)),
    ]

    for seg1 in rect_segments:
        for seg2 in boundary_segments:
            if segments_intersect(seg1, seg2):
                return True

    return False


def is_point_inside(point, boundary_segments):
    crossings = 0

    xp, yp = point

    for (x1, wy1), (x2, wy2) in boundary_segments:
        if (x1 == x2) and (x1 > xp) and (min(wy1, wy2) <= yp < max(wy1, wy2)):
            crossings += 1

    return crossings % 2 != 0


def segment_splits_rect(p1, p2, segment):
    x1, y1 = p1
    x2, y2 = p2

    xmin, xmax = min(x1, x2), max(x1, x2)
    ymin, ymax = min(y1, y2), max(y1, y2)
    (bx1, by1), (bx2, by2) = segment

    b_mid_x = (bx1 + bx2) / 2
    b_mid_y = (by1 + by2) / 2

    return xmin < b_mid_x < xmax and ymin < b_mid_y < ymax


def solve(red_tiles):
    boundary_segments = build_boundary_segments(red_tiles)

    max_area = 0
    for i in range(len(red_tiles)):
        x1, y1 = red_tiles[i]
        for j in range(i + 1, len(red_tiles)):
            x2, y2 = red_tiles[j]
            width = abs(x1 - x2) + 1
            height = abs(y1 - y2) + 1
            area = width * height

            if area < max_area:
                continue

            if rect_crosses_boundary((x1, y1), (x2, y2), boundary_segments):
                continue

            midx = min(x1, x2) + 0.5
            midy = min(y1, y2) + 0.5
            if not is_point_inside((midx, midy), boundary_segments):
                continue

            splits = False
            for seg in boundary_segments:
                if segment_splits_rect((x1, y1), (x2, y2), seg):
                    splits = True

            if splits:
                continue
            if area > max_area:
                max_area = area

    return max_area


print(solve(red_tiles))
