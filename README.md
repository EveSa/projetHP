# Choix du texte

Nous avons choisi pour texte un extrait du roman Harry Potter afin de pouvoir comparer l’annotation automatique des mots propres à l’univers de J.K. Rowling avec les autres mots du roman soit parce que l’étiqueteur fonctionne avec un dictionnaire de langue française soit parce qu’il reconnaît les affixes des néologismes. 

Le début du chapitre 6 du tome 4 d’Harry Potter nous a semblé particulièrement approprié car il y apparaît à plusieurs reprises des mots non contenus dans le dictionnaire français. 

# Choix de l’annotation manuelle

## “qu’on”

Lors de l’annotation manuelle nous pouvons nous demander comment découper les tokens pour quelques cas tels que les apostrophes. Il y avait deux possibilités :

qu / ’ /on

qu’ / on

Nous avons choisi de garder l’annotation “qu’ ”, “on” car elle suit le découpage appliqué par l’UD (Universal Dependencies). En effet, choisir ce découpage permet de suivre la logique du tagger Stanford qui utilise les catégories d’UD pour catégoriser les mots.

## “y”

Nous choisissons également d’annoter le morphème “y” comme un pronom plutôt qu’un adverbe en nous basant sur les annotations déjà réalisées sur les corpus français en UD contrairement aux recommandations des dictionnaires français disponibles en ligne.

## “t”

Nous décidons également de ne pas séparer le “t” euphonique du pronom auquel il est rattaché dans le cas “murmura-t-elle”.

# Objectif du script python

## Tagger automatiquement

Afin d’étiqueter automatiquement l’extrait choisi, nous avons importé la bibliothèque nltk qui dispose de l’étiqueteur Stanford ainsi que l’étiqueteur SpaCy.
	
### Stanford

Cet étiqueteur a différentes utilisations selon la langue que nous voulons étiqueter. En effet pour l’anglais et le russe il suffit tout simplement de l’importer via le module nltk sans spécifier Java, comme explicité dans la documentation de StanfordPOSTagger ci-dessous :
	 
	  from nltk.tag import StanfordPOSTagger
	  st = StandfordPOSTagger('english-bidirectional-distsim.tagger')
	  st.tag('What is the airspeed of an unladen swallow ?'.split())

Pour le français, nous importons aussi StanfordPOSTagger par le biais d’nltk mais nous devons spécifier l’environnement où se trouve Java afin que ce dernier puisse fonctionner.

		java_path = chemin/java.exe
		os.environ['JAVAHOME'] = java_path

Nous devons aussi spécifier où se trouve le tagger (stanford-postagger.jar) et le modèle de référence (french-ud.tagger).

	jar = 'chemin/stanford-postagger.jar'
	model = 'chemin/french-ud.tagger'

Il ne nous reste plus qu’à définir que le module StanfordPOSTagger doit utiliser comme modèle de référence “model” et qu’il doit suivre les instructions des fichiers java contenus dans “jar”.

	pos_tagger = StanfordPOSTagger(model,jar, encoding='utf-8')

Maintenant que le tagger est prêt à être utilisé, nous ouvrons les deux fichiers qui nous seront utiles : le texte contenant les mots à étiqueter (“text”) et le texte qui contiendra le résultat (“resultat”).

	f = "chemin/Harry_Potter_T4_Ch6-P1-2.txt"
	resultat = open(texte_tagge_auto.txt, "w", encoding="utf-8")
	text = open(f, encoding="utf-8").read()

Pour pouvoir utiliser le tagger sur notre texte il faut d’abord le tokéniser. Pour ce faire, nous allons utiliser le module word_tokenize du module nltk (importé précédemment). 

	text_final = pos_tagger(word_tokenize(text))

Notre texte est maintenant tokénisé et étiqueté sous la forme d’une liste mais nous voulons que chaque mot du texte ainsi que sa catégorie soient sur une seule ligne afin qu’il soit plus simple pour nous de les traiter par la suite.

Nous utilisons une boucle for qui va écrire dans un fichier ligne par ligne, à chaque tour de boucle, le mot et son pos (part of speech).

	for word,pos in text_final:
		resultat.write("("+word+"/"+pos+")"+"\n")

Il ne nous reste plus qu’à fermer les fichiers avec la fonction `.close()`.

### SpaCy

