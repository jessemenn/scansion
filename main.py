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

def printStress(line):
	''' 
		Takes the line. Prints out the stresses.
		currently called from prettyOutput

		If the word is not in UNSTRESSED and in the cmuDict, print it.
		Otherwise print an asterisk for each syllable.
	'''
	output = "       "
	for word in line['line']:
		if word['word'] not in UNSTRESSED and word['inDict'] == True:
			for item in word['stress']:
				output += item
				output += ' '
		else:
			i = 0
			while(i < word['high']):
				output += '* '
				i += 1
	print output

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
# start stressings
                printStress(line)
# oorgle
        createStressArray(poem[6])

def createStressArray(line):
	'''
		Creates a list with the stresses of the line passed.
		This list is checked against existing lists of candidate meters
			(See settings.py)
	'''
	# Do syllable counts for line look good?
	if (line['lower'] == line['upper']):
		# if so, we're gonna do something! yay! Things!
		# make list to hold stuff, descriptively called thing!
		thing = []
		booze = 0 #counter
		# This just fills thing with tildes. 
		while (booze < line['upper']):
			thing.append('~')
			booze += 1
		print len(thing)
		print (thing)
		print thing[0]



## main
if __name__ == '__main__':
	if len(sys.argv) < 2:
		filename = 'sample.txt'
	elif len(sys.argv) >= 2:
		filename = sys.argv[1]
	print '*** Using ', filename, ' ***'
	sys.exit(main(filename))
