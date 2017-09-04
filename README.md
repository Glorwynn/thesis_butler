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
       |--env.tex
       |--new_part_content.tbr
       |--new_chapter_content.tbr
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
    |--makefile
    |--content.tex
- `thesis_butler` contient l'ensemble des fichiers dont **Thesis Butler** a besoin pour fonctionner.
- `front_page` contient la page de garde et les logos
- `header` contient l'ensemble des packages et des macros du documents. Si vous souhaitez ajouter d'autres packages, c'est ici.
- le fichier `content.tex` contient l'ensemble des importations des parties et chapitres de la thèse.

## COMMANDES
Cette section contient la liste des commandes de **TB**. Si vous contribuez, merci de les ajouter à cette liste.
### Création de parties
    new-part <nom de la partie>
Le nom de la partie en paramètre est convertis en snake_case. **TB** créer le répertoire puis un `makefile` (une copie de celui de la racine, dans lequel le fichier de référence `these` est changé en `part`) et enfin un fichier `part.tex` qui sera compilé si l'on souhaite un PDF ne contenant que la partie.
### Création de chapitres
    new-chapter <nom du chapitre> [->nom_de_la_partie]
Le nom du chapitre en paramètre est convertis en [snake_case](https://fr.wikipedia.org/wiki/Snake_case). **TB** créer le répertoire du chapitre dans la racine si le nom de la partie n'est pas renseignée, ou dans la partie si elle a été renseignée. Elle créer ensuite un `makefile` pour le chapitre, un fichier `chapter.tex` qui sera compilé si l'on souhaite un PDF ne contenant que le chapitre, et enfin un fichier de plan détaillé qui est remplis avec une section fictive. Une importation est alors ajoutée au fichier `content.tex` de son parent (la partie si il en fait partie, la thèse sinon).
### Préparer la rédaction d'un chapitre
    go-write <nom_du_chapitre>
Cette commande convertit, dans un nouveau fichier, tous les éléments des listes du fichier de plan détaillé et les place dans des balises facilitant la rédaction.
### Ajout d'un fichier de biblio
    new-bib <nom du fichier bib>
AJoute un fichier de biblio dans le répertoire `biblio` et ajoute son référencement dans le fichier `biblio.tex`.
### Compilation de la thèse
    thesis <action>
Cette commande permet de gérer la thèse dans son ensemble. Les actions disponibles sont :
- `open` permet d'ouvrir le pdf correspondant avec `evince`
- `simple` permet de compiler une seule fois la thèse (pour de simples modification de contenu textuel)
- `complete` permet de compiler la thèse ainsi que la biblio de façon à ce que toutes les modifications de citations et de références soient pris en compte.
### Compilation d'une partie
    part <action>
Cette commande permet de gérer une partie avec ses chapitres. Les actions disponibles sont :
- `open` permet d'ouvrir le pdf correspondant avec `evince`
- `simple` permet de compiler une seule fois la thèse (pour de simples modification de contenu textuel)
- `complete` permet de compiler le chapitre ainsi que la biblio de façon à ce que toutes les modifications de citation et de référence soient pris en compte.
### Compilation d'un chapitre
    chapter <nom_du_chapitre> <action>
Cette commande permet de gérer un chapitre. Les actions disponibles sont :
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