SpaCy est une bibliothèque Python de traitement automatique des langues. Il permet par exemple la tokenization, la lemmatisation, le tagging POS, la reconnaissance de phrase ou d’entité, l’analyse des dépendances, etc. 
Les lignes de code suivantes sont utilisées pour effectuer la tokenization des mots et le POS tagging.

	 import spacy
	 nlp = spacy.load("fr_core_news_sm")
	 txt = open("chemin/Harry_Potter.txt, encoding='utf-8').read()
	 doc = nlp(txt)
	 for token in doc:
	 	print(token.text,token.pos)

Figure 1. script

## Comparer les annotations

### Décaler les lignes selon les erreurs

Afin de comparer automatiquement le fichier d’annotation manuelle avec le fichier d’annotation réalisé par l’étiqueteur Stanford, nous faisons face au problème de la différence de tokenisation qui se traduit en deux cas :

#### cas 1 :

|		|	AUTO TOKENISATION	|	MANUAL TOKENISATION	 |
| ------|-----------------------|------------------------|
|	1	|	(Harry/PROPN)		|	(Harry/) 			|
|	2	|	(eut/AUX)			|	(eut/)				|
|	3	|	(l'impression/NOUN)	|	(l’/) # décalage	|
|	4	|	(qu'il/PRON)		|	(impression/)		|
|	5	|	(venait/VERB)		|	(qu’/)				|
|	6	|	(tout/ADV)			|	(il/)				|
|	7	|	(juste/ADV)			|	(venait/)			|
|	8	|	(de/ADP)			|	(tout/)				|
|	9	|	(se/PRON)			|	(juste/)			|
|	10	|	(coucher/VERB)		|	(de/)				|

tableau 1 - représentation du décalage de ligne suite à une différence de tokenisation
	
On remarque qu’à cause de la séparation sur l’apostrophe faite dans l’annotation manuelle mais non réalisée dans l’annotation automatique, tous les mots suivant la différence de tokenisation sont décalés. Et ce décalage s'accroît à chaque nouvelle différence.

Il faut donc trouver un moyen pour comparer les tokens tout en prenant en compte cette difficulté. Nous avons choisi de faire une comparaison ligne par ligne des tokens. La solution est donc d’ajouter des lignes pour contrebalancer le décalage.
 
	 		if len(auto_word) > len(man_word) and 
	 		re.search(man_word,auto_word) is not None and 
 			man_word[-1] != auto_word [-1] :
          
        		   textes.write(auto_word+"		"+man_word+"\n")
        		   textes.write(auto_pos+"	"+man_pos+"\n\n")
        		   print("-", end="")
 	
        		   new_line = "(%s/%s)"%(auto_word,auto_pos)
        		   auto_lines.insert(i,new_line)
 
image 2 - Résolution du décalage des lignes dû à la tokenisation différente


|		|AUTO TOKENISATION		|	MANUAL TOKENISATION |
|-------|-----------------------|-----------------------|
|	1	|(Harry/PROPN)			|	(Harry/)			|
|	2	|(eut/AUX)				|	(eut/)				|
|	3	|(l'impression/NOUN)	|	(l’/) 				|
|	4	|						|	(impression/)
|	5	|(qu'il/PRON)			|	(qu’/)
|	6	|						|	(il/)
|	7	|(venait/VERB)			|	(venait/)
|	8	|(tout/ADV)				|	(tout/)
|	9	|(juste/ADV)			|	(juste/)
|	10	|(de/ADP)				|	(de/)

tableau 2 - correction du décalage de ligne suite à une différence de tokenisation

#### cas2 :

Non présent dans notre extrait

|	  |		AUTO TOKENISATION		|		MANUAL TOKENISATION  |
|-----|-----------------------------|----------------------------|
|	1 |	 (“pomme de terre”, NOUN)	|		(‘pomme’, NOUN)
|	2 | 							|		(‘de’, DET)
|	3 | 							|		(‘terre’, NOUN)

tableau 3 - représentation du décalage de ligne suite à une différence de tokenisation

Pour faire un travail global et réutilisable, il nous faut aussi prendre en compte le cas inverse de décalage des lignes. C'est-à-dire la division manuelle en plusieurs token lorsque l’étiqueteur ne voit qu’un seul mot.

Il suffit pour cela d’inverser le script précédent.

### Réaliser les mesures 

Nous avons besoin, pour réaliser les mesures d'évaluations, du nombre de vrais positifs, faux positifs et faux négatifs.

précision = nb de bon résultats trouvésnb de résultats à trouver=vrai positifvrai positif+faux positif

rappel=nb de bon résultats trouvésnb de résultats trouvés=vrai positifvrai positif+faux négatif

f-mesure=2(précision  rappel)/(précision + rappel)

En nous basant sur les formules ci-dessus, nous pouvons utiliser la longueur des fichiers au dénominateur plutôt que les vrais positifs et faux positifs. Nos formules sont donc :

	p = (vrai_positif)/(len(man_lines))
	r = (vrai_positif)/(len(auto_lines))
 	if p!=0 or r!=0 : #On evite le cas où la précision et le rappel
 	seraient == 0 pour les 2 premières décimal (python arrondi alors à 0)
    		f= 2*(p*r)/(p+r)
 	else :
    		f = 'div/zero'

image 3 - calcul des mesures de vérifications

# Utilisation du script

Le fichier `Harry_Potter_T4_Ch6-P1-2.txt` contient le texte brut du début du chapitre 6 pour nous avons étudié
Nous avons ensuite tokenisé ce texte à l'aide de 2 méthodes différentes :
- Stanford avec le script `StanfordTok.py`
        dont la sortie est le fichier `StanfordAutoTokenized.txt`
- SpaCy avec le script `SpacyTok.py`
        dont la sortie est le fichier `SpacyAutoTokenized.txt`

Nous avons également procédé à un pré-découpage du texte pour en faciliter l'annotation manuelle avec le script `cutText.py`

Le script `alignement.py` regroupe l'alignement des mots entre eux ainsi que la comparaison des POS et le calcul des mesures d'évaluation.
Il s'utilise suivi du nom du fichier à comparer avec l'annotation manuelle :
    'python3 alignement.py StandfordAutoTokenized.txt'
    'python3 alignement.py SpacyAutoTokenized.txt'

Les résultats finaux sont consignés dans le fichier `POSDifferences.txt`

# Analyse des résultats

## Stanford

### La différence de tokenisation

La principale différence entre l’étiqueteur et l’annotation automatique semble être la découpe des mots.

Par exemple : (d’aller) au lieu de (d’)(aller), ce qui va donner lieu à des problèmes d’étiquetage par la suite.

### Les verbes

Une erreur assez fréquente que l’on peut voir est l’étiquetage des verbes “avoir” et “être” comme étant des auxiliaires. Cette erreur s’explique sûrement par le fait qu’il est beaucoup plus probable que des formes verbales telles que “eut”, “fut”, “sont”, “a” soient des auxiliaires.

Les mots polysémiques tels que “lit” ont aussi mal été étiquetés.

### Les déterminants

Parfois le taggeur va donner - à tort - la catégorie déterminant à un pronom, un nom ou ne pas reconnaître le déterminant. 

Exemples : “Mrs Weasley vint le[DET] réveiller” “demanda-t-il d’un ton[DET] anxieux” “une grosse marmite de[ADP] porridge”.

### Les adverbes

Une autre erreur assez fréquente de la part de Stanford est l’étiquetage des tokens comme étant des adverbes. On peut trouver tout types de catégories mal étiquetées tels que les pronoms (“il peut y avoir”) et les noms (“un très vieux jean).

### Les mots spécifiques au texte

Étonnamment l’étiqueteur est assez bon avec les mots spécifiques au monde d’Harry Potter. Ses seules erreurs sont l'étiquetage de “Moldu” et de “Transplaner” comme étant des noms propres. Cela pourrait potentiellement s’expliquer par le fait qu’ils aient une majuscule en début de mot alors qu’ils se trouvent en milieu de phrase.

## Spacy

### La tokenisation

Dans le cas de l’apostrophe qui sert de signe typographique marquant l’élision des voyelles finales de certains mots en français, Spacy a segmenté en deux groups par exemple comme le résultat montre ci-dessous “C’est” -> “ C’ ” et “est”, “l’heure” -> “ l’ ” et “heure”.


		 Figure 2. apostrophe

L’autre part, dans les phrases interrogatives, telles que la phrase fréquente “est-ce que”, ou dans les phrases incises, telles que la combinaison “dit-il”, pour ces genres d'inversion du sujet, on ajoute un trait d'union. En ce qui concerne ce point, la bibliothèque le traite de la manière suivante, “demanda-t-il” -> “demanda”, “-t”, “-il” : 


            Figure 3. trait d’union 1

C'est le cas pour le traitement des traits d'union lorsqu'ils apparaissent dans les phrases plutôt écrites. En outre, dans l’expression parlée, nous rencontrons une autre situation. Comme il apparaît dans cet article de Harry Potter, “Charlie et Pe-e-e-e-e-e-ercy ?”, il a séparé chaque tiret :


         Figure 4. trait d’union 2

### Les verbes

En même temps, nous avons trouvé des erreurs d'étiquetage très évidentes et nous les avons listées ci-dessous. Comme ce mot “dégagé”, il est étiqueté comme un verbe parce qu'il se termine par un é, mais il s'agit en fait d'un adjectif. 

         Figure 5. POS  erreurs

Spacy reconnaît régulièrement les verbes comme des adjectifs ou des noms :


|	AUTO TOKENISATION	|	MANUAL TOKENISATION		|
|-----------------------|---------------------------|
|	chercha	 			|		chercha				|
|	ADJ 				|		VERB
|						|
|	murmura 			|		murmura
|	NOUN				|		VERB

tableau 5 - exemple d’erreur par l’étiqueteur Spacy

Mais aussi les adjectifs issus de verbes comme des verbes :

|	AUTO TOKENISATION	|	MANUAL TOKENISATION		|
|-----------------------|---------------------------|
|	indistinct  		|		indistinct 			|
|	NOUN				|		ADJ
|						|
|	échevelées 			|		échevelées
|	VERB				|		ADJ

tableau 6 - exemple d’erreur par l’étiqueteur Spacy

Ces erreurs nous indiquent la probable utilisation des affixes pour déterminer la catégorie grammaticale des tokens par Spacy.
Les adpositions

La distinction entre les adpositions et les déterminants pose problème à l’étiqueteur de Spacy. Cette difficulté est liée à l’ambivalence du morphème “de” qui ce comporte parfois comme une adposition et parfois comme un déterminant. Les adpositions confondues avec leur déterminants sont aussi mal reconnus car il est en fait du choix de l’annotateur de les noter comme déterminants ou adposition.

### Erreurs d’annotation

Un certain nombre d’erreurs sont liées à des erreurs d’annotations manuelles : des fautes de frappes ou des utilisations de conventions différentes
### Les mots spécifiques au texte

Comme nous nous y attendions, les mots spécifiques à Harry Potter comme “transplaner”, "désartibuler" ou “Quidditch” posent 	problèmes à l'étiqueteur. 

|		AUTO TOKENISATION	|	MANUAL TOKENISATION	|
|---------------------------|-----------------------|
|	Transplaner		 		|	Transplaner			|
|	PROPN 					|	VERB				|
|							|						|
|	désartibulés 			|	désartibulés		|
|	NOUN 					|	ADJ					|
|							|						|
|	transplané 				|	transplané			|
|	AUX 					|	VERB				|
|							|						|
|	Moldus 					|	Moldus				|
|	NOUN 					|	PROPN				|
|							|						|
|	Quidditch 				|	Quidditch			|
|	NOUN				 	|	PROPN				|
tableau 6 - exemple d’erreur par l’étiqueteur Spacy

## Comparaison des deux étiqueteurs


|				|		Précision	|	Rappel		|	F-mesure|
|---------------|-------------------|---------------|-----------|
|	Stanford	|		79.41%		|	79.41%		|	79.41%  |
|	Spacy		|		80.09%		|	80.09%		|	80.09%	|
	

tableau 4 - résultats des étiqueteurs sur le texte Harry Potter
# Conclusion

Cette étude a permis de comparer le résultat de l’annotation automatique et celui de l’annotation manuelle sur un extrait du roman Harry Potter. Nous nous focalisons surtout sur la distribution de catégories pour les OOV (Out-of-vocabulary words : termes qui ne font pas partie du lexique normal que l’on trouve dans un environnement de traitement du langage naturel), y compris les noms propres et les néologismes qui pourraient poser des problèmes pour l’étiqueteur.

À la suite de notre analyse, il est donc évident maintenant que non seulement l’étiqueteur Stanford mais aussi l’étiqueteur SpaCy ont réalisé une meilleure performance pour les mots que l’on trouve dans les dictionnaires que les OOV. Et en tant qu’étiqueteurs automatiques, Stanford et SpaCy ont eu tous les deux des problèmes sur l’annotation de certaines catégories. Les erreurs viennent parfois d’analyses erronées des structures syntaxiques et de polysémies.

Comme nous avons pu le voir à de multiples reprises, l’unité euphorique “t” ne peut être annoté correctement car le modèle d’annotation sur lequel repose le modèle d'entraînement est UD. Cette annotation ne catégorise pas ce phénomène linguistique mais rattache l’unité euphonique au pronom qui le suit et la catégorie de “t” est effacée par la catégorie PRON du token auquel il est rattaché. 

		TEXTE ORIGNAL	       ANNOTATION UD
		murmura-t-elle      	murmura/VERB
	   						   -t-elle/PRON

Il serait donc intéressant de rajouter une catégorie le traitant tel que UEUPH.

Notre projet est disponible en ligne sur Github à l’adresse : https://github.com/EveSa/projetHP


