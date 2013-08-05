'''
DEFINTIONS:
LINE: dict(line=[], lower=0, upper=0, blank=False, stressArray=[])
WORD: dict(word='', low=0, high=0, repl=False, inDict=False, stress=[])
POEM: dict()
'''

import nltk
from curses.ascii import isdigit
from nltk.corpus import cmudict
import nltk.data
import string
import sys
import pprint
import string
from copy import deepcopy

'''
	Settings file with:
		import library statements
		global constant defintions
'''

VOWELS = ['a', 'e', 'i', 'o', 'u', 'y']

DIPHTHONGS = ['aa', 'ae', 'ai', 'ao', 'au',
              'ea', 'ee', 'ei', 'eo', 'eu',
              'ia', 'ie', 'ii', 'io', 'iu',
              'oa', 'oe', 'oi', 'oo', 'ou'
              'ua', 'ue', 'ui', 'uo', 'uu']

CMU = cmudict.dict()

TOKENIZER = nltk.data.load('tokenizers/punkt/english.pickle')

'''
Exclude all string.punctuation except apostrophe,
and hyphen.
'''
EXCLUDE = set('!"#$%&()*+,./:;<=>?@[\\]^_`{|}~')


# Chances are these words should never be stressed.
UNSTRESSED = 'a an of the am and n for in is on or that to with'.split()
UNSTRESSED+= 'are as be by he him is her my she them em us we'.split()
UNSTRESSED+= 'its they their were you your'.split()
UNSTRESSED+= 'at do did from i it me but had has have our shall was will'.split()
UNSTRESSED+= 'dost hast hath shalt thee thou thy wilt ye'.split()
UNSTRESSED+= 'if how what when where who why can so this though which'.split()
UNSTRESSED+= 'could should would all like nor out too yet near through while whose'.split()
UNSTRESSED+= 'these those came come none one two three four five six eight nine ten'.split()
UNSTRESSED+= 'ah en et la may non off per re than un his'.split()

# Disyllable and trisyllable poetic meters...
PYRRHUS = [-1, -1]
IAMB = [-1, 1]
TROCHEE = [1, -1]
SPONDEE = [1, 1]
TRIBRACH = [-1, -1, -1]
DACTYL = [1, -1, -1]
AMPHIBRACH = [-1, 1, -1]
ANAPEST = [-1, -1, 1]
BACCHIUS = [-1, 1, 1]
ANTIBACCHIUS = [1, 1, -1]
CRETIC = [1, -1, 1]
MOLOSSUS = [1, 1, 1]

MONOMETER = 1
DIMETER = 2
TRIMETER = 3
TETRAMETER = 4
PENTAMETER = 5
HEXAMETER = 6
HEPTAMETER = 7
OCTAMETER = 8 


#temporary possible forms:
pyrhic_penta = PYRRHUS * PENTAMETER
iambic_penta = IAMB * PENTAMETER
trochaic_penta = TROCHEE * PENTAMETER
pyrhic_tetra = PYRRHUS * TETRAMETER
iambic_tetra = IAMB * TETRAMETER
trochaic_tetra = TROCHEE * TETRAMETER