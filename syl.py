import re
import nltk
from curses.ascii import isdigit
from nltk.corpus import cmudict
import nltk.data
import pprint
import string

# -- replaced by getMaxMin -- 
# def nsyl(word):
#   lowercase = word.lower()
#   if lowercase not in cmu:
#     return 0
#   else:
#      return min([len([y for y in x if isdigit(y[-1])]) for x in cmu[lowercase]])



def getMaxMin(word):
  lowercase = word['word']
  if lowercase not in cmu:
    print lowercase,' not in dictionary'
    lowercase = stripEndings(word)
    return word
  else:
    word['low'] = min([len([y for y in x if isdigit(y[-1])]) for x in cmu[lowercase]])
    word['high'] = max([len([y for y in x if isdigit(y[-1])]) for x in cmu[lowercase]])
    return word

def stripEndings(word):
  temp = (word['word'])
  if (len(temp) > 1):
    tempCheck, tempLetter = temp[:-1], temp[-1]
    print 'temp check: ',tempCheck
  if (tempCheck in cmu):
    a = tempCheck
    '''
      for some reason, if I try to run tempCheck through this second max, it gives
      an error... changing it to a diff variable, (set after entering this if
        statement, makes it okay. I don't understand why.)
    '''
    word['low'] = min([len([y for y in tempCheck if isdigit(y[-1])]) for tempCheck in cmu[tempCheck]])
    print 'word["low"]: ',word['low']
    word['high'] = max([len([y for y in a if isdigit(y[-1])]) for a in cmu[a]])
    print 'word["high"]: ',word['high']
  return word

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

def loadWebster(webster):
  fp = open("words.txt")
  return 999

def scoring (lineObj):
  '''
    "Score" each line so that you get an idea of syllable count.
    By taking a range, it allows some mild wiggle room later, perhaps by
      multiplying by number of lines, We'll be able to get relatively close
      to some sort of percentage-ness of syllables per poem.
    I'm figuring if min/max line counts are both 10, we're probably stoked.
      Score: 2
    If 10 falls between min and max and we're within a few syl (9 to 11)
      Score: 1
    If shit's crazy, the line's probably pretty screwed up
      Score 0.
  '''
  a = lineObj['lower']
  b = lineObj['upper']
  c = abs(b - a)  # if negative, prolly something weird, print error msg
  if ((a == 10) and (b == 10)):
    lineObj['score'] = 2
  elif ((a <= 10) and (b >= 10)) and (c <= 3):
    lineObj['score'] = 1
  elif (c > 3) or (a > 10) or (b < 10):
    lineObj['score'] = 0
  return lineObj

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

for datum in data:
  '''
  This is really ugly, but, I needed to replace -'d endings
  with -ed endings, and the only place I could think of doing
  it was when first creating the lines.
  As this loop starts, apostrophes should be the only punctuation
  in the word. After replED, that apostrophe (and anything else
  I missed in exclude) should be stripped out.
  '''
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

for line in lines:
  line = nltk.Text(line)

regexp = "[A-Za-z]+"
exp = re.compile(regexp)

for line in lines:
  words = [w.lower() for w in line]
  lineObj = dict(line=line, upper=0, lower=0, score=0) ## change to upper/lower bounds
  for a in words:
    if (exp.match(a)):
      current = dict(word=a, low=0, high=0)
      current = getMaxMin(current)
      lineObj['lower'] = lineObj['lower'] + current['low']
      lineObj['upper'] = lineObj['upper'] + current['high']
  lineObj = scoring(lineObj)
  print '***************************************************************'
  print lineObj['line'],'has a score of: ',lineObj['score']
  print '         ',lineObj['lower']
  print '         ',lineObj['upper']
  print '***************************************************************'