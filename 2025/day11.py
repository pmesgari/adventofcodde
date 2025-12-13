from functools import cache


def parse_input():
    """
    Parse the devices and connections into a graph
    returns:
    - graph: Dict[str, List[str]]
    """

    with open(0, encoding="utf-8") as f:
        graph = {}
        for line in f:
            node, edges = line.split(":")
            graph[node] = edges.strip().split(" ")

        return graph


def part1(graph):
    def _count_paths(current_node):
        """
        Count all the paths to target from current node
        returns:
        - paths_count: int
        """

        if current_node == "out":
            return 1
        if current_node not in graph:
            return 0

        count = 0
        for n in graph[current_node]:
            count += _count_paths(n)

        return count

    print(_count_paths("you"))


def part2(graph):
    def get_segment_count(start_node, end_node):
        @cache
        def _count_paths(current_node):
            """
            Count all the paths to target from current node
            returns:
            - paths_count: int
            """

            if current_node == end_node:
                return 1
            if current_node not in graph:
                return 0

            count = 0
            for n in graph[current_node]:
                count += _count_paths(n)

            return count

        _count_paths.cache_clear()
        return _count_paths(start_node)

    leg1 = get_segment_count("svr", "dac")
    leg2 = get_segment_count("dac", "fft")
    leg3 = get_segment_count("fft", "out")

    leg4 = get_segment_count("svr", "fft")
    leg5 = get_segment_count("fft", "dac")
    leg6 = get_segment_count("dac", "out")

    print((leg1 * leg2 * leg3) + (leg4 * leg5 * leg6))


graph = parse_input()
part1(graph)
part2(graph)
