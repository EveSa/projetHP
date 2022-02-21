import re
import os

#version environnement unix
os.chdir("/home/eve/Documents/MasterTAL/Semestre2/EnrichissementdeCorpus/projetHP")

#version environnement windows
#os.chdir("C://Users//elisa//Downloads//Enrichissement de corpus//")
 
#### OUVERTURE DES FICHIERS ####

#version environnement unix
f = "/home/eve/Documents/MasterTAL/Semestre2/EnrichissementdeCorpus/projetHP/autoTokenized.txt"
g= "/home/eve/Documents/MasterTAL/Semestre2/EnrichissementdeCorpus/projetHP/texte_tokenize.txt"

#version environnement windows
#f = "C://Users//elisa//Downloads//Enrichissement de corpus//resultat.txt"
#g= "C://Users//elisa//Downloads//Enrichissement de corpus//texte_tokenize.txt"

auto_tok_text = open(f, "r", encoding="utf-8")
man_tok_text = open(g, "r", encoding="utf-8")
textes = open("POSDifferences.txt", "w", encoding="utf-8")

#### LECTURE DES FICHIERS ####

auto_lines=auto_tok_text.readlines()
man_lines=man_tok_text.readlines()
max_lenght=max(len(auto_lines),len(man_lines))

#### DEFINITION DES FONCTIONS ####

def clean(lines,index,value):
    try:
        line=re.sub(r'\(|\)|\n',r'',lines[index])
        list_line=re.split('/',line)
        word = list_line[value] #On mettra une value de 0 pour le mot et une value de 1 pour le pos
        return word
    except:
        return ''

#### INITIALISATION DES COMPTEURS ####

i=0 #i if for automatically tokenized file
j=0 #j is for manual tokenized file
vrai_positif=0


#### CORPS DU SCRIPT ####

while j < len(man_lines) and i <len(auto_lines): #On parcourt la totalité des lignes du fichiers
    
#initialisation des valeurs pour la boucle en cours
        auto_word = clean(auto_lines,i,0)
        man_word = clean(man_lines,j,0)
        auto_pos = clean(auto_lines,i,1)
        man_pos = clean(man_lines,j,1)

#Si la taille du mot annoté automatiquement est > à celui annoté manuellement,
#on considère que c'est parceque le mot est réparti en plusieurs parties sur l'annotation manuelle
        if len(auto_word) > len(man_word) and re.search(man_word,auto_word) and man_word[-1] != auto_word [-1] :
            
            textes.write(auto_word+" " +man_word+"\n")
            textes.write(auto_pos+" " +man_pos+"\n")
            print("-", end="")
            #On insère une nouvelle "ligne" dans le readlines pour décaler les sorties
            new_line = "(%s/%s)"%(auto_word,auto_pos)
            auto_lines.insert(i,new_line)

#et inversement
        elif len(auto_word) < len(man_word) and re.search(man_word,auto_word) and man_word[-1] != auto_word [-1] :

            textes.write(auto_word+" " +man_word+"\n")
            textes.write(auto_pos+" " +man_pos+"\n")
            print("-", end="")
            
            new_line = "(%s/%s)"%(man_word,man_pos)
            man_lines.insert(j,new_line)

#Si les deux mots ont la même taille, on peut regarder le POS et vérifier leur adéquation
        else:
            
            if auto_pos == man_pos :
                vrai_positif +=1 
                print("+", end="")
            
            else :
                textes.write(auto_word+" " +man_word+"\n")
                textes.write(auto_pos+" " +man_pos+"\n")
                print("-", end="")

        i += 1
        j += 1

#### FERMETURE DES FICHIERS ####

auto_tok_text.close()
man_tok_text.close()
textes.close()

#### CALCULs précision, rappel et f-mesure ####
p = (vrai_positif)/(len(man_lines))
r = (vrai_positif)/(len(auto_lines))
if p!=0 or r!=0 : #On evite le cas où la précision et le rappel seraient == 0 pour les 2 premières décimal (python arrondi alors à 0)
    f= 2*(p*r)/(p+r)
else :
    f = 'div/zero'

print('\n precision : %f\n rappel : %f\n f-mesure : %f' %(p,r,f))

exit()