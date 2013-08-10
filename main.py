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
	metadata = {'title': "", 'author': "", 'date': "", 'nation': ""}
	getMetadata(poem, metadata)
	outputMetadata(metadata)

	poem = makeWords(poem)
	prettyOutput(poem,noteDictionary=True)
	beginStress(poem)

def outputMetadata(metadata):
	print "title | ", metadata['title']
	print "author| ", metadata['author']
	print "date  | ", metadata['date']
	print "nation| ", metadata['nation']

def getMetadata(poem, metadata):
	'''
		Gets metadata information from first four lines of the poem
		then removes those four lines from the list (poem)
	'''
	for word in poem[0]:
		metadata['title'] += word
		metadata['title'] += " "
	for word in poem[1]:
		metadata['author'] += word
		metadata['author'] += " "
	for word in poem[2]:
		metadata['date'] += word
	for word in poem[3]:
		metadata['nation'] += word
	for x in range(4): ## delete first four lines of the list/poem
		del poem[0]

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



## main
if __name__ == '__main__':
	if len(sys.argv) < 2:
		filename = 'sample.txt'
	elif len(sys.argv) >= 2:
		filename = sys.argv[1]
	print '*** Using ', filename, ' ***'
	sys.exit(main(filename))
