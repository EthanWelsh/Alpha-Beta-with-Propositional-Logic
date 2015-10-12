import ast


class AtomicSentence:
    def __init__(self, sentence):
        self.operator = sentence[0]
        self.components = []

        for component in sentence[1:]:
            if self.depth(component) == 0:
                self.components.append(component)
            else:
                self.components.append(AtomicSentence(component))

    def get_vars(self):

        variables = []

        for component in self.components:
            if isinstance(component, str):
                variables.append(component)
            else:
                variables.extend(component.get_vars())

        return set(variables)

    def evaluate(self, var_dict):

        truth = []
        for component in self.components:
            if isinstance(component, str):
                truth.append(var_dict[component])
            else:
                truth.append(component.evaluate(var_dict))

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
    print(atomic.get_vars())
    print(atomic.evaluate({'Smoke':False, 'Fire': False}))


if __name__ == '__main__':
    main()
