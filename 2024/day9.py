"""--- Day 9: Disk Fragmenter ---"""

from typing import List


with open(0, encoding="utf-8") as f:
    disk_map_input = f.readline().strip()


def parse_disk_map(disk_map: str) -> List[str]:
    """Represent a disk map in string format"""
    output = []
    fid = 0
    for idx, char in enumerate(disk_map):
        if idx % 2 == 0:
            for _ in range(int(char)):
                output.append(fid)
            fid += 1
        else:
            for _ in range(int(char)):
                output.append(".")
    return output


def calc_checksum(disk_map: List[str]) -> int:
    """Calculate the checksum"""
    total = 0
    for idx, char in enumerate(disk_map):
        if char == ".":
            continue
        total += idx * int(char)

    return total


def find_files(disk_map: List[str]) -> List[List[int]]:
    """Find all file blocks on the disk
    Each file is represented as a tuple (fileid, start, size)
    """
    files = []
    fid = 0
    start = 0
    size = 0
    while True:
        if start >= len(disk_map):
            break
        if disk_map[start] == ".":
            start += 1
            continue
        curr = disk_map[start]
        size = 0
        while True:
            if start + size >= len(disk_map):
                break
            if disk_map[start + size] != curr:
                break
            size += 1
        files.append((fid, start, size))
        fid += 1
        start += size

    return reversed(files)


def find_slice(disk_map: List[str], filesize: int):
    """Find a free space that fits the given filesize"""
    start = 0
    size = 0
    while True:
        if start >= len(disk_map):
            return None
        if disk_map[start] != ".":
            start += 1
            continue
        size = 0
        while True:
            if start + size >= len(disk_map):
                break
            if disk_map[start + size] != ".":
                break
            size += 1
        if filesize <= size:
            return start
        start += size


def compact(disk_map):
    """Compact the disk"""
    free = 0
    file = len(disk_map) - 1
    step = 0
    while True:
        while disk_map[free] != ".":
            free += 1
        while not isinstance(disk_map[file], int):
            file -= 1
        if free >= file:
            break
        disk_map[free] = disk_map[file]
        disk_map[file] = "."
        step += 1

    checksum = calc_checksum(disk_map)
    return checksum


def compact_whole(disk_map, files):
    """Compact the disk using only whole files"""
    for fid, start, size in files:
        free = find_slice(disk_map, size)
        if free and free < start:
            for i in range(size):
                disk_map[free + i] = fid
                disk_map[start + i] = "."

    return calc_checksum(disk_map)


disk_map = parse_disk_map(disk_map_input)
files = find_files(disk_map)
print(compact(disk_map))
print(compact_whole(disk_map, files))
