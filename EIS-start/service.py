from datetime import datetime
import os
import shutil
import platform
import datetime
from pathlib import Path

import variables as vars


def log_l_ap_next():
    vars.log_data_list.append(str(f'\n----------\n\n'))


def log_l_ap_text(text):
    vars.log_data_list.append(str(f'{text}\n'))


def log_l_ap(text):
    vars.log_data_list.append(str(f'----------\n\n{text}\n'))


def get_info_for_log_file_name():
    username = os.getlogin().lower()
    data_time = str(datetime.datetime.strftime(datetime.datetime.today(), "%d.%m.%Y - %H.%M.%S"))
    file_name = f'Log_{username}_{data_time}'
    return file_name


def get_system_info():
    win = platform.platform()
    system = platform.machine()
    username = os.getlogin()
    data_time = str(datetime.datetime.strftime(datetime.datetime.today(), "%d.%m.%Y %H:%M:%S"))

    out_text = f'----------\n\nСистема: {win} __:__ {system}\nПользователь: {username}\nДата и время запуска: {data_time}\n\n----------\n'
    vars.log_data_list.append(out_text)


def copy_file_to_log_folder(path_from, file_name):
    to_ = os.path.join(vars.log_folder, file_name + '.txt')
    try:
        shutil.copy2(path_from, to_)
        print(f'Успешно скопировал файл на сервер!\n{to_}')
    except Exception as e:
        print(f'Не скопировал файл на сервер!\n{to_}\nПотому что: [{e}]')


def get_full_txt(file_name):
    log_file_path = os.path.join(vars.desktop, file_name + '.txt')
    # try:
    log_file = open(log_file_path, 'a')
    for item in vars.log_data_list:
        log_file.write("%s\n" % item)
    log_file.close()
    print(f'Успешно записал log файл!\n{log_file_path}')
    # except Exception as e:
    #     print(f'Не записал log файл!\n{log_file_path}\nПотому что: [{e}]')
    copy_file_to_log_folder(log_file_path, file_name)


