#!/usr/bin/python2.7
#-*- coding: utf-8 -*-

import os, glob, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname( __file__), os.pardir))
BIB = os.path.abspath(os.path.join(os.path.dirname( __file__), os.pardir)) + '/bibliography/'
SYS = os.path.abspath(os.path.dirname( __file__))

def touch(path):
    ''' touch(str) -> /
        ------
        Créer un fichier vide
    '''
    f = open(path, 'w')
    print('[OK] Le fichier '+ path +' a été créé')
    f.close()

def formatName(name):
    ''' formatName(str) -> str
        ------
        formate la chaine de caractère en chaine sans accents avec les espaces et la ponctuation en underscore (_)
    '''
    replace_accents = {'e': ['é','è','ê','ë'],
                       'a': ['à','â','ä'],
                       'i': ['ì','î','ï'],
                       'o': ['ò','ô','ö'],
                       'u': ['ù','û','ü'],
                       '_': [' , ',', ',' ,',',',
                             ' : ',': ',' :',':',
                             ' ; ','; ',' ;',';',
                             ' . ','. ',' .','.',
                             ' ']}
    for letter in replace_accents:
        for accent in replace_accents[letter]:
            name = name.replace(accent, letter)
    return (name)

def importDataFile(directory): ######## Penser à faire un objet pour le data file
    ''' convertDataFile(str) -> dict
        ------
        Convertit les données du fichier .data du répertoire en dictionnaire
    '''
    exists(directory + '/.data')
    f = open(directory + '/.data', 'r')
    datas = {}
    for line in f:
        line_data = line.split('=')
        datas[line_data[0]] = line_data[1][:-1]
    return datas
    f.close()

def updateDataFile(directory, datas):
    ''' updateDataFile(str, dict) -> /
        ------
        Met à jour les données du fichier .data du répertoire
    '''
    # print directory
    old_data = importDataFile(directory)
    string = ""
    for data in datas:
        string += data + "=" + datas[data] + '\n'
    f = open(directory + '/.data', 'w')
    f.write(string)
    f.close()

def error(string):
    ''' error(str) -> /
        ------
        Imprime une erreur puis quitte le programme
    '''
    print('[ERROR] ' + string)
    exit()

def exists(file_name):
    ''' exists(str) -> /
        ------
        Si le fichier ou répertoire n'existe pas, une erreur est affichée et le programme est arrêté
    '''
    if glob.glob(file_name) == []:
        if os.path.isdir(file_name): error('Le répertoire ' + file_name + ' n\'existe pas')
        error('Le fichier ' + file_name + ' n\'existe pas')
        exit()

def getDir(dir_name):
    ''' getDir(str) -> str
        ------
        Donne le chemin relatif du répertoire, si il existe
    '''
    dir_name_format = formatName(dir_name)
    for path, dirs, files in os.walk('.'):
        for directory in dirs:
            if dir_name_format == directory:
                return os.path.join(path, directory)
    error('Le répertoire ' + dir_name_format + ' n\'esiste pas')

def sortDir(dir_list):
    ''' sortDir(list) -> list
        ------
        Renvoie une liste de répertoires numérotés triés.
    '''
    i = len(dir_list)
    while i >= 1:
        for j in range(i-1):
            if int(re.search('^([0-9]+)-.*', dir_list[j+1]).group(1)) < int(re.search('^([0-9]+)-.*', dir_list[j]).group(1)):
                tmp = dir_list[j+1]
                dir_list[j+1] = dir_list[j]
                dir_list[j] = tmp
        i-=1
    return dir_list

def getAllDirNumber(search_dir):
    ''' getAllDirNumber(str) -> list
        ------
        Renvoie la liste de tous les répertoires de parties ou chapitre
    '''
    dir_list = []
    for directory in os.listdir(search_dir):
        if (re.match('^[0-9]+-', directory) is not None and os.path.isdir(search_dir + "/" + directory)):
            dir_list += [directory]
    return dir_list

def getLastDirNumber(search_dir = '.'):
    ''' getLastDirNumber(str) -> int
        ------
        Donne la valeur la plus haute dans les répertoires notés du répertoire en paramètre.
    '''
    higher_value = 0
    for directory in os.listdir(search_dir):
        if (re.match('^[0-9]+-', directory) is not None and os.path.isdir(search_dir + "/" + directory)):
            value = int(re.search('^([0-9]+)-.*', directory).group(1))
            if value > higher_value:
                higher_value = value
    return higher_value

def makeDir(name, dest_dir='.'):
    ''' makeDir(str, str) -> /
        ------
        Créer un répertoire dont le nom est formaté dans un répertoire de destination.
    '''
    exists(dest_dir)
    name_format = str(getLastDirNumber(dest_dir)+1) + '-' + formatName(name)
    os.mkdir(dest_dir + '/' + name_format)
    print('[OK] Le répertoire ' + name_format + ' a été créé')

def getFileContent(file_name):
    ''' getFileContent(str) -> str
        ------
        récupère l'ensemble des lignes d'un fichier en paramètre
    '''
    content = ""
    f = open(file_name, 'r')
    for line in f:
        content += line
    return content

def fillTemplateLine(line, replace):
    ''' fillTemplateLine(str, dict) -> str
        ------
        Remplis la ligne par les informations en paramètres
    '''
    for pattern in replace:
        line = re.sub('<\+\+ '+ pattern[0] +' \+\+>',pattern[1] ,line)
    return line

def copyFile(file_name, dest_file, replace=[]):
    ''' copyFile(str, str) -> /
        ------
        Copie un fichier à sa destination et modifie toutes les informations des pattern de la forme <++ xxx ++>, si le remplacement est renseigné.
    '''
    exists(file_name)
    new_file = open(dest_file, 'w');
    new_file.write(fillTemplateLine(getFileContent(file_name), replace))
    new_file.close()
    print('[OK] Le fichier ' + dest_file + ' a été créé')

