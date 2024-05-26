class TrieNode:
    def __init__(self):
        self.children = {}
        self.weight = 0
        self.is_end = False

    def __repr__(self):
        return f"TrieNode(weight={self.weight}, children={list(self.children.keys())})"


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, fragment):
        node = self.root
        for i in fragment:
            if i not in node.children:
                node.children[i] = TrieNode()
            node = node.children[i]
            node.weight += 1
        node.is_end = True

    def extract_paths(self, consensus, should_be_end_node=False):
        def dfs(node, prefix):
            paths = []
            for i, child in node.children.items():
                if child.weight >= consensus:
                    child_paths = dfs(child, prefix + i)
                    paths.extend(child_paths)
            if (not paths) and ((not should_be_end_node) or node.is_end):
                paths.append(prefix)
            return paths

        return dfs(self.root, '')

    def __repr__(self):
        def display(node, level=0):
            result = []
            for i, child in node.children.items():
                result.append(' ' * (2 * level) + f"{i}({child.weight})")
                result.extend(display(child, level + 1))
            return result

        return '\n'.join(display(self.root))


if __name__ == '__main__':
    EXTRACT_ONLY_FULL_PATHS = False

    consensus = int(input("Enter the consensus number: "))
    num_fragments = int(input("Enter the number of fragments: "))
    fragments = []
    for i in range(0, num_fragments):
        fragment = input()
        fragments.append(fragment)

    # Create a trie and insert DNA fragments
    trie = Trie()
    for fragment in fragments:
        trie.insert(fragment)

    print("Trie structure:")
    print(trie)

    # Extract paths with the provided consensus
    paths = trie.extract_paths(consensus, EXTRACT_ONLY_FULL_PATHS)
    print(f"Paths with edge weight >= {consensus}:")
    print(paths)