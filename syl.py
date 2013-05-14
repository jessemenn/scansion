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
     print '***** *****',lowercase,'***** ***** not in dictionary'
     return 0
  else:
     return min([len([y for y in x if isdigit(y[-1])]) for x in d[lowercase]])

d = cmudict.dict()

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
fp = open("sample.txt")
data = fp.read()
data = data.split('\n') ## line breaking.

print '**************************************************************'
print '         starting nltk.wordpunct_tokenize(line)'
print '**************************************************************'
exclude = set(string.punctuation)
## store some shit
lines = []
for woot in data:
  woot = ''.join(ch for ch in woot if ch not in exclude)
  lines.append(nltk.wordpunct_tokenize(woot))
#  lines.append(nltk.WhitespaceTokenizer().tokenize(woot)) 
#  print lines

print '**************************************************************'
print '               starting nltk.Text(line)'
print '**************************************************************'

#text = nltk.Text(tokens)
for line in lines:
  line = nltk.Text(line)
#  print line

print '**************************************************************'
print '               starting doing shit!'
print '**************************************************************'

regexp = "[A-Za-z]+"
exp = re.compile(regexp)

for line in lines:
  sum1 = 0
  words = [w.lower() for w in line]
  for a in words:
    if (exp.match(a)):
#      print a
#      print "no of syllables:",nsyl(a)
      sum1 = sum1 + nsyl(a)
  print line,"number of syllables in this line:",sum1
  print '**************************************************************'