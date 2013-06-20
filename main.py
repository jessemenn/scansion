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

#		getStress(w) # get stresses for each word

		line['lower'] += w['low']
		line['upper'] += w['high']

# def getStress(w):
# 	if (w['inDict'] == True):
# 		fuckyeah = w['word']
# 		fuckyeah = CMU[fuckyeah]
# 		w['stress'] = doStress(fuckyeah)

# def doStress(fuckyeah):
# 	return [i[-1] for i in fuckyeah[0] if i[-1].isdigit()]

			# def getStress(cmu):
			# 	return [i[-1] for i in d if i[-1].isdigit()
			# example:
			# cmu = cmudict.dict()
			# word = d['alkaline']
			# word = [['AE1', 'L', 'K', 'AH0', 'L', 'AY2', 'N']]
			# stress(word[0]) # note list of list.
			# will give back ['1', '0', '2']

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
#                printStress(line)
'''
def printStress(line):
	output = ""
	for word in line['line']:
		for item in word['stress']:
			if (word['low'] == 1) and (word['high'] == 1):
				output += '8 '
			else:
				output += item
				output += ' '
	print output
'''
## main
if __name__ == '__main__':
	if len(sys.argv) < 2:
		filename = 'sample.txt'
	elif len(sys.argv) >= 2:
		filename = sys.argv[1]
	print '*** Using ', filename, ' ***'
	sys.exit(main(filename))
