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