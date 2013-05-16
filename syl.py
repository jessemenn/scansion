import re
import nltk
from curses.ascii import isdigit
from nltk.corpus import cmudict
import nltk.data
import pprint
import string

def nsyl(word):
  lowercase = word.lower()
  if lowercase not in d:
    print lowercase,' not in dictionary'
    global dunno        ## be careful with this stupidity
    dunno = dunno + 1  ## be careful with this stupidity
    return 0
  else:
     return min([len([y for y in x if isdigit(y[-1])]) for x in d[lowercase]])

d = cmudict.dict()

################## open file ##################
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
#fp = open("sample.txt")
fp = open("pope_windsor_forest.txt")
#fp = open("paradise_lost.txt")
data = fp.read()
data = data.split('\n') ## line breaking.


exclude = set(string.punctuation)


lines = []

for woot in data:
  woot = ''.join(ch for ch in woot if ch not in exclude)
  lines.append(nltk.wordpunct_tokenize(woot))
#  lines.append(nltk.WhitespaceTokenizer().tokenize(woot))

for line in lines:
  line = nltk.Text(line)

########### begin doing stuff ###########

regexp = "[A-Za-z]+"
exp = re.compile(regexp)


############### debug stuff:
global dunno # not found in dict
dunno = 0
fuck = 0  # wrong count
lineFuck = 0 # line has a word not in dict
trueError = 0 # actual errors
################

for line in lines:
  sum1 = 0
  lineFuck = 0
  words = [w.lower() for w in line]
  for a in words:
    if (exp.match(a)):
      sum1 = sum1 + nsyl(a)
    if (nsyl(a) == 0):
      lineFuck = 1      ## flag as line has a word missing
      dunno = dunno - 1 ## nsyl changes DUNNO each time a word is missing, so decrement here
  print line,"number of syllables in this line:",sum1
##################### debugging stuff #####################
  if (sum1 != 10):
    fuck = fuck + 1
    if (lineFuck == 0):
      trueError = trueError + 1

print 'Lines with syllables != 10: ',fuck
print 'Words not found: ',dunno
print 'Actual errors when all words are found: ',trueError