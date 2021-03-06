
## -- jesse.py -- ##
## -- functions -- ##

## -- contents of dictionary made in 'makeWords' -- ##

from settings import *

def getMerits(merits, forms, finalScores):
	'''
		Recieves blank dictionary, merits (agree/disagree/difference) and
			forms (dict of possible forms, each possible form a list).
		Fills in the values for the merits.
	'''
	for key in forms.keys():
		tester = forms[key]
		counter = 0
		for item in finalScores:
			if item == tester[counter]:
				#print "Slot: ", counter, " | ", "finalScores: ", item, " | ", "form: ", tester[counter], " agree!"
				merits['agree']	+= 1
			elif item != tester[counter]:
				#print "Slot: ", counter, " | ", "finalScores: ", item, " | ", "form: ", tester[counter], " DISAGREE"
				merits['disagree'] += 1
			counter += 1
		print key.ljust(15), "agreements: ", merits['agree'], " disagreements: ", merits['disagree'], "diff: ", (merits['agree']-merits['disagree'])
		merits['agree'] = 0
		merits['disagree'] = 0
		merits['difference'] = 0

def checkForms(finalScores):
	'''
		Receives finalScores from beginStress.
		Generates possible forms (generateForms)
		Checks against possible forms of poetic meter (iambic + pentameter for example).
		Calls merits.
		prints merits
		prints likely form
	'''
	maximum = len(finalScores)
	forms = {'pyrrhic': [], 'iambic': [], 'trochaic': [], 'spondaic': []}
	generateForms(maximum, forms)

	merits = {"agree": 0, "disagree": 0, "diff": 0}
	getMerits(merits, forms, finalScores)

def generateForms(maximum, forms):
	# we want feet, not syllables
	feet = maximum / 2

	# don't forget needa adjust for 3-syl feet
	forms['pyrrhic'] = PYRRHUS*feet
	forms['iambic'] = IAMB*feet
	forms['trochaic'] = TROCHEE*feet
	forms['spondaic'] = SPONDEE*feet
	forms['tribrachiac'] = TRIBRACH*feet
	forms['dactylic'] = DACTYL*feet
	forms['amphibrachiac'] = AMPHIBRACH*feet
	forms['anapestic'] = ANAPEST*feet
	forms['bacchiac'] = BACCHIUS*feet
	forms['antibacchiac'] = ANTIBACCHIUS*feet
	forms['creticac'] = CRETIC*feet
	forms['molossusiac'] = MOLOSSUS*feet

	if ((maximum % 2) == 1):
		for key in forms:
			forms[key].append(-1)

def prettyOutput(poem, wordCount=True, lineCount=True, numberLines=True, noteSubstitution=True,noteDictionary=False):
        '''
                Takes a poem, a list of special 'line' datatype as input. Prints it out in a readable format. Default is to include
                a line number, lower and upper bounds for syllable count of that line, and then each word from a line with lower/upper syllabe count in parentheses.
                outputting of counts for words or lines can be turned off by passing False to wordCount or lineCount respectively. 
                Line numbering can be turned off by passing numberLines=False.
                This function can also note whether or not that word has been corrected for a substition (with an asterisk) and 
                whether the word is in the dictionary (with an exclamation point).
        '''
        lineNo = 0
        for line in poem:
                outstring = ""
                linetotal = ""

                if not(line['blank']):
                        procLine(line)
                        for w in line['line']:
                                if(noteSubstitution):
                                        if(w['repl']): outstring += '*'
                                if(noteDictionary):
                                        if not(w['inDict']): outstring += '!'
                                outstring += w['word']
                                if(wordCount):
                                        outstring += "(%d/%d) " %(w['low'], w['high'])
                                else:
                                        outstring += "%s " %(w['word'])
                        if(lineCount):
                                linetotal += " [%3d/%3d] |" %(line['lower'],line['upper'])
                lineNo += 1

                if(numberLines): linetotal = '%5d | %s' % (lineNo, linetotal)
                print '%s %s' %(linetotal, outstring)

def printStress(poem):
	''' 
		Takes the poem. Prints out the list of stresses.
		Called from main.
	'''
	output = ""
	for line in poem:
		output += str(line['stressArray']) # convert to string and concatenate to output
		output += '\n' # and add a new line to make purdy
	print output

