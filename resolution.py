import ast
import itertools


class Sentence:
    def __init__(self, sentence):
        self.terms = list()
        for term in sentence:

            if isinstance(term, tuple):
                self.terms.append("~{}".format(term[1]))
            else:
                self.terms += [term]

    def remove(self, item):
        self.terms.remove(item)

    #def __str__(self):
    #    return str(str(self.terms))

    def __contains__(self, item):
        return item in self.terms

    def __eq__(self, other):

        if isinstance(other, Sentence):
            return self.terms == other.terms
        if isinstance(other, str):
            return self.terms[0] == other

    def __repr__(self):
        return str(str(self.terms))

    __hash__ = lambda self: hash(repr(self))


def negate(sentence):

    if sentence[0] == '~':
        return sentence[1:]
    else:
        return '~' + sentence


def resolve(sen_a, sen_b):

    if isinstance(sen_a, Sentence):
        sen_a = sen_a.terms
    if isinstance(sen_b, Sentence):
        sen_b = sen_b.terms
    if isinstance(sen_a, str):
        sen_a = [sen_a]
    if isinstance(sen_b, str):
        sen_b = [sen_b]

    literals = sen_a + sen_b
    resolvents = []

    resolution_occured = False

    for (x, y) in itertools.combinations(literals, 2):
        if x == negate(y):
            resolution_occured = True
            resolvents += (set(literals) - {x, negate(x)})

    if resolution_occured:
        return resolvents
    else:
        return list(set(literals))


def resolution(kb, alpha):

    clauses = kb | {Sentence((('not', alpha),('not', alpha)))}
    new = set()
    while True:
        for clause_a, clause_b in itertools.combinations(clauses, 2):

            resolvents = resolve(clause_a, clause_b)
            #print(clause_a, clause_b, resolvents)

            if [] in resolvents:
                return True
            new |= set(resolvents)
        if clauses.issuperset(new):
            return [str(clause) for clause in list(set(clauses))]
        clauses |= new


def main():

    cnf = ast.literal_eval("[[('not', 'Mythical'), ('not', 'Mortal')], ['Mythical', 'Mortal'], ['Mythical', 'Mammal'], ['Mortal', 'Horned'], [('not', 'Mammal'), 'Horned'], [('not', 'Horned'), 'Magical']]")

    knowledge_base = set()

    for sen in cnf:
        knowledge_base |= {Sentence(sen)}

    print(resolution(knowledge_base, 'Horned'))
    print(resolution(knowledge_base, 'Magical'))
    print(resolution(knowledge_base, 'Mythical'))

if __name__ == '__main__':
    main()
