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

    def __init__(self, tree):
        self.root = self.build_tree(tree)
        self.visited_count = 0

    def build_tree(self, tree):
        if type(tree) is list:
            root = Tree.Node(tree[0])
            for child in tree[1:]:
                root.children.append(self.build_tree(child))
            return root
        elif type(tree) is tuple:
            return Tree.Node(*tree)

    def alpha_beta(self, root, alpha, beta, max_player):
        visited_count = 1

        if len(root.children) == 0:
            return root.score, visited_count

        if max_player:
            max_score = -sys.maxsize
            for child in root.children:
                child_score, children_visited = self.alpha_beta(child, alpha, beta, False)

                max_score = max(max_score, child_score)
                alpha = max(alpha, max_score)

                visited_count += children_visited

                if beta <= alpha:
                    break

            return max_score, visited_count
        else:
            min_score = sys.maxsize
            for child in root.children:
                child_score, children_visited = self.alpha_beta(child, alpha, beta, True)

                min_score = min(min_score, child_score)
                beta = min(beta, min_score)

                visited_count += children_visited

                if beta <= alpha:
                    break

            return min_score, visited_count


def main():
    tree = ast.literal_eval(sys.argv[1])
    spruce = Tree(tree)
    print(spruce.alpha_beta(spruce.root, -sys.maxsize, sys.maxsize, True))


if __name__ == '__main__':
    main()
