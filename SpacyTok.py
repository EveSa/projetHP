import spacy

nlp = spacy.load("fr_core_news_sm")
txt = open("/home/eve/Documents/MasterTAL/Semestre2/EnrichissementdeCorpus/projetHP/Harry_Potter_T4_Ch6-P1-2.txt").read()
resultat = open("SpacyAutoTokenized.txt", "w", encoding="utf-8")
doc = nlp(txt)
for token in doc:
    if token.pos_ != "SPACE":
        resultat.write("("+ token.text + "/" + token.pos_ +")"+"\n")
        print(token.text,token.pos_)