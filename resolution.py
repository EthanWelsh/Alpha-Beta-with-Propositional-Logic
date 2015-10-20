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

    def __str__(self):
        return str(str(self.terms))

    def __contains__(self, item):
        return item in self.terms


def negate(sentence):

    if sentence[0] == '~':
        return sentence[1:]
    else:
        return '~' + sentence


def resolve(sen_a, sen_b):

    set_a = set()
    set_b = set()

    for a in sen_a.terms:
        set_a |= {a}

    for b in sen_b.terms:
        set_b |= {b}

    neg_a = {negate(a) for a in sen_a.terms}
    neg_b = {negate(b) for b in sen_b.terms}

    return Sentence(list((set_a - neg_b) | (set_b - neg_a)))


def resolution(kb, alpha):

    alpha = Sentence(negate(alpha))
    clauses = kb | {alpha}

    new = set()
    while True:
        for clause_a, clause_b in itertools.combinations(clauses, 2):
            resolvents = resolve(clause_a, clause_b)
            if [] in resolvents:
                return True
            new |= {resolvents}
        if clauses.issuperset(new):
            return False
        clauses |= new


def main():

    cnf = ast.literal_eval("[[('not','mythical'),('not','mortal')],"
                                          "['mythical','mortal'],"
                                          "['mythical','mammal'],"
                                          "[('not','immortal'),'horned'],"
                                          "[('not','mammal'),'horned'],"
                                          "[('not','horned'),'magical']]")

    knowledge_base = set()

    for sen in cnf:
        knowledge_base |= {Sentence(sen)}

    #print(resolution(knowledge_base, 'horned'))
    #print(resolution(knowledge_base, 'magical'))
    #print(resolution(knowledge_base, 'mythical'))

    a = Sentence(('p', 'q'))
    b = Sentence((('not', 'p'), 'r'))

    print(a)
    print(b)

    res = resolve(a, b)
    print(res)

    #print(res)

if __name__ == '__main__':
    main()
