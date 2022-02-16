import os
from nltk.tag import StanfordPOSTagger
from nltk import word_tokenize

#version environnement windows
#java_path = 'C://Program Files (x86)//Common Files//Oracle//Java//javapath/java.exe'   
#os.environ['JAVAHOME'] = java_path

#version environnement unix
java_path="/bin/java"
os.environ['JAVAHOME']=java_path

# Add the jar and model via their path (instead of setting environment variables):

#version environnement windows
#jar='C://Users//elisa//Downloads//Enrichissement de corpus//stanford-tagger-4.2.0//stanford-postagger-full-2020-11-17//stanford-postagger.jar'
#model = 'C://Users//elisa//Downloads//Enrichissement de corpus//stanford-tagger-4.2.0//stanford-postagger-full-2020-11-17//models//french-ud.tagger'
#f = "C://Users//elisa//Downloads//Enrichissement de corpus//Harry_Potter_T4_Ch6-P1-2.txt"

#version environnement unix
jar="/home/eve/Bureau/MasterTAL/Semestre2/EnrichissementdeCorpus/Projet_HP/stanford-postagger-full-2020-11-17/stanford-postagger.jar"
model="/home/eve/Bureau/MasterTAL/Semestre2/EnrichissementdeCorpus/Projet_HP/stanford-postagger-full-2020-11-17/models/french-ud.tagger"
f="/home/eve/Documents/MasterTAL/Semestre2/EnrichissementdeCorpus/Projet_HP/Harry_Potter_T4_Ch6-P1-2.txt"

resultat = open("resultat.txt", "w", encoding="utf-8")

text = open(f, encoding="utf-8").read()

pos_tagger = StanfordPOSTagger(model, jar, encoding='utf8')

text_final = pos_tagger.tag(word_tokenize(text))
print(text_final)


for word,pos in text_final:
    resultat.write("("+ word + "/" + pos +")"+"\n")
    
resultat.close()