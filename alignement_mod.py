import re
import os

#version environnement unix
os.chdir("/home/eve/Documents/MasterTAL/Semestre2/EnrichissementdeCorpus/Projet_HP")

#version environnement windows
#os.chdir("C://Users//elisa//Downloads//Enrichissement de corpus//")
 
#### Ouverture des fichiers

#version environnement unix
f = "/home/eve/Documents/MasterTAL/Semestre2/EnrichissementdeCorpus/aresultat.txt"
g= "/home/eve/Documents/MasterTAL/Semestre2/EnrichissementdeCorpus/Projet_HP/texte_tokenize.txt"

#version environnement windows
#f = "C://Users//elisa//Downloads//Enrichissement de corpus//resultat.txt"
#g= "C://Users//elisa//Downloads//Enrichissement de corpus//texte_tokenize.txt"

auto_tok_text = open(f, "r", encoding="utf-8")
man_tok_text = open(g, "r", encoding="utf-8")
textes = open("texts_together.txt", "w", encoding="utf-8")
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

while j < len(man_lines) or i <len(auto_lines): #On parcourt la totalité des lignes du fichiers
    
        print(i,j)

        auto_word = clean_word(auto_lines,i)   #On récupère le mot annoté automatiquement
        man_word = clean_word(man_lines,j)     #On récupère le mot annoté manuellement 
        auto_pos = clean_pos(auto_lines,i)     #On récupère de pos annoté automatiquement
        man_pos = clean_pos(man_lines,j)       #On récupère le pos annoté manuellement


        if len(auto_word) > len(man_word) : #Si la taille du mot annoté automatiquement est > à celui annoté manuellement, on considère que c'est parceque le mot est réparti en deux parties sur l'annotation manuelle
            textes.write(auto_word+" " +man_word+"\n")
            differences.write("-")
            j += 1
            man_wordplus1=clean_word(man_lines,j)
            textes.write(auto_word+" " +man_wordplus1+"\n")
            differences.write("-")

        elif len(auto_word) < len(man_word) : #et inversement
            textes.write(auto_word+" " +man_word+"\n")
            differences.write("-")
            i += 1
            auto_wordplus1=clean_word(auto_lines,i)
            print(auto_wordplus1,man_word)
            textes.write(auto_word+" " +man_wordplus1+"\n")
            differences.write("-")

        else:                                   #Si les deux mots ont la même taille, on peut regarder le POS et vérifier leur adéquation
            print(auto_word,man_word)
            textes.write(auto_word+" " +man_word+"\n")
            if auto_pos == man_pos :
                vrai_positif +=1 
                differences.write("+")
            else :
                differences.write("-")

        i += 1
        j += 1

#### Fermeture des fichiers
auto_tok_text.close()
man_tok_text.close()
textes.close()

#### Calcul précision, rappel et f-mesure
p = (vrai_positif)/(len(man_lines))
r = (vrai_positif)/(len(auto_lines))
if p!=0 or r!=0 : #On evite le cas où la précision et le rappel seraient == 0 pour les 2 premières décimal (python arrondi alors à 0)
    f= 2*(p*r)/(p+r)
else :
    f = 'div/zero'

print('precision : %f\n rappel : %f\n f-mesure : %f' %(p,r,f))

exit()
