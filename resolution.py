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

    def truth_outcomes(self):
        truth_vars = list(self.get_vars())
        truth_vars.sort()

        truth_table = list(itertools.product([True, False], repeat=len(truth_vars)))

        outcomes = []

        for i in range(len(truth_table)):
            var_dict = dict([(truth_vars[v], truth_table[i][v]) for v in range(len(truth_vars))])
            outcomes.append(self.evaluate_truth(var_dict))

        return outcomes

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
        elif self.operator == '->':
            return not truth[0] or truth[1]
        elif self.operator == '<->':
            return truth[0] == truth[1]
        elif self.operator == 'not':
            return not truth[0]

    def depth(self, l):
        if isinstance(l, list):
            return 1 + max(self.depth(item) for item in l)
        else:
            return 0

    def __str__(self):
        ret = [self.operator]
        ret.extend(str(component) for component in self.components)
        return str(ret)


def conjunctive_normal_form(sentence):

    if isinstance(sentence, str):
        return sentence

    for i in range(1, len(sentence)):
        sentence[i] = conjunctive_normal_form(sentence[i])

    operator = sentence[0]

    if operator == 'not':
        sub_sentence = sentence[1]

        if len(sub_sentence) > 1:

            if sub_sentence[0] == 'not':
                return sub_sentence[1]

            elif sub_sentence[0] == 'and':
                simplified = ['or']

                for atomic_sentence in sub_sentence[1:]:
                    simplified.append(conjunctive_normal_form(['not', atomic_sentence]))

                return simplified

            elif sub_sentence[0] == 'or':
                simplified = ['and']

                for atomic_sentence in sub_sentence[1:]:
                    simplified.append(conjunctive_normal_form(['not', atomic_sentence]))
                return simplified
        else:
            return sentence

    elif operator == '->':
        a = conjunctive_normal_form(['not', sentence[1]])
        b = conjunctive_normal_form(sentence[2])

        return ['or', a, b]

    return sentence


def resolve(knowledge_base, alpha):

    kb_outcomes = knowledge_base.truth_outcomes()
    knowledge_base.components.append(AtomicSentence(['not', alpha]))
    s_outcomes = knowledge_base.truth_outcomes()

    for i in range(len(kb_outcomes)):
        if kb_outcomes[i] and not s_outcomes[i]:
            return False

    return True


def main():
    """
    If the unicorn is mythical, then it is immortal, but if it is not mythical, then it is a mortal mammal. If the
    unicorn is either immortal or a mammal, then it is horned. The unicorn is magical if it is horned.
    """

    knowledge_base = [
        "['->', 'Mythical', 'Immortal']",                               # Mythical -> Immortal
        "['->', ['not', 'Mythical'], ['and', 'Mortal', 'Mammal']]",     # ~Mythical -> Mortal ^ Mammal
        "['->', ['or', 'Immortal', 'Mammal'], 'Horned']",               # (Immortal v Mammal) -> Horned
        "['->', 'Horned', 'Magical']"                                   # Horned -> Magical
    ]

    kb = ['and']

    for statement in knowledge_base:
        kb.append(ast.literal_eval(statement))

    cnf_kb = conjunctive_normal_form(kb.copy())

    print(kb)
    print(cnf_kb)

    knowledge_base = AtomicSentence(kb)
    cnf_kb = AtomicSentence(cnf_kb)

    #print(knowledge_base.truth_outcomes() == cnf_kb.truth_outcomes())

    tests = [
        'Horned',   # The unicorn is horned.
        'Magical',  # The unicorn is magical.
        'Mythical'  # The unicorn is mythical.
    ]

    for test in tests:
        print(resolve(knowledge_base, test))


if __name__ == '__main__':
    main()
