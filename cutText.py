# running the Stanford POS Tagger from NLTK
import nltk

import os
os.chdir("/home/eve/Documents/MasterTAL/Semestre2/EnrichissementdeCorpus")
 
# point this path to a utf-8 encoded plain text file in your own file system
f = "/home/eve/Documents/MasterTAL/Semestre2/EnrichissementdeCorpus/Harry_Potter_T4_Ch6-P1-2.txt"
texte = open("texte_tokenize.txt", "w", encoding="utf-8")
 
text_raw = open(f, encoding="utf-8").read()
text = nltk.word_tokenize(text_raw)
 
# print the list of tuples: (word,word_class)
# this is just a test, comment out if you do not want this output
print(text)
 
# for loop to extract the elements of the tuples in the pos_tagged list
# print the word and the pos_tag with the underscore as a delimiter
for word in text:
    texte.write("("+word + "/" ")"+"\n")
    
texte.close()