def createImports(dir_id, directory=''): # La compilation d'une partie n'est pas possible parce qu'elle as des chemins relatifs pour la thèse en entier
    ''' createImports(str) -> /
        ------
        Remplis de fichier imports.tex avec les répertoires numérotés du répertoire courant, dans l'ordre.
    '''
    abs_directory = ROOT + directory
    dir_list = sortDir(getAllDirNumber(abs_directory))
    if dir_list == []: return ""
    input_string = ""
    for dir_name in dir_list:
        data = importDataFile(abs_directory + '/' + dir_name)
        replace = [['TITLE', data['title']], ['ID', data['id']], ['PATH', abs_directory + '/' + dir_name]]
        if os.path.exists(dir_name + '/imports_'+ data['id'] +'.tex'):
            replace += [['TYPE', 'part']]
        else:
            replace += [['TYPE', 'chapter']]
        input_string += fillTemplateLine(getFileContent(SYS + '/default_contents/import.template.tbr'), replace) + '\n'
        createImports(data['id'], directory + '/' + dir_name)
    input_file = open(abs_directory + '/imports_'+ dir_id +'.tex', 'w')
    input_file.write(input_string)
    input_file.close()

def updateMainFile(file_name, regexp, new_str):
    content = getFileContent(file_name)
    content = re.sub(regexp, new_str ,content)
    f = open(file_name, 'w')
    f.write(content)
    f.close()

def updateBibRef(current_dir = ROOT):
    os.chdir(current_dir)
    all_dir = getAllDirNumber('.')
    all_bib = ""
    for bib_file in os.listdir(BIB):
        all_bib += BIB + bib_file[:-4] + ', '
    all_bib = all_bib[:-2]
    if os.path.exists('chapter.tex'):
        updateMainFile('chapter.tex', 'bibliography\{[^\}]*\}', 'bibliography{'+ all_bib +'}')
    elif os.path.exists('part.tex'):
        updateMainFile('part.tex', 'bibliography\{[^\}]*\}', 'bibliography{'+ all_bib +'}')
    elif os.path.exists('these.tex'):
        updateMainFile('these.tex', 'bibliography\{[^\}]*\}', 'bibliography{'+ all_bib +'}')
    else:
        error('Le fichier principal du répertoire (these.tex, part.tex, chapter.tex) n\'existe pas')
    for directory in all_dir:
        updateBibRef(directory)
        os.chdir('..')

def newPart(title, part_id):
    makeDir(formatName(part_id), '.')
    os.chdir(str(getLastDirNumber()) + '-' + formatName(part_id))
    touch('.data')
    updateDataFile('.',{'title': title, 'id': formatName(part_id)})
    copyFile(SYS + '/default_contents/newDir.template.tbr', 'part.tex', [['TITLE', title], ['PATH', ROOT], ['TYPE', 'part'], ['ID', formatName(part_id)]])
    copyFile(SYS + '/default_contents/makefile.template.tbr', 'makefile', [['TYPE', 'part']])
    copyFile(SYS + '/default_contents/part_content.template.tbr', 'plan-'+ formatName(part_id) +'.tex', [['ID', formatName(part_id)]])
    touch('imports_'+ formatName(part_id) +'.tex')
    os.chdir('..')
    updateBibRef(ROOT)

def newChapter(title, chapter_id, directory='.'):
    exists(directory)
    os.chdir(directory + '/')
    makeDir(formatName(chapter_id))
    os.chdir(str(getLastDirNumber()) + '-' + formatName(chapter_id))
    # new_dir = directory + '/' + str(getLastDirNumber()) + '-' + formatName(chapter_id)
    touch('.data')
    updateDataFile('.',{'title': title, 'id': formatName(chapter_id)})
    import_path = ""
    office = '../office/default_contents/'
    if directory != '.' :
        import_path = '../'
        office = '../' + office
    copyFile(SYS + '/default_contents/newDir.template.tbr', 'chapter.tex', [['TITLE', title], ['PATH', ROOT], ['TYPE', 'chapter'], ['ID', formatName(chapter_id)]])
    copyFile(SYS + '/default_contents/makefile.template.tbr', 'makefile', [['TYPE', 'chapter']])
    copyFile(SYS + '/default_contents/chapter_content.template.tbr', 'plan-'+ formatName(chapter_id) +'.tex', [['ID', formatName(chapter_id)]])
    if directory != '.' :
        os.chdir('../..')
    else:
        os.chdir('..')
    updateBibRef()



def newBib(bib_name):
    touch(ROOT + '/bibliography/' + bib_name)
    updateBibRef(ROOT)


#####################################################################
#####################################################################

if sys.argv[1] == 'newpart':
    if len(sys.argv) < 4:
        error('Le nombre de paramètres est de ' + str(len(sys.argv)-1) + ' au lieu de 3')
    newPart(sys.argv[2], sys.argv[3])
    createImports('thesis')
elif sys.argv[1] == 'newchapter':
    if len(sys.argv) < 4:
        error('Le nombre de paramètres est de ' + str(len(sys.argv)-1) + ' au lieu de 3')
    if len(sys.argv) > 4:
        newChapter(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        newChapter(sys.argv[2], sys.argv[3])
    createImports('thesis')
elif sys.argv[1] == 'update':
    createImports('thesis')
    print "[OK] Les importations sont mises à jour"
    updateBibRef(ROOT)
    print "[OK] La biblio a été mise à jour"
elif sys.argv[1] == 'newbib':
    if len(sys.argv) < 3:
        error('Le nombre de paramètres est de ' + str(len(sys.argv)-1) + ' au lieu de 2')
    newBib(sys.argv[2])
