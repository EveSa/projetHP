import re
import os

#version environnement unix
#os.chdir("/home/eve/Documents/MasterTAL/Semestre2/EnrichissementdeCorpus")

#version environnement windows
os.chdir("C://Users//elisa//Downloads//Enrichissement de corpus//")
 
#### Ouverture des fichiers
#version environnement unix
#f = "/home/eve/Documents/MasterTAL/Semestre2/EnrichissementdeCorpus/texte_tagge_auto.txt"
#version environnement windows
f = "C://Users//elisa//Downloads//Enrichissement de corpus//texte_tagge_auto.txt"
#version environnement unix
#g= "/home/eve/Documents/MasterTAL/Semestre2/EnrichissementdeCorpus/texte_tagge_man.txt"
#version environnement windows
g= "C://Users//elisa//Downloads//Enrichissement de corpus//texte_tagge_man.txt"
auto_tok_text = open(f, "r", encoding="utf-8")
man_tok_text = open(g, "r", encoding="utf-8")
textes = open("textes_ensemble.txt", "w", encoding="utf-8")
differences = open("differences.txt", "w", encoding="utf-8")

#### Lecture des fichiers
auto_lines=auto_tok_text.readlines()
man_lines=man_tok_text.readlines()
max_lenght=max(len(auto_lines),len(man_lines))

#### Fonction de recupération du mot traité
def clean_word(lines,index):
    try:
        line=re.sub(r'\(|\)|\n',r'',lines[index])
        list_line=re.split('/',line)
        word = list_line[0]
        return word
    except:
        return ''

#### Fonction de recupération du POS traité
def clean_pos(lines,index):
    if index<(len(lines)) :
        line=re.sub(r'\(|\)|\n',r'',lines[index])
        list_line=re.split('/',line)
        pos = list_line[1]
        return pos
    else :
        return ''

#### Boucle d'alignement des mots

i=1 #i if for automatically tokenized file
j=1 #j is for manual tokenized file
vrai_positif=0

while j < len(man_lines):
    while i <len(auto_lines):
        print(i,j)
        auto_word = clean_word(auto_lines,i)
        man_word = clean_word(man_lines,j)
        auto_pos = clean_pos(auto_lines,i)
        man_pos = clean_pos(man_lines,j)


        if len(auto_word) > len(man_word) :
            print(auto_word,man_word)
            print(auto_pos,man_pos)
            textes.write(auto_word+" " +man_word+"\n")
            textes.write(auto_pos+" " +man_pos+"\n")
            j += 1
            man_wordplus1=clean_word(man_lines,j)
            man_posplus1 = clean_pos(man_lines,j)
            print(auto_word,man_wordplus1)
            print(auto_pos,man_posplus1)
            differences.write("-")
            textes.write(auto_word+" " +man_wordplus1+"\n")
            textes.write(auto_pos+" " +man_posplus1+"\n")

        elif len(auto_word) < len(man_word) :
            print(auto_word,man_word)
            print(auto_pos,man_pos)
            textes.write(auto_word+" " +man_word+"\n")
            textes.write(auto_pos+" " +man_pos+"\n")
            i += 1
            auto_wordplus1=clean_word(auto_lines,i)
            auto_posplus1=clean_pos(auto_lines,i)
            print(auto_wordplus1,man_word)
            print(auto_posplus1,man_pos)
            differences.write("-")
            textes.write(auto_wordplus1 + " " + man_word+ "\n")
            textes.write(auto_posplus1 + " " + man_pos+ "\n")

        else:   
            print(auto_word,man_word)
            print(auto_pos,man_pos)
            if auto_pos == man_pos :
                vrai_positif +=1 
                differences.write("+")
                textes.write(auto_word+" " +man_word+"\n")
                textes.write(auto_pos+" " +man_pos+"\n")

        i += 1
        j += 1

print(vrai_positif)

#### Fermeture des fichiers
auto_tok_text.close()
man_tok_text.close()
textes.close()
differences.close()

#### Calcul précision, rappel et f-mesure
p = (vrai_positif)/(len(man_lines))
r = (vrai_positif)/(len(auto_lines))
f= 2*(p*r)/(p+r)

print('precision : %f \n rappel : %f \n f-mesure : %f' %(p,r,f))

exit()