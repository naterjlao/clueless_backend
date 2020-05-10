#!/usr/bin/python3
# Functional Regression test for accusations and suggestions
import sys
sys.path.append('..')

from testing_utils import *
from cards import *
from game import *
from gameboard import *
from globals import *
from players import *
from utils import *
l = Logger()

s = Suggestion(None,"Bob","spoon","bathroom",l)

assertTrue(s.counter("Bob"))
assertTrue(s.counter("spoon"))
assertTrue(s.counter("bathroom"))
assertFalse(s.counter("Martha"))
assertFalse(s.counter("fork"))
assertFalse(s.counter("restroom"))


c = CaseFile(Card("Bob",l),Card("spoon",l),Card("bathroom",l),l)
a = Accusation(None,"Bob","spoon","bathroom",l)

assertTrue(a.counter("Bob"))
assertTrue(a.counter("spoon"))
assertTrue(a.counter("bathroom"))
assertFalse(a.counter("Martha"))
assertFalse(a.counter("fork"))
assertFalse(a.counter("restroom"))

assertTrue(a.checkCasefile(c))

a = Accusation(None,"Bob","spoon","restroom",l)
assertFalse(a.checkCasefile(c))
a = Accusation(None,"Bob","fork","bathroom",l)
assertFalse(a.checkCasefile(c))
a = Accusation(None,"Martha","spoon","bathroom",l)
assertFalse(a.checkCasefile(c))

