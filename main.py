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
	createStressArray(poem)
	printStress(poem)
	buildFullArray(poem)

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

def buildFullArray(poem):
	'''
	Check each slot of line['stressArray'] and add/subtract from corresponding slot
	in finalScores. By the end we'll know whether each syllable position is stressed
	(positive) or unstressed (negative) or we're just plum not sure (zero). The higher
	the absolute value of each slot, the surer we are.
	For example, we'll end with something like:
		[-10, 4, -8, 1, -12, 6, -12, 4, -6, 13, 0, 0]
	which will be turned into:
		[-1, 1, -1, 1, -1, 1, -1, 1, -1, 1, 0, 0]
	'''
# create a list of length w/ the largest upper bound, all w/ values of 0
	maximum = 0
	for line in poem:
		if line['lower'] == line['upper'] == 10:
			if maximum < line['upper']:
				maximum = line['upper']
	finalScores = [0]*maximum
# Add or subtract from finalScores based on stressArray
	for line in poem:
		if line['lower'] == line['upper'] == 10:
			counter = 0
			for item in line['stressArray']:
				finalScores[counter] += item
				counter += 1
	print finalScores
# Turn finalScores into merely -1, 0, 1	(to check for stress patterns)
	counter = 0
	for item in finalScores:
		if item < 0:
			finalScores[counter] = -1
		if item > 0:
			finalScores[counter] = 1
		counter += 1
	print finalScores


## main
if __name__ == '__main__':
	if len(sys.argv) < 2:
		filename = 'sample.txt'
	elif len(sys.argv) >= 2:
		filename = sys.argv[1]
	print '*** Using ', filename, ' ***'
	sys.exit(main(filename))
