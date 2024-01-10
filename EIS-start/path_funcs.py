from pathlib import Path
import os

import tkinter.filedialog as fd

import check_funcs
import messages as mes
import variables as vars
from tkinter.messagebox import askyesnocancel


def check_path(path):
    print(Path(path))
    if Path(path).exists():
        return True
    else:
        return False


def get_temp_filepath():
    filetypes = [("Все файлы", ".*")]

    if vars.last_folder == '':
        vars.temp_path = fd.askopenfilename(title="Укажите файл установки браузера",
                                            initialdir=f"{vars.usr_docs}",
                                            filetypes=filetypes)
        if vars.temp_path != '':
            vars.last_folder = vars.temp_path
            return True
    else:
        vars.temp_path = fd.askopenfilename(title="Укажите файл установки браузера",
                                            initialdir=f"{vars.last_folder}",
                                            filetypes=filetypes)
        if vars.temp_path != '':
            vars.last_folder = vars.temp_path
            return True

    if vars.temp_path != '':
        if check_path(vars.temp_path):
            return True
        else:
            mes.error('Ошибка пути файла',
                      f'Путь {vars.temp_path} не существует!')
            return False
    else:
        mes.error('Ошибка пути файла',
                  f'Выберите файл установки!')
        return False


def get_temp_folderpath():
    if vars.last_folder == '':
        vars.temp_path = fd.askdirectory(title="Укажите запрашиваемый путь",
                                            initialdir=f"{vars.usr_docs}")
        if vars.temp_path != '':
            vars.last_folder = vars.temp_path
            return True
    else:
        vars.temp_path = fd.askdirectory(title="Укажите запрашиваемый путь",
                                         initialdir=f"{vars.last_folder}")
        if vars.temp_path != '':
            vars.last_folder = vars.temp_path
            return True

    if vars.temp_path != '':
        if check_path(vars.temp_path):
            return True
        else:
            mes.error('Ошибка пути файла',
                      f'Путь {vars.temp_path} не существует!')
            return False
    else:
        mes.error('Ошибка пути файла',
                  f'Выберите файл установки!')
        return False


def path_confirm(self, app):
    if vars.install_folder_changed_path != '' and check_funcs.check_connection(self, False):
        answer = askyesnocancel('Путь установки',
                                'Внимание!\nСоединение с сервером установлено, но вы задали собственный путь до установочных файлов.\nЖелаете продолжить?\n\nДа - продолжить установку по указанному вами пути.\nНет - использовать установочные файлы с сервера.\nОтмена - выход из программы.')
        if answer == True:
            vars.true_install_path = vars.install_folder_changed_path
            return True
        elif answer == False:
            vars.true_install_path = vars.install_folder
            return True
        else:
            app.on_close()
        # vars.path_confirmed = True
    elif vars.install_folder_changed_path != '' and not check_funcs.check_connection(self, False):
        vars.true_install_path = vars.install_folder_changed_path
        vars.path_confirmed = True
        mes.warning('Ручное указание пути',
                    f'Обращаем ваше внимание, что установка будет производиться по указанному вами локальному пути!')
        return True
    elif vars.install_folder_changed_path == '' and check_funcs.check_connection(self, False):
        vars.true_install_path = vars.install_folder
        vars.path_confirmed = True
        return True
    elif vars.install_folder_changed_path == '' and not check_funcs.check_connection(self, False):
        vars.true_install_path = ''
        vars.path_confirmed = False
        mes.error('Ручное указание пути',
                  f'Внимание!\n\nСоединение с сервером не обнаружено! Укажите путь к локальным файлам установки для возможности работы программы!')
        return False
    else:
        print('1')