def buildFullArray(poem, freqLineLen):
	'''
	Check each slot of line['stressArray'] and add/subtract from corresponding slot
	in finalScores. By the end we'll know whether each syllable position is stressed
	(positive) or unstressed (negative) or we're just plum not sure (zero). The higher
	the absolute value of each slot, the surer we are.
	Also receives freqLineLen (the syllable count)
	For example, we'll end with something like:
		[-10, 4, -8, 1, -12, 6, -12, 4, -6, 13, 0, 0]
	which will be turned into:
		[-1, 1, -1, 1, -1, 1, -1, 1, -1, 1, 0, 0]

	Returns finalScores (The last list consisting of only of -1, 0, 1)
	'''
# create a list of length w/ the largest upper bound, all w/ values of 0
	maximum = 0
	for line in poem:
		if line['lower'] == line['upper'] == freqLineLen:
			if maximum < line['upper']:
				maximum = line['upper']
	finalScores = [0]*maximum
# Add or subtract from finalScores based on stressArray
	for line in poem:
		if line['lower'] == line['upper'] == freqLineLen:
			counter = 0
			for item in line['stressArray']:
				finalScores[counter] += item
				counter += 1
	print "      Totaled up: ", finalScores
# Turn finalScores into merely -1, 0, 1	(to check for stress patterns)
	counter = 0
	for item in finalScores:
		if item < 0:
			finalScores[counter] = -1
		if item > 0:
			finalScores[counter] = 1
		counter += 1
	print "      finalScores: ", finalScores
	return finalScores

def lineMajority(lineCounts):
	'''
		Takes lineCounts, a list with length (max syllables in a line of the poem).
		Finds the largest count of lines with N syllables (what syllable count
			appears the most in the poem... lines of 10 syllables are most common).
		Returns two values: N, and corresponding count
	'''
	maximum = 0	
	count = 0
	syl = 1
	for line in lineCounts:
		count += 1
		if line >= maximum:
			maximum = line
			syl = count
	return maximum, syl


def syllableMajority(poem):
	'''
		Recieves poem. Makes a list of 0s with length of largest upper syl count.
		Counts the number of lines with syl counts.
		4 lines of 10 syl; 8 lines of 11 syl, etc.
		Returns lineCounts (list)
	'''
# create a list w/ length of the largest upper bound, all w/ values of 0
	counter = 0
	for line in poem:
		if line['lower'] == line['upper']:
			if counter < line['upper']:
				counter = line['upper']
	lineCounts = [0]*counter
# go through the lines to count lines of X syl
	counter = 0
	for line in poem:
		if (line['upper'] == line['lower']):
			counter = line['upper']
			lineCounts[counter-1] = lineCounts[counter-1] + 1
	return lineCounts
	
def createStressArray(poem):
	'''
		Takes poem from main. Creates a list from the stresses.
		Stores this list in line['stressArray].
		This list is checked against existing lists of candidate meters (eventually)
			(See settings.py)
	'''
	for line in poem:
		# Do syllable counts for line look good?
		if (line['lower'] == line['upper']):
			# if so, we're gonna do something! yay! Things!
			# make list to hold stuff, descriptively called thing!
			thing = []
			counter = 0 #count syllables
			for word in line['line']:
				if word['word'] in UNSTRESSED:
					thing.append(-1)
				elif word['word'] not in UNSTRESSED and word['inDict']:
					for item in word['stress']:
						if item is '1':
							thing.append(1)
						if item is '2':
							thing.append(1)
						if item is '0':
							thing.append(-1)
				elif word['word'] not in UNSTRESSED and word['inDict'] == False:
					while counter < word['high']:
						thing.append(0)
						counter += 1
			line['stressArray'] = thing
def procLine(line):
	'''
		Receives line of poem
			(dict w/ upper/lower/blank/line (list of words as dicts)
		Checks each word in the line, gets syl count for word/line
	'''
		# for line in tempPoem:
		# 	for word in line['line']:
		# 		word['word']
	for w in line['line']: #for each word in line['line']
		w['inDict'] = checkDict(w['word'])
		getSyl(w) # get syl counts for each word
#start stress
		getStress(w) # get stresses for each word

		line['lower'] += w['low']
		line['upper'] += w['high']

def getStress(w):
	if (w['inDict'] == True):
		lookup = w['word']
		lookup = CMU[lookup]	
		w['stress'] = doStress(lookup)

def doStress(lookup):
	if lookup not in UNSTRESSED:
		return [i[-1] for i in lookup[0] if i[-1].isdigit()]
	else:
		return 0

