import pdb


class TrieNode:
    def __init__(self, parent=None):
        self.children = {}
        self.is_end_of_word = False
        self.parent = parent


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode(node)
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node


class AdjacencyGraphEdge:
    def __init__(self, to, weight):
        self.to = to
        self.weight = weight


class AdjacencyGraph:
    def __init__(self):
        self.edges = {}
        self.in_degree = {}
        self.out_degree = {}

    def add_edge(self, from_node, to_node, weight):
        if from_node not in self.edges:
            self.edges[from_node] = []
        self.edges[from_node].append(AdjacencyGraphEdge(to_node, weight))

        if from_node not in self.out_degree:
            self.out_degree[from_node] = 0
        if to_node not in self.in_degree:
            self.in_degree[to_node] = 0

        self.out_degree[from_node] += 1
        self.in_degree[to_node] += 1

    def get_longest_path(self):
        def dfs(node, current_path, current_length, visited, stack):
            if node in stack:  # Cycle detected
                return [], 0

            if node in visited:
                return visited[node]

            max_path = current_path.copy()
            max_length = current_length

            stack.add(node)

            for edge in self.edges.get(node, []):
                new_path = current_path + [edge.to]
                new_length = current_length + edge.weight
                result_path, result_length = dfs(edge.to, new_path, new_length, visited, stack)

                if result_length > max_length:
                    max_path = result_path
                    max_length = result_length

            stack.remove(node)
            visited[node] = (max_path, max_length)
            return max_path, max_length

        visited = {}
        longest_paths = []
        for node in self.edges.keys():
            if self.in_degree.get(node, 0) == 0:
                stack = set()
                path, length = dfs(node, [node], 0, visited, stack)
                longest_paths.append((path, length))

        longest_paths.sort(key=lambda x: x[1], reverse=True)
        if len(longest_paths) > 0:
            return longest_paths[0]
        return []


class FragmentOverlap:
    def __init__(self, fragment, overlapping_characters):
        self.fragment = fragment
        self.overlapping_characters = overlapping_characters


def build_prefix(end_node):
    reversed_prefix = ''
    node = end_node
    while node and node.parent:
        parent_node = node.parent
        for ch, child_node in parent_node.children.items():
            if child_node == node:
                reversed_prefix += ch
                node = parent_node
                break
    return reversed_prefix[::-1]


def dump_branch_words(node):
    if not node:
        return []

    branch_words = []
    for ch, child_node in node.children.items():
        child_branches = dump_branch_words(child_node)
        if child_branches:
            for branch in child_branches:
                branch_words.append(ch + branch)
        else:
            branch_words.append(ch)

    return branch_words


def calculate_node_depth(node):
    depth = 0
    while node.parent:
        depth += 1
        node = node.parent
    return depth


def build_trie(fragments):
    trie = Trie()
    for fragment in fragments:
        trie.insert(fragment)

    return trie


def search_overlaps(trie, fragment, overlap_limit):
    overlaps = []
    for i in range(1, len(fragment) - overlap_limit + 1):
        suffix = fragment[i:]
        overlapping_end_node = trie.search(suffix)
        if overlapping_end_node:
            branch_words = dump_branch_words(overlapping_end_node)
            overlapping_characters = calculate_node_depth(overlapping_end_node)

            for branch_word in branch_words:
                overlaps.append(FragmentOverlap(suffix + branch_word, overlapping_characters))
        break

    return overlaps


def build_adjacency_graph(trie, fragments, overlap_limit):
    adjacency_graph = AdjacencyGraph()
    for fragment in fragments:
        overlaps = search_overlaps(trie, fragment, overlap_limit)
        for overlap in overlaps:
            adjacency_graph.add_edge(fragment, overlap.fragment, overlap.overlapping_characters)

    return adjacency_graph


if __name__ == '__main__':
    FRAGMENTS = ['AABABBA', 'ABABBAC', 'ABABBAG', 'BABBACE', 'ABBACET']
    OVERLAP_LIMIT = 4
    trie = build_trie(FRAGMENTS)
    adjacency_graph = build_adjacency_graph(trie, FRAGMENTS, OVERLAP_LIMIT)
    print(adjacency_graph.get_longest_path())