from jesse import *
import settings

'''
	The main routine is in main(filename), the first defined function.
	In makeWords function, I make each word into a dict that consists
	of (see jesse.py):
		word 	--	the word
		low		--	int minimum syllable count for the word
		high	--	int maximum syllable count for the word
		repl 	--	bool whether a character replacement was made
					--	maybe this should include what was replaced
		inDict--  if word is in cmuDict
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
# 	print 'yes it ran'

def procLine(line):
	'''
		Recieves line of poem
		Checks each word in the line
	'''
	for w in line:
		w['inDict'] = checkDict(w['word'])
		getSyl(w)
		print w

## main
if __name__ == '__main__':
	if len(sys.argv) < 2:
		filename = 'sample.txt'
	elif len(sys.argv) >= 2:
		filename = sys.argv[1]
	print '*** Using ', filename, ' ***'
	sys.exit(main(filename))