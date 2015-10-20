import ast
import itertools


class Sentence:
    def __init__(self, clauses):
        self.clauses = {c for c in clauses}

    def __eq__(self, other):
        return other.clauses == self.clauses

    def __repr__(self):
        return str((str(self.clauses)))

    def __hash__(self):
        return hash(repr(self))

    def __ror__(self, other):
        return self.clauses | other


def negate(x):
    assert(isinstance(x, str))

    if x[0] == '~':
        return x[1:]
    else:
        return "~" + x


def resolve(sen_a, sen_b):

    resolvents = set()

    for (x, y) in itertools.product(list(sen_a.clauses), list(sen_b.clauses)):
        if x == negate(y):
            step = list((sen_a.clauses - {x}) | (sen_b.clauses - {y}))

            if not step:
                resolvents |= {None}
            else:
                resolvents |= {Sentence(step)}

    return resolvents


def resolution(kb, alpha):
    clauses = kb | {Sentence([negate(alpha)])}
    new = set()

    while True:
        for clause_a, clause_b in itertools.combinations(clauses, 2):
            resolvents = resolve(clause_a, clause_b)

            if None in resolvents:
                return False
            new |= resolvents
        if clauses.issuperset(new):
            return [str(clause) for clause in list(set(clauses))]
        clauses |= new


def main():

    cnf = ast.literal_eval("[[('not', 'Mythical'), ('not', 'Mortal')], ['Mythical', 'Mortal'], ['Mythical', 'Mammal'], ['Mortal', 'Horned'], [('not', 'Mammal'), 'Horned'], [('not', 'Horned'), 'Magical']]")

    kb = set()

    for clause in cnf:
        add = []

        for sen in clause:
            if isinstance(sen, tuple):
                add.append(negate(sen[1]))
            else:
                add.append(sen)
        kb |= {Sentence(add)}

    print(resolution(kb, 'Horned'))
    print(resolution(kb, 'Magical'))
    print(resolution(kb, 'Mythical'))


if __name__ == '__main__':
    main()
