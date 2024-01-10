import os
from tkinter.messagebox import askyesnocancel, askyesno
from tkinter import simpledialog
from pathlib import Path
import shutil
import subprocess

from comtypes.client import CreateObject
import comtypes.gen

import check_funcs
import service
import variables as vars
from check_funcs import *
import messages as mes


def install_shortcut(self):
    def repath_shortcut(browserWDir, url, name):
        import glob
        import win32com.client
        import winshell

        paths = glob.glob(winshell.desktop() + "\\*.lnk")
        # shell = win32com.client.Dispatch("WScript.Shell")
        shell = CreateObject("WScript.Shell")

        # проверяем каждый путь на рабочем столе
        for path in paths:
            # получаем атрибуты ярлыка
            shortcut = shell.CreateShortCut(path).QueryInterface(comtypes.gen.IWshRuntimeLibrary.IWshShortcut)
            wDir = shortcut.WorkingDirectory
            target = shortcut.Targetpath
            username = str(os.getenv('USERNAME')).lower()
            file_name = ''
            if name != '':
                file_name = name
            else:
                file_name = 'Закупки'
            service.log_l_ap_text(f'#Создание ярлыка: В переименовании ищем ярлык {file_name}.')
            end_file_name_from_path = os.path.basename(path).split('.')[0] + '.lnk'

            # если у ярлыка в рабочей папке нет имени пользователя, то заменяем на папку установки браузера
            if end_file_name_from_path == file_name + '.lnk':
                if not username in wDir:
                    service.log_l_ap_text(f'#Создание ярлыка: Обнаружен ярлык с рабочей папкой без имени пользователя! [{path}] wdir - [{wDir}], меняем на [{browserWDir}].')
                    print('Нашел ярлык с неверной рабочей папкой', path)
                    shortcut.WorkingDirectory = browserWDir
                    shortcut.save()
                    print(f'Изменил директорию {path}')
                    service.log_l_ap_text(f'#Создание ярлыка: Обновлена рабочая папка.')

            # # если у ярлыка в рабочей папке нет имени пользователя, то заменяем на папку установки браузера
            # if name != '' and name in str(path) or name == '' and 'Закупки' in str(path):
            #     if not username in wDir:
            #         print('Нашел ярлык с неверной рабочей папкой', path)
            #         shortcut.WorkingDirectory = browserWDir
            #         shortcut.save()
            #         print(f'Изменил директорию {path}')

            # проверяем объект в ярлыке
            if url == '':
                # если у ярлыка в объекте нет имени пользователя, то заменяем на путь до браузера + ссылка
                browser_object = ''
                if end_file_name_from_path == 'Закупки.lnk':
                # if 'Закупки' in str(path):
                    if not username in target:
                        service.log_l_ap_text(f'#Создание ярлыка: Найден ярлык с объектом без имени польз-я [{target}].')
                        print('Нашел ярлык для замены объекта', path)
                        if 'Yandex' in browserWDir:
                            browser_object = str(browserWDir + r'\browser.exe')
                        elif 'Chromium' in browserWDir:
                            browser_object = str(browserWDir + r'\chrome.exe')
                        # shortcut.Targetpath = browser_object + ' https://lk.zakupki.gov.ru/44fz/entrypoint/welcome.html'
                        shortcut.Targetpath = browser_object
                        service.log_l_ap_text(f'#Создание ярлыка: Новый объект - [{browser_object}].')
                        args = [' https://lk.zakupki.gov.ru/44fz/entrypoint/welcome.html', ]
                        shortcut.Arguments = " ".join(args)
                        shortcut.Save()
                        service.log_l_ap_text(f'#Создание ярлыка: Добавлена ссылка - [{args}].')
                        break
                    else:
                        continue
                else:
                    continue
            else:
                # если нужно заменить в ярлыке ссылку на свою
                if end_file_name_from_path == file_name + '.lnk':
                    service.log_l_ap_text(f'#Создание ярлыка: Ищем ярлык [{end_file_name_from_path}] для добавления своей ссылки [{url}].')
                # if name in str(path):
                    browser_object = ''
                    print('Нашел ярлык для замены своей ссылки', str(path))
                    if 'Yandex' in browserWDir:
                        browser_object = str(browserWDir + r'\browser.exe')
                    elif 'Chromium' in browserWDir:
                        browser_object = str(browserWDir + r'\chrome.exe')
                    service.log_l_ap_text(f'#Создание ярлыка: Новый объект - [{browser_object}].')
                    shortcut.Targetpath = browser_object
                    args = [url, ]
                    shortcut.Arguments = " ".join(args)
                    shortcut.Save()
                    print(f'Изменил таргет {path}')
                    service.log_l_ap_text(f'#Создание ярлыка: Добавили ссылку в ярлык [{path}].')
                    break
                else:
                    continue
        return True

    if vars.browser_done:
        service.log_l_ap_next()
        service.log_l_ap_text(f'#Создание ярлыка: путь установки из - [{vars.true_install_path}]')
        if vars.browser_yandex_installed and vars.browser_gost_installed:
            service.log_l_ap_text('#Создание ярлыка: обнаружено два браузера')
            answer = askyesnocancel('Создание ярлыка для браузера',
                                    'Обнаружено 2 поддерживаемых браузера. Будет выполнено создание ярлыка для приоритетного браузера Chromium-Gost.\n\nПродолжить?\n\nДа - установка ярлыка для Chromium-Gost\nНет - установка ярлыка для Яндекс Браузера\nОтмена - отмена создания ярлыка')
            if answer == True:
                vars.browser_installed_name_true = vars.browser_gost_installed_name
                vars.browser_installed_path_true = vars.browser_gost_installed_path
            elif answer == False:
                vars.browser_installed_name_true = vars.browser_yandex_installed_name
                vars.browser_installed_path_true = vars.browser_yandex_installed_path
            else:
                mes.warning('Создание ярлыка дял браузера', 'Создание ярлыка было отменено пользователем!')
                vars.shortcut_done = False
                vars.shortcut_cheked = True
                service.log_l_ap_text(f'#Создание ярлыка: Создание ярлыка было отменено пользователем')
                return False
        elif vars.browser_gost_installed:
            vars.browser_installed_name_true = vars.browser_gost_installed_name
            vars.browser_installed_path_true = vars.browser_gost_installed_path
        elif vars.browser_yandex_installed:
            vars.browser_installed_name_true = vars.browser_yandex_installed_name
            vars.browser_installed_path_true = vars.browser_yandex_installed_path
        else:
            mes.warning('Создание ярлыка для браузера', 'Не обнаружен необходимый браузер!')
            self.shortcut_checkbox.configure(text='Не создан')
            self.shortcut_checkbox.deselect()
            vars.browser_done = False
            vars.shortcut_done = False
            vars.shortcut_cheked = True
            service.log_l_ap_text(f'#Создание ярлыка: Не обнаружен необходимый браузер!')
            return False

        service.log_l_ap_text(f'#Создание ярлыка: {vars.browser_installed_name_true}')
        service.log_l_ap_text(f'#Создание ярлыка: {vars.browser_installed_path_true}')

        if vars.browser_installed_path_true:
            if check_path(vars.browser_installed_path_true):

                answer = askyesnocancel('Создание ярлыка для браузера',
                                        'Создать ярлык для сайта "Закупки"?\n\nДа - создание ярлыка "Закупки".\nНет - Указание своей ссылки для ярлыка.\nОтмена - отмена создания ярлыка')
                if answer == True:
                    service.log_l_ap_text(f'#Создание ярлыка: Ярлык с ссылкой на Закупки')
                    to_ = os.path.join(vars.desktop, 'Закупки.lnk')
                    from_ = os.path.join(vars.true_install_path, 'Софт', 'Ярлыки')
                    if check_path(from_):
                        from_link_path = ''
                        if vars.browser_installed_name_true == 'Chromium-Gost':
                            from_link_path = os.path.join(from_, 'Закупки.lnk')
                        elif vars.browser_installed_name_true == 'Яндекс Браузер':
                            from_link_path = os.path.join(from_, 'Закупки .lnk')
                        service.log_l_ap_text(f'#Создание ярлыка: из {from_link_path}')
                        try:
                            if check_path(from_link_path):
                                shutil.copy2(from_link_path, to_)
                                print(f'Ярлык скопирован из {from_link_path} в {to_}!')
                                service.log_l_ap_text(f'#Создание ярлыка: Ярлык скопирован из {from_link_path} в {to_}!')
                            else:
                                mes.error('Создание ярлыка',
                                          f'Внимание!\n\nНеобходимый файл ярлыка поврежден! Проверьте путь установки!\n\n[{from_link_path}]')
                                vars.shortcut_done = False
                                service.log_l_ap_text(
                                    f'#Создание ярлыка: {vars.shortcut_done}, Внимание! Необходимый файл ярлыка поврежден! Проверьте путь установки! [{from_link_path}]')
                                return False
                        except:
                            mes.error('Создание ярлыка',
                                      f'Внимание!\n\nНе удалось создать ярлык для "{vars.browser_installed_name_true}"')
                            vars.shortcut_done = False
                            service.log_l_ap_text(f'#Создание ярлыка: {vars.shortcut_done}, Не удалось создать ярлык для "{vars.browser_installed_name_true}"')
                            return False

                        if repath_shortcut(vars.browser_installed_path_true, '', ''):
                            mes.info('Создание ярлыка',
                                     f'Успешно создан ярлык на рабочем столе для браузера "{vars.browser_installed_name_true}"')
                            service.log_l_ap_text(f'#Создание ярлыка: Успешно создан ярлык на рабочем столе для браузера "{vars.browser_installed_name_true}"')
                        else:
                            mes.error('Редактирование ярлыка',
                                      f'Не удалось изменить атрибуты ярлыка на рабочем столе для браузера "{vars.browser_installed_name_true}"')
                            service.log_l_ap_text(f'#Создание ярлыка: Не удалось изменить атрибуты ярлыка на рабочем столе для браузера "{vars.browser_installed_name_true}"')

                        vars.shortcut_done = True
                        vars.shortcut_cheked = True
                        service.log_l_ap_text(f'#Создание ярлыка: Успех! sh_D {vars.shortcut_done}, sh_Ch {vars.shortcut_cheked}')
                        return True
                    else:
                        mes.error('Проверка условий для создания ярлыка',
                                  f'Внимание!\n\nПуть до установочных файлов поврежден!\n\n[{from_}]')
                        vars.shortcut_done = False
                        service.log_l_ap_text(
                            f'#Создание ярлыка: {vars.shortcut_done}, Путь до установочных файлов поврежден!\n\n[{from_}]')
                        return False
                elif answer == False:
                    service.log_l_ap_text(f'#Создание ярлыка: Ярлык на собственную ссылку!')
                    new_url = ''
                    new_name = ''

                    from_ = os.path.join(vars.true_install_path, 'Софт', 'Ярлыки')
                    if check_path(from_):
                        USER_INP_URL = simpledialog.askstring(title="Создание ярлыка",
                                                          prompt=f"Укажите ссылку для ярлыка!")
                        if USER_INP_URL != '' and USER_INP_URL is not None:
                            new_url = USER_INP_URL.lower()
                            USER_INP_NAME = simpledialog.askstring(title="Создание ярлыка",
                                                                  prompt=f"Укажите название для ярлыка!")
                            if USER_INP_NAME != '' and USER_INP_NAME is not None:
                                new_name = USER_INP_NAME

                                to_ = os.path.join(vars.desktop, f'{new_name}.lnk')
                                from_link_path = ''
                                if vars.browser_installed_name_true == 'Chromium-Gost':
                                    from_link_path = os.path.join(from_, 'Закупки.lnk')
                                elif vars.browser_installed_name_true == 'Яндекс Браузер':
                                    from_link_path = os.path.join(from_, 'Закупки .lnk')
                                service.log_l_ap_text(f'#Создание ярлыка: to_ {to_}')
                                service.log_l_ap_text(f'#Создание ярлыка: from_link_path {from_link_path}')
                                try:
                                    if check_path(from_link_path):
                                        shutil.copy2(from_link_path, to_)
                                        print(f'Ярлык скопирован из {from_link_path} в {to_}!')
                                        service.log_l_ap_text(f'#Создание ярлыка: Ярлык скопирован из {from_link_path} в {to_}!')
                                    else:
                                        mes.error('Создание ярлыка',
                                                  f'Внимание!\n\nНеобходимый файл ярлыка поврежден! Проверьте путь установки!\n\n[{from_link_path}]')
                                        vars.shortcut_done = False
                                        service.log_l_ap_text(f'#Создание ярлыка: Необходимый файл ярлыка поврежден! Проверьте путь установки!\n\n[{from_link_path}]')
                                        return False
                                except:
                                    mes.error('Создание ярлыка',
                                              f'Внимание!\n\nНе удалось создать ярлык для "{vars.browser_installed_name_true}"')
                                    vars.shortcut_done = False
                                    service.log_l_ap_text(f'#Создание ярлыка: Не удалось создать ярлык для "{vars.browser_installed_name_true}"')
                                    return False
                            else:
                                mes.warning('Создание ярлыка для браузера',
                                            'Создание ярлыка было отменено пользователем!')
                                vars.shortcut_done = False
                                vars.shortcut_cheked = True
                                service.log_l_ap_text(f'#Создание ярлыка: Создание ярлыка было отменено пользователем!')
                                return False
                        else:
                            mes.warning('Создание ярлыка для браузера', 'Создание ярлыка было отменено пользователем!')
                            vars.shortcut_done = False
                            vars.shortcut_cheked = True
                            service.log_l_ap_text(f'#Создание ярлыка: Создание ярлыка было отменено пользователем!')
                            return False

                        if repath_shortcut(vars.browser_installed_path_true, new_url, new_name):
                            mes.info('Создание ярлыка',
                                     f'Успешно создан ярлык на рабочем столе для браузера "{vars.browser_installed_name_true}"')
                        else:
                            mes.error('Редактирование ярлыка',
                                      f'Не удалось изменить атрибуты ярлыка на рабочем столе для браузера "{vars.browser_installed_name_true}"')

                        vars.shortcut_done = True
                        vars.shortcut_cheked = True
                        service.log_l_ap_text(f'#Создание ярлыка: Ссылка - {new_url}')
                        service.log_l_ap_text(f'#Создание ярлыка: Имя - {new_name}')
                        return True
                    else:
                        mes.error('Проверка условий для создания ярлыка',
                                  f'Внимание!\n\nПуть до установочных файлов поврежден!\n\n[{from_}]')
                        vars.shortcut_done = False
                        service.log_l_ap_text(f'#Создание ярлыка: Путь до установочных файлов поврежден!\n\n[{from_}]')
                        return False
                else:
                    mes.warning('Создание ярлыка для браузера', 'Создание ярлыка было отменено пользователем!')
                    vars.shortcut_done = False
                    vars.shortcut_cheked = True
                    service.log_l_ap_text(f'#Создание ярлыка: Создание ярлыка было отменено пользователем!')
                    return False
            else:
                mes.error('Проверка условий для создания ярлыка',
                          f'Внимание!\n\nНе определен путь до установленного браузера!\n\n[{vars.browser_installed_path_true}]')
                vars.shortcut_done = False
                service.log_l_ap_text(f'#Создание ярлыка: Не определен путь до установленного браузера!\n\n[{vars.browser_installed_path_true}]')
                return False
        else:
            mes.error('Проверка условий для создания ярлыка',
                      'Внимание!\n\nНе найден путь до допустимого установленного браузера!')
            vars.shortcut_done = False
            service.log_l_ap_text(f'#Создание ярлыка: Не найден путь до допустимого установленного браузера!')
            return False
    else:
        mes.error('Проверка условий для создания ярлыка', 'Внимание!\n\nНе установлен необходимый браузер!')
        vars.shortcut_done = False
        vars.browser_done = False
        service.log_l_ap_text(f'#Создание ярлыка: Не установлен необходимый браузер!')
        return False


