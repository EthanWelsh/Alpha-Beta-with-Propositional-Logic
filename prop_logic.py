import ast
import itertools


class AtomicSentence:
    def __init__(self, sentence):
        self.operator = sentence[0]
        self.components = []

        for component in sentence[1:]:
            if self.depth(component) == 0:
                self.components.append(component)
            else:
                self.components.append(AtomicSentence(component))

    def model_check(self):
        truth_vars = list(self.get_vars())
        truth_table = list(itertools.product([True, False], repeat=len(truth_vars)))

        outcomes = []

        for i in range(len(truth_table)):
            var_dict = dict([(truth_vars[v], truth_table[i][v]) for v in range(len(truth_vars))])
            outcomes.append(self.evaluate_truth(var_dict))

        return not any(outcomes), any(outcomes) and not all(outcomes), all(outcomes)

    def get_vars(self):

        variables = []

        for component in self.components:
            if isinstance(component, str):
                variables.append(component)
            else:
                variables.extend(component.get_vars())

        return set(variables)

    def evaluate_truth(self, var_dict):

        truth = []
        for component in self.components:
            if isinstance(component, str):
                truth.append(var_dict[component])
            else:
                truth.append(component.evaluate_truth(var_dict))

        if self.operator == 'or':
            return any(truth)
        elif self.operator == 'and':
            return all(truth)
        elif self.operator == 'xor':
            return not all(truth) and any(truth)
        elif self.operator == 'not':
            return not truth[0]

    def depth(self, l):
        if isinstance(l, list):
            return 1 + max(self.depth(item) for item in l)
        else:
            return 0


def main():
    tree = ast.literal_eval("['or', ['or', 'Smoke', 'Fire'], ['not', 'Fire']]")
    atomic = AtomicSentence(tree)

    unsatisfiable, satisfiable, valid = atomic.model_check()

    print("unsatisfiable:", unsatisfiable)
    print("satisfiable:", satisfiable)
    print("valid:", valid)


if __name__ == '__main__':
    main()
