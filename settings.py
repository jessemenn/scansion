'''
DEFINTIONS:
LINE: dict(line=[], lower=0, upper=0, blank=False)
WORD: dict(word='', low=0, high=0, repl=False, inDict=False)
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

EXCLUDE = set('!"#$%&()*+,./:;<=>?@[\\]^_`{|}~')
'''
Exclude all string.punctuation except apostrophe,
and hyphen.
'''