import codecs
import nltk
import sys
from nltk.corpus import stopwords

default_stopwords = set(nltk.corpus.stopwords.words('russian'))

stopwords_file = './stopwords_ingos.txt'
custom_stopwords = set(codecs.open(stopwords_file, 'r', 'utf-8').read().splitlines())

all_stopwords = default_stopwords | custom_stopwords

input_file = sys.argv[1]

#fp = codecs.open(input_file, 'r', 'utf-8')

fp = codecs.open(input_file, 'r', 'cp1251')


lines = fp.readlines()

clean_lines = []

lines_with_freq = []

all_words = []

for e in range(len(lines)):
	words = nltk.word_tokenize(lines[e])
	
	words = [word for word in words if len(word) > 1]
	
	# Remove numbers
	words = [word for word in words if not word.isnumeric()]

	words = [word for word in words if not ('0' in word or '/' in word or '\'' in word or '`' in word)]

	words = [word.strip(',').strip('!').strip('?') for word in words]
	
	# Lowercase all words (default_stopwords are lowercase too)
	words = [word.lower() for word in words]
	
	# Remove stopwords
	words = [word for word in words if word not in all_stopwords]
	
	clean_lines.append([])

	for k in words:
		clean_lines[e].append(k)

fout = codecs.open(sys.argv[1].split('.')[0]+'_clean.txt', 'w', "utf-8")

for e in clean_lines:
	if (len(e)<=3):
		continue
	for k in e:
		fout.write(k + " ")
	fout.write('\n')

fout.close()

#	for k in words:
#		if (k not in all_words):
#			all_words.append(k)
#
#	# Calculate frequency distribution
#	fdist = nltk.FreqDist(words)
#	wf = []
#	for w in fdist.keys():
#		wf.append([w, fdist[w]])
#	
#
#	lines_with_freq.append(wf)
#
#for e in lines_with_freq:
#	for k in all_words:
#		is_in = 0
#		for j in e:
#			if (k in j[0]):
#				is_in = 1
#		if (is_in == 0):
#			e.append([k, 0])
#	
#	e = sorted(e[:], key=lambda x: x[0])
#
#
#
#fout = codecs.open(sys.argv[1].split('.')[0]+'_frequencies.txt', 'w', "utf-8")
#
#for e in range(len(lines_with_freq)):
#	for w in lines_with_freq[e]:
#		fout.write(w[0]+ u' '+unicode(int(w[1]))+u'; ')
#	fout.write('\n')
#
#
#