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
	finalScores = buildFullArray(poem, freqLineLen)

	checkForms(finalScores)



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
	print "      freqLineLen = ", freqLineLen
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
	print "        Totaled up: ", finalScores, "  second for loop"
# Turn finalScores into merely -1, 0, 1	(to check for stress patterns)
	counter = 0
	for item in finalScores:
		if item < 0:
			finalScores[counter] = -1
		if item > 0:
			finalScores[counter] = 1
		counter += 1
	print "      finalScores: ", finalScores, "  final for loop"
	return finalScores






## main
if __name__ == '__main__':
	if len(sys.argv) < 2:
		filename = 'sample.txt'
	elif len(sys.argv) >= 2:
		filename = sys.argv[1]
	print '*** Using ', filename, ' ***'
	sys.exit(main(filename))