def getSyl(word):
	'''
		Takes dictionary "word." Finds min/max syl count.
		Stores results in word['low'] and word['high'], respectively.
		If in CMU, use that. Otherwise, use dumbGuess.
	'''
	if (word['inDict'] == True):
		try:
			lowercase = word['word']
		except KeyError:
			lowercase = word['word'][:-1]
		word['low'], word['high'] = getSylCMU(lowercase)
	else:
		lowercase = word['word']
		word['low'], word['high'] = dumbGuess(lowercase)

def getSylCMU(lowercase):
	'''
		Receives lowercase (a string).
		Returns two values, low and high.
		Checks CMU[dict] for the minimum and maximum syllable counts
	'''
	low = min([len([y for y in x if isdigit(y[-1])]) for x in CMU[lowercase]])
	high = max([len([y for y in x if isdigit(y[-1])]) for x in CMU[lowercase]])
	return low, high

def dumbGuess(lowercase):
	'''
		Receives lowercase (a string).
		Returns two values, low and high.
		Runs a dumb heuristic to determine a dumb syllable count.
	'''
	numSyl = 0
	numVowels = 0
	lastVowel = False
	for ch in lowercase:
		isVowel = False
		for v in VOWELS:
			if ((v == ch) and (lastVowel)):
				isVowel = True
				lastVowel = True
			elif ((v == ch) and not (lastVowel)):
				numVowels = numVowels + 1
				isVowel = True
				lastVowel = True
		if not isVowel:
			lastVowel = False
	if (lowercase[-2:] == 'es') or (lowercase[-1:] == 'e'):
		numVowels = numVowels -1
	return numVowels, numVowels ## low, and high

def replaceHyphen(wordA, wordB):
	'''
		Recieves two 'word' as dict, wordB is blank.
		Called from makeWords.
		Replaces hyphen with a space. Returns two values, the words pre/post-hyphen
		Note, this is really clumsy... replace hyphen in A with a space. Set temp
			to the split word. Split it at the space (thus making a list?). Set 
			wordA to 1st item of temp; wordB to 2nd item. Return both words (as dict)
			UNLESS the hyphen is at the last character.
	'''
	counter = 0
	for ch in wordA['word']:
		if (ch == '-'):
			counter += 1
	if ((counter == 1) and (wordA['word'][-1]=='-')):
		wordB['lastChar'] = True
### lastChar means the only hyphen is at the end.
### note this is stored in tempX the added word...
	for punct in set('-'):
		wordA['word'] = wordA['word'].replace(punct, ' ')
	temp = wordA['word']

	if (wordB['lastChar'] == True):
		temp = temp.split(' ')
		wordA['word'] = temp[0]
		wordB['word'] = ' '
	else:
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
		if word[:-1] not in CMU:
			found = False
		found = False
	return found

def makeWords(poem):
	'''
		Takes list poem.
		Returns a list consisting of:
			tempPoem: the poem as...
				line (dictionary):
					lower bounds for syl count
					upper bounds for syl count
					blank (bool) for blank line
					line (list) for the list of words
		Function iterates through poem, line by line, converting each
		word of the poem into a python dict composed of:
			word: word as string
			low: minimum syl count
			high: minimum syl count
			repl: if something's been replaced (like a 'd)
			inDict: if the word is in the dictionary
			stress: (list to eventually hold the stress symbols)

		for line in tempPoem:
			for word in line['line']:
				word['word']
	'''
	tempPoem = []
	for line in poem:
		tempLine = dict(line=[], lower=0, upper=0, blank=False, stressArray=[])
		if (line == []):
			tempLine['blank'] = True
		for word in line:
			temp = dict(word='', low=0, high=0, repl=False, inDict=False, stress=[])
			temp['word'] = word.lower()
			if '-' in temp['word']:
				tempX = dict(word='', low=0, high=0, repl=False, inDict=False, lastChar=False, stress=[])
				temp, tempX = replaceHyphen(temp, tempX)
					# see replaceHyphen function for description
				if (tempX['lastChar'] == False):
					replaceStuff(temp)
					tempLine['line'].append(temp)
					replaceStuff(tempX)
					tempLine['line'].append(tempX)
				else:
					replaceStuff(temp)
					tempLine['line'].append(temp)
			else:
				replaceStuff(temp)
				tempLine['line'].append(temp)
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
	x = 0
	while x < num:
		print '---------------------- ',message,' ---------------------'
		x += 1
