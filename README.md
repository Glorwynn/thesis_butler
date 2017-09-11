# Thesis Butler
## DESCRIPTION
**Thesis Butler** est un assistant de rédaction de thèse. Son but est de faciliter la rédaction pour que le doctorant n'ait qu'à ce concentrer sur le contenu de sa thèse au lieu de la structure de son LaTeX.

Il est basé sur une méthode de rédaction qui se déroule en deux étapes :
- La rédaction d'un *plan détaillé* dans lequel toutes les idées sont posées sous la forme de listes afin de poser les idées et les structurer au sein du chapitre. Chaque élément des listes correspond à une idée qui pourra être développé dans un seul paragraphe. Il s'agit de la partie la plus "difficile" et la plus importante.
- La rédaction à proprement parlé commence. On parcours toute la thèse en rédigeant chaque élément des listes presque mécaniquement (on est pas à l'abris d'un petit changement dans l'ordre des idées)

C'est un outil développé par un doctorant, pour des doctorants. Si vous souhaitez contribuer, ajoutez et améliorez des fonctionnalités puis faites tourner :)

## STRUCTURE
    /
    |--office/
       |--default_contents/
          |--chapter_content.template.tbr
          |--import.template.tbr
          |--makefile.template.tbr
          |--newDir.template.tbr
          |--part_content.template.tbr
       |--tests/
          |--tests.py
       |--env.tex
       |--config.tex
       |--thesis_butler.py
    |--bibliography/
    |--header/
       |--packages.tex
       |--macros.tex
    |--front_page/
       |--i3s.png
       |--uca.png
       |--front_page.tex
    |--tb
    |--README.md
    |--imports.tex
    |--makefile
    |--content.tex
    |--thesis.tex

## COMMANDES
Cette section contient la liste des commandes de **TB**. Si vous contribuez, merci de les ajouter à cette liste.
### Les parties
#### Création de parties
    part create <titre de la partie> <label de la partie>
Le titre de la partie est celui qui apparaitra dans le PDF après compilation alors que le label sera dans le nom du répertoire et le label de la partie dans le fichier .tex. Les espaces contenus dans le label seront convertis en underscore.
#### Compilation simple
    part <repertoire de la partie> simple
Execute une unique compilation du part.tex du répertoire
#### Compilation complète
    part <repertoire de la partie> complete
Execute une compilation du .tex suivie d'une compilation de la biblio puis de 2 compilation du .tex. L'objectif est de mettre à jour le plan et la bibliographie.
#### Ouverture du PDF
    part <repertoire de la partie> open
Ouvre le PDF `part.pdf` du répertoire
### Les chapitres
#### Création de chapitres
    chapter create <titre de la partie> <label de la partie>
Le titre de la partie est celui qui apparaitra dans le PDF après compilation alors que le label sera dans le nom du répertoire et le label de la partie dans le fichier .tex. Les espaces contenus dans le label seront convertis en underscore.
#### Compilation simple
    chapter <repertoire de la partie> simple
Execute une unique compilation du part.tex du répertoire
#### Compilation complète
    chapter <repertoire de la partie> complete
Execute une compilation du .tex suivie d'une compilation de la biblio puis de 2 compilation du .tex. L'objectif est de mettre à jour le plan et la bibliographie.
#### Ouverture du PDF
    chapter <repertoire de la partie> open
Ouvre le PDF `part.pdf` du répertoire
### Ajout d'un fichier de biblio
    new-bib <nom du fichier bib>
Ajoute un fichier de biblio dans le répertoire `biblio` et ajoute son référencement dans les fichiers `these.tex`, `part.tex` et `chapter.tex` de la thèse.
### Mise à jour des références
    update
Met à jour les importations dans les fichiers `imports_*.tex` de tous les répertoires de la thèse, ainsi que les références des fichiers de biblio dans les fichiers  `these.tex`, `part.tex` et `chapter.tex`.
### Préparer la rédaction d'un chapitre
    go-write <nom_du_chapitre>
Cette commande convertit, dans un nouveau fichier, tous les éléments des listes du fichier de plan détaillé et les place dans des balises facilitant la rédaction.
### Affichage du plan
    ls [nom] [option]
Affiche dans la console le plan de la thèse, partie ou chapitre indiqué. Les options disponibles sont :
- `-u` Affiche uniquement l'élément suivant (ex: `-us` affiche toutes les sections mais pas les chapitres et parties).
- `-p` Affiche toutes les parties.
- `-c` Affiche tous les chapitres de toutes les parties.
- `-s` Affiche toutes les sections de tous les chapitres de toutes les parties.
### Affichage d'un PDF d'exemple
    lorem [part | chapter]
Affiche un exemple de contenu pour tester la mise en page.
### Compilation de la thèse
    thesis <action>
Cette commande permet de gérer la thèse dans son ensemble. Les actions disponibles sont :
- `open` permet d'ouvrir le pdf correspondant avec `evince`
- `simple` permet de compiler une seule fois la thèse (pour de simples modification de contenu textuel)
- `complete` permet de compiler la thèse ainsi que la biblio de façon à ce que toutes les modifications de citations et de références soient pris en compte.
### Nettoyer un répertoire (thèse, partie ou chapitre)
    clean [nom_du_chapitre]
Cette commande permet de nettoyer le répertoire indiqué. Il supprime tous les fichiers générés par la compilation sauf le PDF.
### Archiver un répertoire (thèse, partie ou chapitre)
    archive [nom_de_la_partie] [nom_du_chapitre]
Cette commande permet d'archiver le répertoire indiqué. Il archive uniquement les fichier `tex`, `bib`, `pdf` et les ressources lié au document archivé.

## CONTRIBUTEURS
| Nom | Laboratoire     | Année de fin de thèse |
| :------------- | :------------- | :----------- |
| Emilien Cornillon       | Laboratoire I3S       | 2017 |
