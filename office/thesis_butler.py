#!/usr/bin/python2.7
#-*- coding: utf-8 -*-

import os, glob, re

def touch(path):
    ''' touch(str) -> /
        ------
        Créer un fichier vide
    '''
    f = open(path, 'w')
    print('[OK] Le fichier '+ path +'/imports.tex a été créé')
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
    if not os.path.exists(file_name):
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
    if not os.path.exists('imports.tex'):
        print '[ERREUR] Le répertoire '+ search_dir +' semble être un chapitre (absence de imports.tex).'
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
    content = ""
    f = open(file_name, 'r')
    for line in f:
        content += line
    return content

def fillTemplateLine(line, replace):
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


def createImports(directory='.'):
    ''' createImports(str) -> /
        ------
        Remplis de fichier imports.tex avec les répertoires numérotés du répertoire courant, dans l'ordre.
    '''
    exists(directory + '/imports.tex')
    dir_list = sortDir(getAllDirNumber(directory))
    input_file = open(directory + '/imports.tex', 'w')
    for dir_name in dir_list:
        data = importDataFile(directory + '/' + dir_name)
        replace = [['TITLE', data['title']], ['ID', data['id']], ['PATH', dir_name]]
        if os.path.exists(dir_name + '/imports.tex'):
            replace += [['TYPE', 'part']]
        else:
            replace += [['TYPE', 'chapter']]
        input_file.write(fillTemplateLine(getFileContent('office/default_contents/import.template.tbr'), replace) + '\n')
    input_file.close()

createImports()

def newPart(title, part_id):
    makeDir(formatName(part_id), '.')
    new_dir = str(getLastDirNumber()) + '-' + formatName(part_id)
    touch(new_dir + '/.data')
    updateDataFile(new_dir,{'title': title, 'id': formatName(part_id)})
    copyFile('office/default_contents/newDir.template.tbr', new_dir + '/' + 'part.tex', [['TITLE', title], ['PATH', ''], ['TYPE', 'part']])
    copyFile('office/default_contents/makefile.template.tbr', new_dir + '/' + 'makefile', [['TYPE', 'part']])
    copyFile('office/default_contents/part_content.template.tbr', new_dir + '/' + 'plan-'+ formatName(part_id) +'.tex')
    touch(new_dir + '/imports.tex')
    createImports()

def newChapter(title, chapter_id, directory='.'): ### Faire ça !
    makeDir(formatName(chapter_id), directory)
    new_dir = directory + '/' + str(getLastDirNumber()) + '-' + formatName(chapter_id)
    touch(new_dir + '/.data')
    updateDataFile(new_dir,{'title': title, 'id': formatName(chapter_id)})
    import_path = ""
    if directory != '.' : import_path = '../'
    copyFile('office/default_contents/newDir.template.tbr', new_dir + '/' + 'chapter.tex', [['TITLE', title], ['PATH', import_path], ['TYPE', 'chapter']])
    copyFile('office/default_contents/makefile.template.tbr', new_dir + '/' + 'makefile', [['TYPE', 'chapter']])
    copyFile('office/default_contents/chapter_content.template.tbr', new_dir + '/' + 'plan-'+ formatName(chapter_id) +'.tex')
    createImports(directory)

newPart('Les bibichats mignons', 'bichat mignon')
newPart('Les bibichats bidou', 'bichat bidou')
newChapter('Les bibichats minou', 'chat_minou')

def newBib(bib_name):
    pass

def goWrite(dir_name):
    pass

def lorem(dir_name=None):
    pass

def content(dir_name=None):
    pass
