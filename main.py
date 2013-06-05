import sys
import nltk
from curses.ascii import isdigit
from nltk.corpus import cmudict
import nltk.data
import pprint
import string

'''
	At the bottom of all this is if __name__ == '__main__'
	The main routine is in main(filename), the first defined function.
	In makeWords function, I make each word into a dict that consists
	of:
		word 	--	the word
		low		--	int minimum syllable count for the word
		high	--	int maximum syllable count for the word
		repl 	--	bool whether a character replacement was made
					--	maybe this should include what was replaced
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

##				main
def main(filename):
	'''
	Main routine. Input is string filename (defined at call)
	or the default: "sample.txt"
	'''
	printBlank(1, 'entering main') ## debug
	poem = [] #the poem, by line, will go here
	poem = openFile(poem, filename)
	poem = makeWords(poem)
	procLine(poem)

## output
	i = 0
	for p in poem:
		print poem[i]
		for word in poem[i]:
			print word['word'].lower(), word['low'], word['high'], word['repl'], word['inDict']
		i = i+1

def procLine(poem):
	'''
		Recieves poem (the full poem)
		Checks each word in the poem
	'''
	for line in poem:
		for w in line:
			w['inDict'] = checkDict(w)
			if w['inDict']:
				getSyl(w)

def checkDict(word):
	'''
		Takes word (a dict). Returns a boolean.
		Checks the word['word'] for existence in the CMU dict.
	'''
	found = True
	lowercase = word['word'].lower()
	if lowercase not in CMU:
		found = False
	return found

def makeWords(poem):
	'''
		Takes list poem. Returns a list, tempPoem (a list of dicts).
		Function iterates through poem, line by line, converting each
		word of the poem into a python dict composed of:
			word: word as string
			low: minimum syl count
			high: minimum syl count
	'''
	tempPoem = []
	for line in poem:
		tempLine = []
		for word in line:
			temp = dict(word='', low=0, high=0, repl=False, inDict=False)
			temp['word'] = word
			tempLine.append(temp)
		tempPoem.append(tempLine)
	return tempPoem


def openFile(poem, filename):
	'''
		poem(list poem, string filename)
		Opens the filename, reads the lines, tokenizes,
		while removing everything in EXCLUDE, and then
		stores it all in, and returns, "poem."
	'''
	f = open(filename)
	data = f.readlines()
	for datum in data:
		datum = ''.join(ch for ch in datum if ch not in EXCLUDE)
		temp = nltk.WhitespaceTokenizer().tokenize(datum)
		poem.append(temp)
	return poem


def printBlank(num, message):
	''' Takes an integer and a message to print to screen for spacing
	and/or debugging. '''
	for x in xrange(1,num):
		print '---------------------- ',message,' ---------------------'

## main
if __name__ == '__main__':
	if len(sys.argv) < 2:
		filename = 'sample.txt'
	elif len(sys.argv) >= 2:
		filename = sys.argv[1]
	print '*** Using ', filename, ' ***'
	sys.exit(main(filename))