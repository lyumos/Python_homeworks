import os
import sys

file_1 = os.path.join(os.path.dirname(sys.argv[0]), '1.txt')
file_2 = os.path.join(os.path.dirname(sys.argv[0]), '2.txt')
file_3 = os.path.join(os.path.dirname(sys.argv[0]), '3.txt')

def create_rez_file(files):
    files_dict = {} #словарь, где каждый ключ(кол-во строк в файле) отображает имя определенного файла
    count_list = [] #список с кол-вом строк в файлах
    for file in files:
        with open(file,encoding="utf-8") as file_obj:
            count = sum(1 for line in file_obj)
            count_list.append(count)
            files_dict[count] = ''.join(list(os.path.splitext(os.path.basename(file)))),file
    count_list.sort() #сортируем список по возрастанию
    with open(os.path.join(os.path.dirname(sys.argv[0]), 'rez_file.txt'), 'w', encoding="utf-8") as rez_file_obj: #создаем и открываем результатирующий файл
        for count in count_list:
            for count_key in files_dict.keys():
                if count == count_key:
                    rez_file_obj.write(f'{files_dict[count_key][0]}\n{count}\n{open(files_dict[count_key][1],encoding="utf-8").read()}\n')

create_rez_file([file_1,file_2,file_3])