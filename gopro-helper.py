from os import chdir
from os import mkdir
from os import listdir
from shutil import copy2
from os.path import exists
from os import rename

# целевой путь в файловой системе (должен быть на сд карте где видосы)
target_path = 'F:/DCIM/100GOPRO'
# меняем текущую рабочую директорию на целевой путь
chdir(target_path)
directory = listdir()
# записала список файлов в переменную
temp_dir_path = 'D:/Рабочий стол/gopro'
if exists(temp_dir_path) == False:
    # создаю временную папку на рабочем столе, если ее нет
    mkdir(temp_dir_path)

# перекидываем видосы с метаданными
for file in directory:
    if file.endswith(".MP4") or file.endswith(".mp4"):
        copy2(file, temp_dir_path)
# засовываю данные о видосах в словарь # не, иди нахуй
mylist = []
for file in directory:
    path = file
    name = file.split('.')[0]

    # сортирую по типу записи, назначаю переменные для данных чтобы запихнуть в словарь 
    if name.startswith('GOPR'):
        role = 'main'
        ID = name[4:]
        options = {'id': ID, 'is': role, 'path': path, 'chapters': []}
    elif name.startswith('GP'):
        role = 'chapter'
        ID = name[4:]
        position = name[2:4]
        options = {'id': ID, 'is': role, 'path': path, 'position': position}
        
    
    mylist.append(options)

  
#  добавила к данным основной записи данные о дополнительных
mainonlylist = []
for record in mylist:
    isChapter = record['is'] == 'chapter'
    if isChapter:
        for another_record in mylist:
            sameId = record['id'] == another_record['id']
            isMain = another_record['is'] == 'main'
            if isMain and sameId:
                another_record['chapters'].append(record)

# тут я переношу мейны со вложенными чаптерами в другой словарь, чтобы не удалять чаптеры из прошлого 
for record in mylist:
    isMain = record['is'] == 'main'
    if isMain:
        mainonlylist.append(record)

#сортирую видосы по айдишникам
sortedIds = sorted(mainonlylist, key=lambda x: x['id'])
rename_plan = []
iterator = 1
#делаю план по переименовыванию видосов
for record in mainonlylist:
    rename_plan.append({'oldName': record['path'],
    'newName': str(iterator) + '.mp4'})
    iterator = iterator + 1
    if record['chapters'] is not None:
        for chapter in record['chapters']:
            rename_plan.append({'oldName': chapter['path'],
    'newName': str(iterator) + '.mp4'})
            iterator = iterator + 1
#собственно переименовываю видосы    
for entry in rename_plan: 
  oldName = entry['oldName'] 
  newName = entry['newName'] 
   
  rename(oldName, newName)