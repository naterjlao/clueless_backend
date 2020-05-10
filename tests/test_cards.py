#!/usr/bin/python3
# Functional Regression test for cards
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

p = Player("Ash",l)
p1 = Player("loser",l)
c = Card("Blue Eyes White Dragon",l)

assertTrue(c.getOwner() == CARD_UNASSIGNED)
assertTrue(c.isUnassigned())

c.assignTo(p)
assertTrue(c.getOwner() == p)
assertFalse(c.isUnassigned())

try:
	c.assignTo(p1)
	assertTrue(False)
except:
	assertTrue(True)

