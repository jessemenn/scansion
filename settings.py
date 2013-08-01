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
PYRRHUS = ['0','0']
IAMB = ['0','1']
TROCHEE = ['1','0']
SPONDEE = ['1', '1']
TRIBRACH = ['0','0','0']
DACTYL = ['1','0','0']
AMPHIBRACH = ['0', '1', '0']
ANAPEST = ['0', '0', '1']
BACCHIUS = ['0', '1', '1']
ANTIBACCHIUS = ['1', '1', '0']
CRETIC = ['1', '0', '1']
MOLOSSUS = ['1', '1', '1']