def install_certs(self):
    service.log_l_ap_next()
    if vars.crypto_done:
        if not vars.certs_done:
            service.log_l_ap_text(f'#Установка сертификатов: Установка через КриптоПро.')
            certmgr = Path(r'"C:\Program Files\Crypto Pro\CSP\certmgr.exe"')
            print(certmgr)
            if check_path(str(certmgr).replace('"', '')):
                args_root = ('mRoot',)
                cert_install = ''
                cert_error = False
                cert_error_access = False
                service.log_l_ap_text(f'#Установка сертификатов: Устанавливаем корневые - [{vars.need_install_root_certs}].')
                for cert in vars.need_install_root_certs:
                    for arg in args_root:
                        cert_install = rf'"{cert}"'

                        result = subprocess.run(f"{certmgr} -install -store {arg} -file {cert_install} -silent",
                                                encoding='windows-1251',
                                                stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

                        service.log_l_ap_text(
                            f'#Установка сертификатов: Сертификат - [{cert}]. Код - {result.returncode}. Ошибки - [{result.stderr}].')

                        if result.returncode == 5:
                            vars.certs_done = False
                            cert_error_access = True
                        elif result.returncode == 0:
                            vars.certs_done = True
                            cert_error = False
                            cert_error_access = False
                        else:
                            vars.certs_done = False
                            print(f'-----Ошибка установки-----')
                            print(result.returncode)
                            print(result.stderr)
                            print(result.stdout)
                            print(f'----- конец -----')
                            if result.stderr:
                                # mes.error('Установка сертификата',
                                #           f'Внимание!\nОшибка установки сертификата!\n\nСертификат: [{cert_install}]\n\nОшибка: [{result.stderr}]')
                                cert_error = True
                            else:
                                # mes.error('Установка сертификата',
                                #           f'Внимание!\nНеизвестная ошибка установки сертификата!\n\nСертификат: [{cert_install}]\nКод ошибки: [{result.returncode}]')
                                cert_error = True


                args_ca = ('mCA',)
                cert_install = ''
                service.log_l_ap_text(
                    f'#Установка сертификатов: Устанавливаем промежуточные - [{vars.need_install_ca_certs}].')
                for cert in vars.need_install_ca_certs:
                    for arg in args_ca:
                        cert_install = rf'"{cert}"'
                        result = subprocess.run(f"{certmgr} -install -store {arg} -file {cert_install} -silent",
                                                encoding='windows-1251',
                                                stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

                        service.log_l_ap_text(
                            f'#Установка сертификатов: Сертификат - [{cert}]. Код - {result.returncode}. Ошибки - [{result.stderr}].')

                        if result.returncode == 5:
                            vars.certs_done = False
                            cert_error_access = True
                            mes.error('Установка сертификата',
                                      f'Внимание!\n\nНе удалось получить доступ к хранилищу и установить сертификат \n\n[{cert_install}]\n\nЗапустите программу от имени Администратора для её корректной работы!')
                        elif result.returncode == 0:
                            vars.certs_done = True
                            cert_error = False
                            cert_error_access = False
                        else:
                            print(f'-----Ошибка установки-----')
                            print(result.returncode)
                            print(result.stderr)
                            print(result.stdout)
                            print(f'----- конец -----')
                            vars.certs_done = False
                            if result.stderr:
                                # mes.error('Установка сертификата',
                                #           f'Внимание!\nОшибка установки сертификата!\n\nСертификат: [{cert_install}]\n\nОшибка: [{result.stderr}]')
                                cert_error = True
                            else:
                                # mes.error('Установка сертификата',
                                #           f'Внимание!\nНеизвестная ошибка установки сертификата!\n\nСертификат: [{cert_install}]\nКод ошибки: [{result.returncode}]')
                                cert_error = True
                if cert_error_access:
                    service.log_l_ap_text(f'#Установка сертификатов: Обнаружены ошибки доступа Установка в локальные сертификаты, а не для всех.')
                    mes.warning('Установка сертификатов',
                              f'Внимание!\n\nНе удалось получить доступ к хранилищу и установить сертификаты!\n\nПробуем установку с правами для текущего пользователя!')

                    certmgr = Path(r'"C:\Program Files\Crypto Pro\CSP\certmgr.exe"')
                    print(certmgr)
                    err_temp = ''
                    if check_path(str(certmgr).replace('"', '')):
                        args_root = ('uRoot',)
                        cert_install = ''
                        cert_error = False
                        cert_error_access = False
                        service.log_l_ap_text(
                            f'#Установка сертификатов: Устанавливаем корневые - [{vars.need_install_root_certs}].')
                        for cert in vars.need_install_root_certs:
                            for arg in args_root:
                                cert_install = rf'"{cert}"'

                                result = subprocess.run(f"{certmgr} -install -store {arg} -file {cert_install} -silent",
                                                        encoding='windows-1251',
                                                        stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

                                service.log_l_ap_text(
                                    f'#Установка сертификатов: Сертификат - [{cert}]. Код - {result.returncode}. Ошибки - [{result.stderr}].')

                                if result.returncode == 5:
                                    vars.certs_done = False
                                    cert_error_access = True
                                elif result.returncode == 0:
                                    vars.certs_done = True
                                    cert_error = False
                                    cert_error_access = False
                                else:
                                    vars.certs_done = False
                                    print(f'-----Ошибка установки-----')
                                    print(result.returncode)
                                    print(result.stderr)
                                    print(result.stdout)
                                    print(f'----- конец -----')
                                    if result.stderr:
                                        err_temp = result.stderr
                                        # mes.error('Установка сертификата',
                                        #           f'Внимание!\nОшибка установки сертификата!\n\nСертификат: [{cert_install}]\n\nОшибка: [{result.stderr}]')
                                        cert_error = True
                                    else:
                                        # mes.error('Установка сертификата',
                                        #           f'Внимание!\nНеизвестная ошибка установки сертификата!\n\nСертификат: [{cert_install}]\nКод ошибки: [{result.returncode}]')
                                        cert_error = True

                        args_ca = ('uCA',)
                        cert_install = ''
                        service.log_l_ap_text(
                            f'#Установка сертификатов: Устанавливаем промежуточные - [{vars.need_install_ca_certs}].')
                        for cert in vars.need_install_ca_certs:
                            for arg in args_ca:
                                cert_install = rf'"{cert}"'
                                result = subprocess.run(f"{certmgr} -install -store {arg} -file {cert_install} -silent",
                                                        encoding='windows-1251',
                                                        stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

                                service.log_l_ap_text(
                                    f'#Установка сертификатов: Сертификат - [{cert}]. Код - {result.returncode}. Ошибки - [{result.stderr}].')

                                if result.returncode == 5:
                                    vars.certs_done = False
                                    cert_error_access = True
                                    # mes.error('Установка сертификата',
                                    #           f'Внимание!\n\nНе удалось получить доступ к хранилищу и установить сертификат \n\n[{cert_install}]\n\nЗапустите программу от имени Администратора для её корректной работы!')
                                elif result.returncode == 0:
                                    vars.certs_done = True
                                    cert_error = False
                                    cert_error_access = False
                                else:
                                    print(f'-----Ошибка установки-----')
                                    print(result.returncode)
                                    print(result.stderr)
                                    print(result.stdout)
                                    print(f'----- конец -----')
                                    vars.certs_done = False
                                    if result.stderr:
                                        err_temp = result.stderr
                                        # mes.error('Установка сертификата',
                                        #           f'Внимание!\nОшибка установки сертификата!\n\nСертификат: [{cert_install}]\n\nОшибка: [{result.stderr}]')
                                        cert_error = True
                                    else:
                                        # mes.error('Установка сертификата',
                                        #           f'Внимание!\nНеизвестная ошибка установки сертификата!\n\nСертификат: [{cert_install}]\nКод ошибки: [{result.returncode}]')
                                        cert_error = True

                        if cert_error_access:
                            mes.error('Установка сертификата',
                                      f'Внимание!\n\nНе удалось получить доступ к хранилищу и установить сертификаты!\n\nЗапустите программу от имени Администратора для её корректной работы!')
                            service.log_l_ap_text(
                                f'#Установка сертификатов: Не удалось получить доступ к хранилищу и установить сертификаты.')
                            return False
                        elif cert_error:
                            mes.error('Установка сертификатов', f'При установке сертификатов произошла ошибка!\n\n[{err_temp}]')
                            service.log_l_ap_text(f'#Установка сертификатов: При установке сертификатов произошли ошибки![{err_temp}].')
                            return False
                        else:
                            mes.info('Установка сертификатов', 'Сертификаты успешно установлены!')
                            vars.certs_done = True
                            vars.certs_cheked = True
                            service.log_l_ap_text(f'#Установка сертификатов: Сертификаты успешно установлены.')
                            return True
                    # return False
                elif cert_error:
                    mes.error('Установка сертификатов', 'При установке сертификатов произошла ошибка!')
                    service.log_l_ap_text(
                        f'#Установка сертификатов: При установке сертификатов произошла ошибка.')
                    return False
                else:
                    mes.info('Установка сертификатов', 'Сертификаты успешно установлены!')
                    vars.certs_done = True
                    vars.certs_cheked = True
                    service.log_l_ap_text(f'#Установка сертификатов: Сертификаты успешно установлены.')
                    return True
            else:
                mes.error('Подготовка к установке сертификатов', f'Не найден путь до менеджера сертификатов!\n\n[{certmgr}]')
                service.log_l_ap_text(f'#Установка сертификатов: Не найден путь до менеджера сертификатов!\n\n[{certmgr}].')
                vars.certs_done = False
        else:
            mes.error('Подготовка к установке сертификатов', 'Сертификаты уже установлены!')
            service.log_l_ap_text(f'#Установка сертификатов: Отмена - Сертификаты уже установлены.')
            vars.certs_done = True
    else:
        mes.warning('Подготовка к установке сертификатов',
                  'Не установлен КриптоПро CSP, пробуем установку средствами ОС!')

        service.log_l_ap_text(f'#Установка сертификатов: КриптоПро не обнаружен в системе - установка через cmd для ПК.')

        if not vars.certs_done:
            print('----------------------ставим через ос для локального пк-------------------')
            # certutil -user -addstore "Root" "C:\Certs\Сертификат.cer"
            # certutil -user -addstore "CA" "C:\Certs\Сертификат.cer"

            cert_install = ''
            cert_path_error = False
            cert_error = False
            arg = '"Root"'
            service.log_l_ap_text(
                f'#Установка сертификатов: Устанавливаем корневые - [{vars.need_install_root_certs}].')
            for cert in vars.need_install_root_certs:
                # print(cert)
                cert_install = rf'"{cert}"'

                result = subprocess.run(f"certutil -f -addstore {arg} {cert_install}",
                                        encoding='windows-1251',
                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                service.log_l_ap_text(
                    f'#Установка сертификатов: Сертификат - [{cert}]. Код - {result.returncode}. Ошибки - [{result.stderr}].')

                print(f'-----Результат-----')
                print(f'result.returncode: {result.returncode}')
                print(f'result.stderr: {result.stderr}')
                print(f'result.stdout: {result.stdout}')
                print(f'----- конец результата-----')
                if result.returncode == 2147942561:
                    cert_path_error = True
                    vars.certs_done = False
                    service.log_l_ap_text(
                        f'#Установка сертификатов: Ошибка пути для Сертификата - [{cert}]. Код - {result.returncode}. Ошибки - [{result.stderr}].')
                elif result.returncode == 0:
                    vars.certs_done = True
                    cert_error = False
                else:
                    vars.certs_done = False
                    print(f'-----Ошибка установки-----')
                    print(result.returncode)
                    print(result.stderr)
                    print(result.stdout)
                    print(f'----- конец -----')
                    if result.stderr:
                        # mes.error('Установка сертификата',
                        #           f'Внимание!\nОшибка установки сертификата!\n\nСертификат: [{cert_install}]\n\nОшибка: [{result.stderr}]')
                        cert_error = True
                    else:
                        # mes.error('Установка сертификата',
                        #           f'Внимание!\nНеизвестная ошибка установки сертификата!\n\nСертификат: [{cert_install}]\nКод ошибки: [{result.returncode}]')
                        cert_error = True

            arg = '"CA"'
            service.log_l_ap_text(
                f'#Установка сертификатов: Устанавливаем промежуточные - [{vars.need_install_ca_certs}].')
            for cert in vars.need_install_ca_certs:
                cert_install = rf'"{cert}"'

                result = subprocess.run(f"certutil -f -addstore {arg} {cert_install}",
                                        encoding='windows-1251',
                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                service.log_l_ap_text(
                    f'#Установка сертификатов: Сертификат - [{cert}]. Код - {result.returncode}. Ошибки - [{result.stderr}].')

                print(f'-----Результат-----')
                print(f'result.returncode: {result.returncode}')
                print(f'result.stderr: {result.stderr}')
                print(f'result.stdout: {result.stdout}')
                print(f'----- конец результата-----')
                if result.returncode == 2147942561:
                    cert_path_error = True
                    vars.certs_done = False
                    service.log_l_ap_text(
                        f'#Установка сертификатов: Ошибка пути для Сертификата - [{cert}]. Код - {result.returncode}. Ошибки - [{result.stderr}].')
                elif result.returncode == 0:
                    vars.certs_done = True
                    cert_error = False
                else:
                    vars.certs_done = False
                    print(f'-----Ошибка установки-----')
                    print(result.returncode)
                    print(result.stderr)
                    print(result.stdout)
                    print(f'----- конец -----')
                    if result.stderr:
                        # mes.error('Установка сертификата',
                        #           f'Внимание!\nОшибка установки сертификата!\n\nСертификат: [{cert_install}]\n\nОшибка: [{result.stderr}]')
                        cert_error = True
                    else:
                        # mes.error('Установка сертификата',
                        #           f'Внимание!\nНеизвестная ошибка установки сертификата!\n\nСертификат: [{cert_install}]\nКод ошибки: [{result.returncode}]')
                        cert_error = True

            if cert_error:
                service.log_l_ap_text(f'#Установка сертификатов: При установке сертификатов произошла ошибка. Пробуем установку в хранилище с правами доступа для данного пользователя.')
                mes.error('Установка сертификатов', 'При установке сертификатов произошла ошибка!\n\nПробуем установку в хранилище с правами доступа для данного пользователя!')

                print('----------------------ставим через ос для пользователя-------------------')
                # certutil -user -addstore "Root" "C:\Certs\Сертификат.cer"
                # certutil -user -addstore "CA" "C:\Certs\Сертификат.cer"

                err_temp = ''
                cert_install = ''
                cert_path_error = False
                cert_error = False
                arg = '"Root"'
                service.log_l_ap_text(
                    f'#Установка сертификатов: Устанавливаем корневые - [{vars.need_install_root_certs}].')
                for cert in vars.need_install_root_certs:
                    # print(cert)
                    cert_install = rf'"{cert}"'

                    result = subprocess.run(f"certutil -user -f -addstore {arg} {cert_install}",
                                            encoding='windows-1251',
                                            stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

                    service.log_l_ap_text(
                        f'#Установка сертификатов: Сертификат - [{cert}]. Код - {result.returncode}. Ошибки - [{result.stderr}].')

                    print(f'-----Результат-----')
                    print(f'result.returncode: {result.returncode}')
                    print(f'result.stderr: {result.stderr}')
                    print(f'result.stdout: {result.stdout}')
                    print(f'----- конец результата-----')
                    if result.returncode == 2147942561:
                        cert_path_error = True
                        vars.certs_done = False
                        service.log_l_ap_text(
                            f'#Установка сертификатов: Ошибка пути для Сертификата - [{cert}]. Код - {result.returncode}. Ошибки - [{result.stderr}].')
                    elif result.returncode == 0:
                        vars.certs_done = True
                        cert_error = False
                    else:
                        vars.certs_done = False
                        print(f'-----Ошибка установки-----')
                        print(result.returncode)
                        print(result.stderr)
                        print(result.stdout)
                        print(f'----- конец -----')
                        if result.stderr:
                            err_temp = result.stderr
                            # mes.error('Установка сертификата',
                            #           f'Внимание!\nОшибка установки сертификата!\n\nСертификат: [{cert_install}]\n\nОшибка: [{result.stderr}]')
                            cert_error = True
                        else:
                            # mes.error('Установка сертификата',
                            #           f'Внимание!\nНеизвестная ошибка установки сертификата!\n\nСертификат: [{cert_install}]\nКод ошибки: [{result.returncode}]')
                            cert_error = True

                arg = '"CA"'
                service.log_l_ap_text(
                    f'#Установка сертификатов: Устанавливаем промежуточные - [{vars.need_install_ca_certs}].')
                for cert in vars.need_install_ca_certs:
                    cert_install = rf'"{cert}"'

                    result = subprocess.run(f"certutil -user -f -addstore {arg} {cert_install}",
                                            encoding='windows-1251',
                                            stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

                    service.log_l_ap_text(
                        f'#Установка сертификатов: Сертификат - [{cert}]. Код - {result.returncode}. Ошибки - [{result.stderr}].')

                    print(f'-----Результат-----')
                    print(f'result.returncode: {result.returncode}')
                    print(f'result.stderr: {result.stderr}')
                    print(f'result.stdout: {result.stdout}')
                    print(f'----- конец результата-----')
                    if result.returncode == 2147942561:
                        cert_path_error = True
                        vars.certs_done = False
                        service.log_l_ap_text(
                            f'#Установка сертификатов: Ошибка пути для Сертификата - [{cert}]. Код - {result.returncode}. Ошибки - [{result.stderr}].')
                    elif result.returncode == 0:
                        vars.certs_done = True
                        cert_error = False
                    else:
                        vars.certs_done = False
                        print(f'-----Ошибка установки-----')
                        print(result.returncode)
                        print(result.stderr)
                        print(result.stdout)
                        print(f'----- конец -----')
                        if result.stderr:
                            err_temp = result.stderr
                            # mes.error('Установка сертификата',
                            #           f'Внимание!\nОшибка установки сертификата!\n\nСертификат: [{cert_install}]\n\nОшибка: [{result.stderr}]')
                            cert_error = True
                        else:
                            # mes.error('Установка сертификата',
                            #           f'Внимание!\nНеизвестная ошибка установки сертификата!\n\nСертификат: [{cert_install}]\nКод ошибки: [{result.returncode}]')
                            cert_error = True
                if cert_error:
                    mes.error('Установка сертификатов',
                              f'При установке сертификатов произошла ошибка!\n\n[{err_temp}]')
                    service.log_l_ap_text(
                        f'#Установка сертификатов: При установке сертификатов произошли ошибки![{err_temp}].')
                    return False
                elif cert_path_error:
                    mes.error('Установка сертификатов',
                              'При установке сертификатов произошла ошибка из-за некорректного пути!')
                    service.log_l_ap_text(
                        f'#Установка сертификатов: При установке сертификатов произошла ошибка из-за некорректного пути.')
                    return False
                else:
                    mes.info('Установка сертификатов', 'Сертификаты успешно установлены!')
                    vars.certs_done = True
                    vars.certs_cheked = True
                    service.log_l_ap_text(f'#Установка сертификатов: Сертификаты успешно установлены.')
                    return True
            elif cert_path_error:
                mes.error('Установка сертификатов', 'При установке сертификатов произошла ошибка из-за некорректного пути!')
                service.log_l_ap_text(f'#Установка сертификатов: При установке сертификатов произошла ошибка из-за некорректного пути.')
                return False
            else:
                mes.info('Установка сертификатов', 'Сертификаты успешно установлены!')
                vars.certs_done = True
                vars.certs_cheked = True
                service.log_l_ap_text(f'#Установка сертификатов: Сертификаты успешно установлены.')
                return True
        else:
            mes.error('Установка сертификатов', 'Сертификаты уже установлены!')
            vars.certs_done = True
            service.log_l_ap_text(f'#Установка сертификатов: Отмена - Сертификаты уже установлены.')
            return False
        # mes.error('Подготовка к установке сертификатов', 'Не установлен КриптоПро CSP, необходимый для централизованного управления сертификатами!')
        # vars.certs_done = False


def install_browser(self, app):
    if vars.browser_done and vars.browser_yandex_installed and not vars.browser_gost_installed or not vars.browser_done:
        # Подтверждаем путь установки
        path_confirm(self, app)
        service.log_l_ap_next()
        service.log_l_ap_text(f'#Установка браузера: путь установки из - [{vars.true_install_path}]')
        print(f'Тру путь: {vars.true_install_path}')
        # Путь установочного файла браузера
        path_browser_pack = ''
        # Путь папки с установочными файлами браузеров
        path_browser_folder = os.path.join(vars.true_install_path, 'Софт', 'Браузер')
        service.log_l_ap_text(f'#Установка браузера: Путь папки с установочными файлами браузеров - [{path_browser_folder}]')
        print(f'path_browser_folder: {path_browser_folder}')
        # Если путь до папки установки существует
        if check_path(path_browser_folder):
            # Переменная выбора браузера
            need_browser = ''
            if not vars.browser_done:
                answer = askyesnocancel('Установка необходимого браузера',
                                        'Будет выполнена установка приоритетного браузера Chromium-Gost.\n\nПродолжить?\n\nДа - установить Chromium Gost\nНет - установить Яндекс Браузера\nОтмена - отмена установки браузера')
                if answer == True:
                    need_browser = 'G'
                elif answer == False:
                    need_browser = 'Y'
                else:
                    mes.warning('Установка браузера', 'Установка браузера была отменена пользователем!')
                    self.browser_checkbox.configure(text='Установка отменена')
                    self.browser_checkbox.deselect()
                    vars.browser_done = False
                    vars.browser_cheked = True
                    service.log_l_ap_text(f'#Установка браузера: Установка браузера была отменена пользователем. B_D - {vars.browser_done}, B_Ch - {vars.browser_cheked}.')
                    return False
                service.log_l_ap_text(f'#Установка браузера: Браузеры не обнаружены, для установки выбран - [{need_browser}].')
            elif vars.browser_yandex_installed and not vars.browser_gost_installed:
                answer = askyesno('Установка необходимого браузера',
                                        'Обнаружен установленный Яндекс Браузер. Желаете установить приоритетный браузер Chromium-Gost?\n\nДа - установить Chromium-Gost\nНет - отмена установки браузера.')
                print(answer)
                if answer == True:
                    need_browser = 'G'
                    service.log_l_ap_text(f'#Установка браузера: Обнаружен Яндекс. Выбрана установка G.')
                else:
                    mes.warning('Установка браузера', 'Установка браузера была отменена пользователем!')
                    self.browser_checkbox.configure(text='Установка отменена')
                    self.browser_checkbox.deselect()
                    vars.browser_done = True
                    vars.browser_cheked = True
                    service.log_l_ap_text(f'#Установка браузера: Обнаружен Яндекс. Установка браузера была отменена пользователем. B_D - {vars.browser_done}, B_Ch - {vars.browser_cheked}.')
                    return False
            if check_funcs.check_os_type != False:
                # Разрядность системы
                system_os_x = check_funcs.check_os_type()[0]
                service.log_l_ap_text(f'#Установка браузера: Разрядность системы - {system_os_x}.')
                # Версия Windows
                system_os = check_funcs.check_os_type()[1][0:check_funcs.check_os_type()[1].index(',')].replace("'", '').replace("(", '')
                service.log_l_ap_text(f'#Установка браузера: Версия Windows - {system_os}.')
                # Все имена установочных файлов в папке
                list_files = os.listdir(path_browser_folder)
                service.log_l_ap_text(f'#Установка браузера: Все имена установочных файлов в папке установки - {list_files}.')
                for file in list_files:
                    # Если нужен Хромиум-Гост
                    if need_browser == 'G':
                        if system_os == '10' or system_os == '11':
                            # Ищем 111 версию установщика и заисываем путь к нему
                            if system_os_x.lower() in file and '-111' in file:
                                path_browser_pack = os.path.join(path_browser_folder, file)
                                break
                            else:
                                continue
                        elif system_os == '7' or '8' in system_os:
                            # Ищем 109 версию установщика и заисываем путь к нему
                            if system_os_x.lower() in file and '-109' in file:
                                path_browser_pack = os.path.join(path_browser_folder, file)
                                break
                            else:
                                continue
                    # Если нужен Яндекс Браузер
                    elif need_browser == 'Y':
                        if 'Yandex.exe' in file:
                        # if 'YandexBrowser-' + str(system_type).lower() in file:
                            path_browser_pack = os.path.join(path_browser_folder, file)
                            break
                        else:
                            continue
                service.log_l_ap_text(f'#Установка браузера: Выбран установочник - {path_browser_pack} из {path_browser_folder}.')
                print(f'path_browser_folder: {path_browser_folder}')
                print(f'path_browser_pack: {path_browser_pack}')
                print(f'check_path(path_browser_pack): {check_path(path_browser_pack)}')
                if path_browser_pack != '' and check_path(path_browser_pack):
                    try:
                        if need_browser == 'G':
                            service.log_l_ap_text(f'#Установка браузера: Запуск установки - G')
                            result = subprocess.run(
                                fr'"{path_browser_pack}" --install',
                                encoding='windows-1251', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                            service.log_l_ap_text(f'#Установка браузера: Результат установки (код) - {result.returncode}. Ошибки - [{result.stderr}]')
                            if result.returncode == 0:
                                mes.info('Установка браузера Chromium-Gost', 'Браузер успешно установлен на ваш АРМ!')
                                vars.browser_done = True
                                return True
                            else:
                                mes.error('Установка браузера Chromium-Gost',
                                          f'Внимание!\n\nПри установке обнаружена ошибка:\n{result.stderr}')
                                print(f'-----Ошибка установки-----')
                                print(result.returncode)
                                print(result.stderr)
                                print(result.stdout)
                                print(f'----- конец -----')
                                vars.browser_done = False
                                return False

                        if need_browser == 'Y':
                            service.log_l_ap_text(f'#Установка браузера: Запуск установки - Y')
                            result = subprocess.run(
                                fr'"{path_browser_pack}" --install',
                                encoding='windows-1251', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                            service.log_l_ap_text(
                                f'#Установка браузера: Результат установки (код) - {result.returncode}. Ошибки - [{result.stderr}]')

                            if result.returncode == 0 or result.returncode == 400:
                                mes.info('Установка Яндекс Браузера', 'Браузер успешно установлен на ваш АРМ!')
                                vars.browser_done = True
                                return True
                            elif result.returncode == 500:
                                mes.error('Установка Яндекс Браузера',
                                          f'Установка была отменена пользователем!')
                                vars.browser_done = False
                                service.log_l_ap_text(f'#Установка браузера: Код {result.returncode} - Установка была отменена пользователем.')
                                return False
                            else:
                                mes.error('Установка Яндекс Браузера',
                                          f'Внимание!\n\nПри установке обнаружена ошибка:\n{result.stderr}')
                                print(f'-----Ошибка установки-----')
                                print(result.returncode)
                                print(result.stderr)
                                print(result.stdout)
                                print(f'----- конец -----')
                                vars.browser_done = False
                                return False
                    except Exception as e:
                        mes.error('Установка браузера',
                                  f'Внимание!\n\nОшибка установки!\n\nЗапустите программу с правами администратора и повторите попытку!\n\nИсключение: [{e}]')
                        vars.browser_done = False
                        service.log_l_ap_text(f'#Установка браузера: Исключение запуска процесса установки - [{e}]')
                        return False
                else:
                    mes.error('Установка браузера',
                              f'Внимание!\n\nПри установке определен некорректный путь [{path_browser_pack}]')
                    vars.browser_done = False
                    service.log_l_ap_text(
                        f'#Установка браузера: При установке определен некорректный путь [{path_browser_pack}]')
                    return False
            else:
                mes.error('Установка браузера', f'Неподдерживаемый тип системы {check_funcs.check_os_type}')
                vars.browser_done = False
                service.log_l_ap_text(f'#Установка браузера: Неподдерживаемый тип системы {check_funcs.check_os_type}')
                return False
        else:
            mes.error('Установка браузера', f'Некорректный путь: [{path_browser_folder}]')
            vars.browser_done = False
            service.log_l_ap_text(f'#Установка браузера: Некорректный путь: [{path_browser_folder}]')
            return False
    else:
        mes.error('Установка браузера', f'Требуемый браузер уже установлен!')
        vars.browser_done = True
        service.log_l_ap_text(f'#Установка браузера: Требуемый браузер уже установлен!')
        return False


def install_crypto_csp(self, app):
    if not vars.crypto_done:
        path_confirm(self, app)

        service.log_l_ap_next()
        service.log_l_ap_text(f'#Установка КриптоПро CSP: Путь установки - {vars.true_install_path}.')

        path = os.path.join(vars.true_install_path, 'Софт', 'КриптоПро', 'CSPSetup.exe')
        service.log_l_ap_text(f'#Установка КриптоПро CSP: Установка - {path}.')
        if check_path(path):
            try:
                result = subprocess.run(
                    fr'"{path}" -kc kc2 -lang ru -args "/l*v! \"{vars.usr_docs}\csp.log\"" -silent -noreboot -nodlg -reinstall',
                    encoding='windows-1251',
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                service.log_l_ap_text(
                    f'#Установка КриптоПро CSP: Результат установки (код) - {result.returncode}. Ошибки - [{result.stderr}].')

                if result.returncode == 0:
                    mes.info('Установка КриптоПро CSP', 'Криптопровайдер успешно установлен на ваш АРМ!')
                    vars.crypto_done = True
                    return True
                else:
                    mes.error('Установка КриптоПро CSP',
                              f'Внимание!\n\nПри установке обнаружена ошибка:\n{result.stderr}')
                    print(f'-----Ошибка установки-----')
                    print(result.returncode)
                    print(result.stderr)
                    print(result.stdout)
                    print(f'----- конец -----')
                    vars.crypto_done = False
                    return False
            except Exception as e:
                mes.error('Установка КриптоПро CSP', f'Внимание!\n\nПри установке определен некорректный путь [{path}]\n\nИсключение установки: [{e}].')
                vars.crypto_done = False
                service.log_l_ap_text(f'#Установка КриптоПро CSP: При установке определен некорректный путь [{path}]. Исключение установки - [{e}].')
                return False
        else:
            mes.error('Установка КриптоПро CSP', f'Внимание!\n\nПри установке определен некорректный путь [{path}]')
            vars.crypto_done = False
            service.log_l_ap_text(f'#Установка КриптоПро CSP: При установке определен некорректный путь [{path}].')
            return False
    else:
        mes.error('Установка КриптоПро CSP', f'Внимание!\n\nКриптоПро CSP уже установлен')
        vars.crypto_done = True
        service.log_l_ap_text(f'#Установка КриптоПро CSP: Отмена - КриптоПро CSP уже установлен на АРМ.')
        return False


def install_crypto_plugin(self, app):
    if vars.browser_done or vars.browser_firefox_installed:
        if not vars.plugin_done:
            # Если уже установлен криптопро цсп
            if vars.crypto_done:
                path_confirm(self, app)
                service.log_l_ap_text(f'#Установка КриптоПро cadesplugin: Путь установки - {vars.true_install_path}.')
                path = os.path.join(vars.true_install_path, 'Софт', 'КриптоПро', 'cadesplugin.exe')
                service.log_l_ap_next()
                service.log_l_ap_text(f'#Установка КриптоПро cadesplugin: Установка - {path}.')
                if check_path(path):
                    try:
                        result = subprocess.run(
                            fr'"{path}" -reinstall -silent -norestart -cadesargs "/quiet"',
                            encoding='windows-1251',
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                        service.log_l_ap_text(
                            f'#Установка КриптоПро cadesplugin: Результат установки (код) - {result.returncode}. Ошибки - [{result.stderr}].')

                        if result.returncode == 0:
                            mes.info('Установка КриптоПро Cades Plugin', 'Плагин успешно установлен на ваш АРМ!')
                            vars.plugin_done = True
                            return True
                        else:
                            mes.error('Установка КриптоПро Cades Plugin',
                                                    f'Внимание!\n\nПри установке обнаружена ошибка:\n{result.stderr}')
                            print(f'-----Ошибка установки-----')
                            print(result.returncode)
                            print(result.stderr)
                            print(result.stdout)
                            print(f'----- конец -----')
                            vars.plugin_done = False
                            return False
                    except Exception as e:
                        mes.error('Установка КриптоПро Cades Plugin',
                                  f'Внимание!\n\nОшибка установки!\n\nЗапустите программу с правами администратора и повторите попытку!\n\nИсключение установки - [{e}].')
                        vars.plugin_done = False
                        service.log_l_ap_text(f'#Установка КриптоПро cadesplugin: Исключение установки - [{e}].')
                        return False
                else:
                    mes.error('Установка КриптоПро Cades Plugin',
                              f'Внимание!\n\nПри установке определен некорректный путь [{path}]')
                    vars.plugin_done = False
                    service.log_l_ap_text(f'#Установка КриптоПро cadesplugin: При установке определен некорректный путь [{path}].')
                    return False
            else:
                mes.error('Подготовка к установке КриптоПро Cades Plugin',
                          'Внимание!\n\nНе обнаружен установленный КриптоПро CSP!')
                vars.plugin_done = False
                service.log_l_ap_text(f'#Установка КриптоПро cadesplugin: Не обнаружен установленный КриптоПро CSP.')
                return False
        else:
            mes.error('Установка КриптоПро Cades Plugin', f'Внимание!\n\nКриптоПро Cades Plugin уже установлен')
            vars.plugin_done = True
            service.log_l_ap_text(f'#Установка КриптоПро cadesplugin: Отмена - КриптоПро Cades Plugin уже установлен.')
            return False
    else:
        mes.error('Установка КриптоПро Cades Plugin', f'Внимание!\n\nВ системе не обнаружен подходящий браузер!')
        service.log_l_ap_text(f'#Установка КриптоПро cadesplugin: В системе не обнаружен подходящий браузер.')
        vars.plugin_done = False
        return False
