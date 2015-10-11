import ast
import sys


class Tree:
    class Node:
        def __init__(self, letter, score=None):
            self.children = []
            self.letter = letter
            self.score = score

        def get_children(self):
            return self.children

        def __str__(self):
            return str(self.score)

    def __init__(self, tree):
        self.root = self.build_tree(tree)

    def build_tree(self, tree):
        if type(tree) is list:
            root = Tree.Node(tree[0])
            for child in tree[1:]:
                root.children.append(self.build_tree(child))
            return root
        elif type(tree) is tuple:
            return Tree.Node(*tree)

    def get_level(self, level_num, root=None, current_level=0):
        if root is None:
            if self.root is not None:
                root = self.root
            else:
                return

        if current_level == level_num:
            yield [root.letter]
        else:
            for child in root.children:
                yield from self.get_level(level_num, root=child, current_level=current_level + 1)


def main():
    tree = ast.literal_eval(sys.argv[1])
    spruce = Tree(tree)

    for i in range(5):
        print([x for x in spruce.get_level(i)])


if __name__ == '__main__':
    main()
