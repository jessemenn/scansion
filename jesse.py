
## -- jesse.py -- ##
## -- functions -- ##
from settings import *

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
		Takes string (such as something['word']). Returns a boolean.
		Checks for existence of string in the CMU dict.
	'''
	found = True
	if word not in CMU:
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
			temp['word'] = word.lower()
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
