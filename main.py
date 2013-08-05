from jesse import *
import settings

'''
	The main routine is in main(filename), the first defined function.
	In makeWords function, I make each word into a dict that consists
	of (see jesse.py):
		word 	--	the word
		low	--	int minimum syllable count for the word
		high	--	int maximum syllable count for the word
		repl 	--	bool whether a character replacement was made
				maybe this should include what was replaced
                inDict  --  if word is in cmuDict
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
	prettyOutput(poem,noteDictionary=True)
	beginStress(poem)

def beginStress(poem):
	'''
		Called w/ poem.
		Calls syllableMajority, createStressArray, printStress...
		lineLen: count of lines w/ syllable_slot (from lineMajority)
		freqLineLen: syllable_slot (from lineMajority)

	'''
	createStressArray(poem)
#	printStress(poem) 
	lineCounts = syllableMajority(poem)
	print "     ", "LineCounts: ",lineCounts
	lineLen, freqLineLen = lineMajority(lineCounts)
	print "     ","Most frequent syllable count: ", freqLineLen, " appears: ", lineLen

	buildFullArray(poem, freqLineLen)

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
	'''
# create a list of length w/ the largest upper bound, all w/ values of 0
	maximum = 0
	print "freqLineLen = ", freqLineLen
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
	print "finalScores: ", finalScores, "  second for loop"
# Turn finalScores into merely -1, 0, 1	(to check for stress patterns)
	counter = 0
	for item in finalScores:
		if item < 0:
			finalScores[counter] = -1
		if item > 0:
			finalScores[counter] = 1
		counter += 1
	print "finalScores: ", finalScores, "  final for loop"

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
			# This just fills thing with tildes.
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





## main
if __name__ == '__main__':
	if len(sys.argv) < 2:
		filename = 'sample.txt'
	elif len(sys.argv) >= 2:
		filename = sys.argv[1]
	print '*** Using ', filename, ' ***'
	sys.exit(main(filename))
