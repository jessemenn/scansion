import re
import nltk
from curses.ascii import isdigit
from nltk.corpus import cmudict
import nltk.data
import pprint
import string

def nsyl(word):
  lowercase = word.lower()
  if lowercase not in cmu:
    print lowercase,' not in dictionary'
    global dunno        ## be careful with this stupidity
    dunno = dunno + 1  ## be careful with this stupidity
    return 0
  else:
     return min([len([y for y in x if isdigit(y[-1])]) for x in cmu[lowercase]])

def replED(word):
  if (len(word) > 1):
    oorgle = list(word)
    if ((word[-2] == "'") and (word[-1] == 'd')):
      oorgle[-2] = "e"
      word = ''.join(oorgle)
    if ((word[-2] == "'") and (word[-1] == 'n')):
      oorgle[-2] = "e"
      word = ''.join(oorgle)
  for punct in string.punctuation:
    word = word.replace(punct,"")
  return word

def stripEndings(word):
  return 999
def loadWebster(webster):
  fp = open("words.txt")
  return 999



cmu = cmudict.dict()
# webster = loadWebster(webster)

################## open file ##################
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
# fp = open("sample.txt")
# fp = open("frost_woods.txt")
fp = open("pope_windsor_forest.txt")
# fp = open("paradise_lost.txt")
data = fp.read()
data = data.split('\n') ## line breaking.

# exclude = set(string.punctuation)
exclude = set('!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~')
  # exclude all string.punctuation except apostrophe (I think?)
  # note that i remove all of string.punctuation at the end of
  # the replED function
lines = []  #to store the poem



# This is really ugly, but, I needed to replace -'d endings
# with -ed endings, and the only place I could think of doing
# it was when first creating the lines.
# As this loop starts, apostrophes should be the only punctuation
# in the word. After replED, that apostrophe (and anything else
# I missed in exclude) should be stripped out.

for datum in data:
  datum = ''.join(ch for ch in datum if ch not in exclude)
  temps = nltk.WhitespaceTokenizer().tokenize(datum)
  argy = []
  bargy = ''
  i = 0
  for temp in temps:
    argy = replED(temp)
    temps[i] = argy
    i = i + 1 #counter
    bargy = ' '.join(temps)
  lines.append(nltk.wordpunct_tokenize(bargy))

#  datum = ''.join(ch for ch in datum)
#  lines.append(nltk.WhitespaceTokenizer().tokenize(datum))

for line in lines:
  line = nltk.Text(line)

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