import ast


def conjunctive_normal_form(sentence):

    if isinstance(sentence, str):
        return sentence

    operator = sentence[0]

    if operator == 'not':
        sub_sentence = sentence[1]

        if len(sub_sentence) > 1:

            if sub_sentence[0] == 'not':
                return sub_sentence[1]

            elif sub_sentence[0] == 'and':
                simplified = ['or']

                for atomic_sentence in sub_sentence[1:]:
                    atomic_sentence = conjunctive_normal_form(atomic_sentence)
                    simplified.append(['not', atomic_sentence])

                return simplified

            elif sub_sentence[0] == 'or':
                simplified = ['and']

                for atomic_sentence in sub_sentence[1:]:
                    atomic_sentence = conjunctive_normal_form(atomic_sentence)
                    simplified.append(['not', atomic_sentence])
                return simplified
        else:
            return sentence

    elif operator == '->':
        a = conjunctive_normal_form(['not', sentence[1]])
        b = conjunctive_normal_form(sentence[2])

        return ['or', a, b]
    elif operator == 'Xor':
        thrift = []
        for index, outer in enumerate(sentence[1:]):
            if outer[0] == 'or':
                for inner in outer[1:]:
                    sentence.extend(inner)

                sentence.remove(index)

            if outer[0] == 'and':
                for inner in outer[1:]:
                    thrift.append(inner)

        distributed = ['or']

        for outer in thrift:
            for inner in thrift:
                if outer != inner and not (['and', outer, inner] in distributed or ['and', inner, outer] in distributed):
                    distributed.append(['and', outer, inner])

        return distributed

    elif operator == 'Xand':
        thrift = []
        for index, outer in enumerate(sentence[1:]):
            if outer[0] == 'and':
                for inner in outer[1:]:
                    sentence.extend(inner)

                sentence.remove(index)

            if outer[0] == 'or':
                for inner in outer[1:]:
                    thrift.append(inner)

        distributed = ['and']

        for outer in thrift:
            for inner in thrift:
                if outer != inner and not (['or', outer, inner] in distributed or ['or', inner, outer] in distributed):
                    distributed.append(['or', outer, inner])

        return distributed

    return sentence




def resolve(knowledge_base, test):
    pass


if __name__ == '__main__':

        """
        If the unicorn is mythical, then it is immortal, but if it is not mythical, then it is a mortal mammal. If the
        unicorn is either immortal or a mammal, then it is horned. The unicorn is magical if it is horned.
        """

        knowledge_base = [
            "['->', 'Mythical', 'Immortal']",                           # Mythical -> Immortal
            "['->', ['not', 'Mythical'], ['and', 'Mortal', 'Mammal']]",   # ~Mythical -> Mortal ^ Mammal
            "['->', ['or', 'Immortal', 'Mammal'], 'Horned']",           # (Immortal v Mammal) -> Horned
            "['->', 'Horned', 'Magical']"                                # Horned -> Magical
        ]

        for sentence in knowledge_base:
            print(conjunctive_normal_form(ast.literal_eval(sentence)))


        test = [
            'Horned',   # The unicorn is horned.
            'Magical',  # The unicorn is magical.
            'Mythical'  # The unicorn is mythical.
        ]
