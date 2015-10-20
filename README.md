# A-Propositional-Logic

Alpha Beta
----------
```
python alpha_beta.py "['A', ['B', ('D', 3), ('E', 5)], ['C', ['F', ['I',('K',0), ('L', 7)], ('J',5)], ['G', ('M',7), ('N',8)], ('H',4)]]"
(4, 12)

python alpha_beta.py "['A', ['B', ['D', ('H', 6), ('I', 5)], ['E', ('J', 8), ('K',7)]], ['C', ['F', ('L',2), ('M',1)], ['G',('N',4), ('O',3)]]]"
(6, 11)

python alpha_beta.py "['A', ['B', ['E', ('L', 2), ('M', 3)], ['F', ('N', 8), ('O', 5)], ['G', ('P', 7), ('Q', 6)]], ['C', ['H', ('R', 0), ('S', 1)], ['I', ('T', 5), ('U', 2)]], ['D', ['J', ('V', 8), ('W', 4)], ['K', ('X', 10), ('Y', 2)]]]"
(8, 19)
```

Model Check
-----------

```
python model_check.py "['->', 'Smoke', 'Smoke']"
('Unsatisfiable:', False)
('Satisfiable:', False)
('Valid:', True)

python model_check.py "['->', 'Smoke', 'Fire']"
('Unsatisfiable:', False)
('Satisfiable:', True)
('Valid:', False)

python model_check.py "['->', ['->', 'Smoke', 'Fire'], ['->', ['not', 'Smoke'], ['not', 'Fire']]]"
('Unsatisfiable:', False)
('Satisfiable:', True)
('Valid:', False)

python model_check.py "['or', 'Smoke', 'Fire', ['not', 'Fire']]"
('Unsatisfiable:', False)
('Satisfiable:', False)
('Valid:', True)

python model_check.py "['<->', ['->', ['and', 'Smoke', 'Heat'], 'Fire'], ['or', ['->', 'Smoke', 'Fire'], ['->', 'Heat', 'Fire']]]"
('Unsatisfiable:', False)
('Satisfiable:', False)
('Valid:', True)

python model_check.py "['->', ['->', 'Smoke', 'Fire'], ['->', ['and', 'Smoke', 'Heat'], 'Fire']]"
('Unsatisfiable:', False)
('Satisfiable:', False)
('Valid:', True)

python model_check.py "['or', 'Big', 'Dumb', ['->', 'Big', 'Dumb']]"
('Unsatisfiable:', False)
('Satisfiable:', False)
('Valid:', True)
```

Resolution
----------
```
python resolution.py "[[('not', 'Mythical'), ('not', 'Mortal')], ['Mythical', 'Mortal'], ['Mythical', 'Mammal'], ['Mortal', 'Horned'], [('not', 'Mammal'), 'Horned'], [('not', 'Horned'), 'Magical']]" "Horned"
False

python resolution.py "[[('not', 'Mythical'), ('not', 'Mortal')], ['Mythical', 'Mortal'], ['Mythical', 'Mammal'], ['Mortal', 'Horned'], [('not', 'Mammal'), 'Horned'], [('not', 'Horned'), 'Magical']]" "Magical"
False

python resolution.py "[[('not', 'Mythical'), ('not', 'Mortal')], ['Mythical', 'Mortal'], ['Mythical', 'Mammal'], ['Mortal', 'Horned'], [('not', 'Mammal'), 'Horned'], [('not', 'Horned'), 'Magical']]" "Mythical"
["set(['~Mammal', 'Horned'])", "set(['Magical', 'Mythical'])", "set(['Mythical', '~Mythical'])", "set(['~Mortal', '~Mythical'])", "set(['~Mythical', 'Horned'])", "set(['Magical', '~Mythical'])", "set(['Magical', 'Horned'])", "set(['Mammal', 'Horned'])", "set(['Mammal', 'Magical'])", "set(['Mythical', 'Horned'])", "set(['Mammal'])", "set(['~Horned', 'Magical'])", "set(['~Mortal', 'Magical'])", "set(['Horned'])", "set(['Magical'])", "set(['~Mammal', 'Magical'])", "set(['~Mortal', 'Mammal'])", "set(['Mammal', 'Mythical'])", "set(['~Mortal', 'Horned'])", "set(['Mortal'])", "set(['~Mythical'])", "set(['Mythical', 'Mortal'])", "set(['Horned', '~Mythical'])", "set(['~Mortal', 'Mortal'])", "set(['Mythical', 'Magical'])", "set(['Horned', 'Mortal'])", "set(['Magical', 'Mortal'])"]
```
