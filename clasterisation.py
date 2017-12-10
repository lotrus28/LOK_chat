#this script processes parsed operator-client dialoges 
#it aims to hierarchically clasterize words according to their frequencies 
#unfortunately some problems occur at the stage of distance matrix building

#importing library for morphemic analysis of the text
import pymorphy2
#importing module for word counting
from collections import Counter
#importing numpy to handle arrays
import numpy as np
#importing module for disctance matrix computation
from scipy.spatial import distance
#importing module for hierarchical clasterization
from scipy.cluster import hierarchy
#importing module for dendrogram visualization
import matplotlib.pyplot as plt

morph = pymorphy2.MorphAnalyzer()

#this is the test version, it handles only every 100th string of text to reduce operation time
#importing text
with open("test.txt", "r") as tosub, open("out_2.txt", "w", encoding="utf-8") as outfile:
    file_iter=iter(tosub)
    i=0
    while True:
        i=i+1   
        try:
            line=next(file_iter)
            if i%100==0:
                #remove all punctuation marks
                line=line.replace(".", " ")
                line=line.replace("?", " ")
                line=line.replace("!", " ")
                line=line.replace(",", " ")
                #print(line)
                #line=morph.tokenize(line)
                #print(line)
                line=line.strip().split()
                for a in line:
                    #replace all words by their infinitives and write to a new file
                    temp_el=morph.parse(a)[0].normal_form
                    outfile.write(str(temp_el)+" ")
                outfile.write("\n")
        except:
            break
            
#obtain vector of all possible words (it is largely reduced by previous step)        
with open("out_2.txt", "r") as infile:
    f_iter=iter(infile)
    word_dump=[]
    while True:
        try:
            line=next(f_iter)
            line=line.strip().split()
            for word in line:
                if word not in word_dump:
                    word_dump.append(word)
        except:
            break

print(len(word_dump))

#converting all strings to vectors of word-counts according to total vector of words
#phrase_dict={}
mega_vect=[]
with open("out_2.txt", "r", encoding="utf-8") as infile:
    f_iter=iter(infile)
    i=0
    while True:
        try:
            i=i+1
            line=next(f_iter)
            line=line.strip().split()
            counts = Counter(line)
            word_vect=[]
            for b in word_dump:
                if b in counts.keys():
                    word_vect.append(counts[b])
                else:
                    word_vect.append(0)
            #creating list of lists (vectors) to convert it to numpy array
            mega_vect.append(word_vect)
            #temp_dict={i:word_vect}
            #phrase_dict.update(temp_dict)
        except:
            break

#converting list of vectors to array
phrase_array = np.array(mega_vect)

#computing distnance matrix and building dendrogram
#unfortunately this part of the code does not work correctly
%matplotlib inline
import sys
sys.setrecursionlimit(10000)
#dist_mat=distance.pdist(phrase_array, "hamming")
Z = hierarchy.linkage(phrase_array, 'single')
plt.figure()
dn = hierarchy.dendrogram(Z)

#writing array to a pickle-file 
import pickle
pickle_out = open("array.pickle","wb")
pickle.dump(phrase_array, pickle_out)
pickle_out.close()