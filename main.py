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

	for line in poem: 
		procLine(line)

# ## output
# 	i = 0
# 	for p in poem:
# 		print poem[i]
# 		for word in poem[i]:
# 			print word['word'], word['low'], word['high'], word['repl'], word['inDict']
# 		i = i+1

def procLine(line):
	'''
		Recieves line of poem
		Checks each word in the line
	'''
	for w in line:
		w['inDict'] = checkDict(w)
		if (w['inDict'] == True):
			getSyl(w)
		elif (w['inDict'] == False):
			temp = w['word'][:-1]
	print line
def getSyl(word):
	'''
		Takes dictionary "word." Finds min/max syl count.
		Stores results in word['low'] and word['high'], respectively.
		If in CMU, use that. Otherwise, use dumbGuess.
	'''
	lowercase = word['word'].lower()
	if (word['inDict']):
		word['low'] = min([len([y for y in x if isdigit(y[-1])]) for x in CMU[lowercase]])
		word['high'] = max([len([y for y in x if isdigit(y[-1])]) for x in CMU[lowercase]])

def replaceHyphen(wordA, wordB):
	'''
		Recieves two 'word' as dict, wordB is blank.
		Called from makeWords.
		Replaces hyphen with a space. Returns two values, the words pre/post-hyphen
		Note, this is really clumsy... replace hyphen in A with a space. Set temp
			to the split word. Split it at the space (thus making a list?). Set 
			wordA to 1st item of temp; wordB to 2nd item. Return both words (as dict)
	'''
	for punct in set('-'):
		wordA['word'] = wordA['word'].replace(punct, ' ')
	temp = wordA['word']
	temp = temp.split(' ')
	wordA['word'] = temp[0]
	wordB['word'] = temp[1]
	return wordA, wordB

def replaceStuff(word):
	'''
		Takes word (as dict).
		Modifies the dictionary as needed.
		Replaces: 'd endings with ed; 'n with en;
	'''
	temp = word['word'] #store original word to check if we replaced
	if (len(word['word']) > 1):
		if ((word['word'][-2] == "'")):
			if ((word['word'][-1] == "d") or (word['word'][-1] == "n")): # ends in 'd, 'n
				word['word'] = word['word'].replace(word['word'][-2], 'e')
		for punct in string.punctuation:
			word['word'] = word['word'].replace(punct, "") ## strip any other punctuation
	if (word['word'] == temp): ## did we replace anything?
		word['repl'] = False
	else:
		word['repl'] = True

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
			repl: if something's been replaced (like a 'd)
			inDict: if the word is in the dictionary
	'''
	tempPoem = []
	for line in poem:
		tempLine = []
		for word in line:
			temp = dict(word='', low=0, high=0, repl=False, inDict=False)
			temp['word'] = word
			if '-' in temp['word']:
				tempX = dict(word='', low=0, high=0, repl=False, inDict=False)
				temp, tempX = replaceHyphen(temp, tempX)
					# see replaceHyphen function for description
				replaceStuff(temp)
				replaceStuff(tempX)
				tempLine.append(temp)
				tempLine.append(tempX)
			else:
				replaceStuff(temp)
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