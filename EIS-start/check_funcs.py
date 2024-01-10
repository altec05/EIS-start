import service
import variables as vars
import os
import messages as mes
import platform
import winapps
import fsb795
from path_funcs import path_confirm, get_temp_folderpath, check_path


def check_mozilla():
    flag = False
    for app in winapps.search_installed('Mozilla Firefox'):
        flag = True
        print(flag)
        return True
    flag = False
    print(flag)
    return False


# Проверка наличия требуемых компонентов
def start_all(self, app):
    def get_count_certs():
        stores = list()
        if vars.temp_path != '':
            stores = [os.path.join(vars.temp_path, 'Сертификаты', 'Корневые'),
                      os.path.join(vars.temp_path, 'Сертификаты', 'Промежуточные')]
        else:
            stores = [os.path.join(vars.true_install_path, 'Сертификаты', 'Корневые'),
                      os.path.join(vars.true_install_path, 'Сертификаты', 'Промежуточные')]
        certs_list = list()
        for store in stores:
            try:
                certs_list += os.listdir(store)
            except:
                if not check_path(store):
                    mes.error('Определение сертификатов',
                              f'Внимание!\n\nПуть до хранилища сертификатов поврежден!\nИспользуется: {store}')
                    return False
        counter = 0
        for cert in certs_list:
            counter += 1
        return counter

    vars.clear_vars()
    while not vars.thread_stop:
        self.all_progress.set(0)
        self.all_progress.configure(determinate_speed=7)
        vars.clear_vars()
        print(vars.path_confirmed)
        # Подтверждаем путь установки
        # if not vars.path_confirmed:
        #     if not path_confirm(self, app):
        #         vars.thread_stop = True
        #         return False

        if vars.path_confirmed:
            self.all_progress.step()
            if check_path(vars.true_install_path):
                connection_status = check_connection(self, False)
                self.all_progress.step()
                service.log_l_ap(f'Источник установки: {vars.true_install_path}\nСоединение: {connection_status}')
                # Проверка наличия КриптоПро CSP
                if check_install('КриптоПро CSP'):
                    self.crypto_checkbox.configure(text='Установлен')
                    self.crypto_checkbox.configure(fg_color='green')
                    self.crypto_checkbox.select()
                    vars.crypto_done = True
                    vars.crypto_cheked = True
                    self.all_progress.step()
                else:
                    self.crypto_checkbox.configure(text='Не установлен')
                    self.crypto_checkbox.deselect()
                    vars.crypto_done = False
                    vars.crypto_cheked = True
                    self.all_progress.step()
                service.log_l_ap(f'КриптоПро CSP: У - {vars.crypto_done}, П - {vars.crypto_cheked}')
                # Проверка наличия КриптоПро ЭЦП Browser plug-in
                if check_install('КриптоПро ЭЦП Browser plug-in'):
                    self.plugin_checkbox.configure(text='Установлен')
                    self.plugin_checkbox.configure(fg_color='green')
                    self.plugin_checkbox.select()
                    vars.plugin_done = True
                    vars.plugin_cheked = True
                    self.all_progress.step()
                else:
                    self.plugin_checkbox.configure(text='Не установлен')
                    self.plugin_checkbox.deselect()
                    vars.plugin_done = False
                    vars.plugin_cheked = True
                    self.all_progress.step()
                service.log_l_ap(f'КриптоПро ЭЦП Browser plug-in: У - {vars.plugin_done}, П - {vars.plugin_cheked}')
                # Проверка наличия Гост Хромиума и Яндекс Браузера
                if check_browser(self):
                    if vars.browser_gost_installed and vars.browser_yandex_installed:
                        self.browser_checkbox.configure(text=f'Установлены: {vars.browser_gost_installed_name} и {vars.browser_yandex_installed_name}')
                        vars.browser_done = True
                    elif not vars.browser_gost_installed and vars.browser_yandex_installed:
                        self.browser_checkbox.configure(
                            text=f'Установлен {vars.browser_yandex_installed_name}')
                        vars.browser_done = True
                    elif not vars.browser_yandex_installed and vars.browser_gost_installed:
                        self.browser_checkbox.configure(
                            text=f'Установлен {vars.browser_gost_installed_name}')
                        vars.browser_done = True
                    self.browser_checkbox.configure(fg_color='green')
                    self.browser_checkbox.select()
                    vars.browser_cheked = True
                    vars.browser_done = True
                    self.all_progress.step()
                else:
                    if check_mozilla():
                        mes.warning('Проверка браузера', 'На АРМ онаружен Mozilla Firefox, но не обнаружены требуемые браузеры!')
                        vars.browser_firefox_installed = True
                    else:
                        vars.browser_firefox_installed = False
                    self.browser_checkbox.configure(text='Не установлен')
                    self.browser_checkbox.deselect()
                    vars.browser_cheked = True
                    vars.browser_done = False
                    self.all_progress.step()
                service.log_l_ap(
                    f'Браузер: У - {vars.browser_done}, П - {vars.browser_cheked}\nЯндекс - {vars.browser_yandex_installed}, путь - {vars.browser_yandex_installed_path}\nГост - {vars.browser_gost_installed}, путь - {vars.browser_gost_installed_path}\nМозилла - {vars.browser_firefox_installed}')
                # Определение длины прогресса сертификатов
                cert_pr_max = int()
                certs_pr_step = int()
                try:
                    cert_pr_max = get_count_certs()
                    certs_pr_step = int(100 / cert_pr_max)
                except:
                    if not get_count_certs():
                        mes.warning('Определение сертификатов',
                                  f'Внимание!\n\nПри обработке сертификатов была обнаружена ошибка.\n\nУкажите локальный корректный путь до расположения, где хранится папка "Сертификаты"!')
                        vars.temp_path = ''
                        if get_temp_folderpath():
                            try:
                                cert_pr_max = get_count_certs()
                                certs_pr_step = int(100 / cert_pr_max)
                            except:
                                mes.error('Указание временного пути до сертификатов',
                                          f'Внимание!\n\nНе удалось указать временный путь!\nПерезапустите программу.')
                                app.on_close()
                        else:
                            mes.error('Указание временного пути до сертификатов',
                                      f'Внимание!\n\nНе удалось указать временный путь!\nПерезапустите программу.')
                            app.on_close()

                self.certs_progress.configure(determinate_speed=certs_pr_step)
                self.certs_progress.set(0)
                # Проверка наличия требуемых сертификатов
                if check_certs(self):
                    self.certs_checkbox.configure(text=f'Установлены')
                    self.certs_checkbox.configure(fg_color='green')
                    self.certs_checkbox.select()
                    vars.certs_cheked = True
                    vars.certs_done = True
                    self.all_progress.step()
                else:
                    self.certs_checkbox.configure(text='Не установлены')
                    self.certs_checkbox.deselect()
                    vars.certs_cheked = True
                    vars.certs_done = False
                    self.all_progress.step()
                service.log_l_ap(f'Сертификаты: Уст-ы - {vars.certs_done}\nНе Уст-ы корневые - {vars.need_install_root_certs}\nНе Уст-ы промежуточные - {vars.need_install_ca_certs}')
                # Проверка наличия Ярлыка на рабочем столе
                short_names = check_shortcut(self)
                if short_names != '':
                    self.shortcut_checkbox.configure(text=f'Создан для {short_names}')
                    self.shortcut_checkbox.configure(fg_color='green')
                    self.shortcut_checkbox.select()
                    vars.shortcut_done = True
                    vars.shortcut_cheked = True
                    self.all_progress.step()
                else:
                    print(check_shortcut(self))
                    self.shortcut_checkbox.configure(text='Не создан')
                    self.shortcut_checkbox.deselect()
                    vars.shortcut_done = False
                    vars.shortcut_cheked = True
                    self.all_progress.step()
                service.log_l_ap(
                    f'Ярлык: У - {vars.shortcut_done} для {short_names}\nП - {vars.shortcut_cheked}')
                self.certs_progress.set(1)
                self.all_progress.configure(progress_color='#03DAC6')
                self.all_progress.set(1)
                vars.thread_stop = True
            else:
                self.all_progress.step()
                mes.error('Ошибка пути установки',
                          f'Внимание!\nПуть установки не существует!\n\nИспользуется путь: {vars.true_install_path}')
                vars.thread_stop = True
                service.log_l_ap(f'Начало проверки: Ошибка [Путь установки не существует!\n\nИспользуется путь: {vars.true_install_path}]')
        else:
            mes.error('Проверка подтверждения пути', 'Внимание!\n\nНе потвердился путь установки! Обратитесь к специалисту.')
            vars.thread_stop = True
            service.log_l_ap(f'Начало проверки: Ошибка [путь не подтвержден!]')
    vars.thread_stop = True


def check_os_type():
    print(platform.machine())
    if platform.machine().lower() == 'amd64' or platform.machine().lower() == 'x64' or '386' in platform.machine().lower():
        return [str(platform.machine()), str(platform.win32_ver())]
    else:
        return False


# Проверяем ping до сервера и возвращаем T/F
def check_connection(self, up):
    import platform  # For getting the operating system name
    import subprocess  # For executing a shell command

    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    host = '192.168.15.4'
    host_first = 'ya.ru'

    # Building the command. Ex: "ping -c 1 google.com"
    command_first = ['ping', param, '1', host_first]
    command = ['ping', param, '1', host]

    if subprocess.call(command_first) == 0:
        if subprocess.call(command_first) == 0:
            if up:
                self.all_progress.step()
                self.connect_checkbox.select()
                self.connect_checkbox.configure(fg_color='green')
                self.connect_checkbox.configure(text='Соединение установлено')
                self.all_progress.step()
                return True
            else:
                self.connect_checkbox.select()
                self.connect_checkbox.configure(fg_color='green')
                self.connect_checkbox.configure(text='Соединение установлено')
                return True
        else:
            if up:
                self.all_progress.step()
                self.connect_checkbox.deselect()
                self.connect_checkbox.configure(text='Соединение отсутствует')
                self.all_progress.step()
            else:
                self.connect_checkbox.deselect()
                self.connect_checkbox.configure(text='Соединение отсутствует')
            return False
    else:
        if up:
            self.all_progress.step()
            self.connect_checkbox.deselect()
            self.connect_checkbox.configure(text='Соединение отсутствует')
            self.all_progress.step()
        else:
            self.connect_checkbox.deselect()
            self.connect_checkbox.configure(text='Соединение отсутствует')
        return False


# Проверка установленного на ПК приложения по имени
def check_install(name):
    for app in winapps.list_installed():
        if app.name == name:
            return True
        else:
            continue


# Проверка установки браузеров
def check_browser(self):
    def check_chromium():
        if check_path(os.path.join(vars.appdata_path, 'Chromium', 'Application', 'chrome.exe')):
            vars.browser_gost_installed = True
            vars.browser_gost_installed_name = 'Chromium-Gost'
            vars.browser_gost_installed_path = f"{os.path.join(vars.appdata_path, 'Chromium', 'Application')}"
        elif check_path(os.path.join(vars.appdata_roaming_path, 'Chromium', 'Application', 'chrome.exe')):
            vars.browser_gost_installed = True
            vars.browser_gost_installed_name = 'Chromium-Gost'
            vars.browser_gost_installed_path = f"{os.path.join(vars.appdata_roaming_path, 'Chromium', 'Application')}"
        else:
            vars.browser_gost_installed = False
            vars.browser_gost_installed_name = ''
            vars.browser_gost_installed_path = ''

    def check_yandex():
        if check_path(r'C:\Program Files (x86)\Yandex\YandexBrowser\Application\browser.exe'):
            vars.browser_yandex_installed = True
            vars.browser_yandex_installed_name = 'Яндекс Браузер'
            path = r'C:\Program Files (x86)\Yandex\YandexBrowser'
            vars.browser_yandex_installed_path = f"{os.path.join(path)}"

        elif check_path(r'C:\Program Files\Yandex\YandexBrowser\Application\browser.exe'):
            vars.browser_yandex_installed = True
            vars.browser_yandex_installed_name = 'Яндекс Браузер'
            path = r'C:\Program Files\Yandex\YandexBrowser'
            vars.browser_yandex_installed_path = f"{os.path.join(path)}"

        elif check_path(r'D:\Program Files (x86)\Yandex\YandexBrowser\Application\browser.exe'):
            vars.browser_yandex_installed = True
            vars.browser_yandex_installed_name = 'Яндекс Браузер'
            path = r'D:\Program Files (x86)\Yandex\YandexBrowser'
            vars.browser_yandex_installed_path = f"{os.path.join(path)}"

        elif check_path(r'D:\Program Files\Yandex\YandexBrowser\Application\browser.exe'):
            vars.browser_yandex_installed = True
            vars.browser_yandex_installed_name = 'Яндекс Браузер'
            path = r'D:\Program Files\Yandex\YandexBrowser'
            vars.browser_yandex_installed_path = f"{os.path.join(path)}"

        elif check_path(os.path.join(vars.appdata_path, 'Yandex', 'YandexBrowser', 'Application', 'browser.exe')):
            vars.browser_yandex_installed = True
            vars.browser_yandex_installed_name = 'Яндекс Браузер'
            path = os.path.join(vars.appdata_path, 'Yandex', 'YandexBrowser', 'Application')
            vars.browser_yandex_installed_path = f"{os.path.join(path)}"

        elif check_path(os.path.join(vars.appdata_roaming_path, 'Yandex', 'YandexBrowser', 'Application', 'browser.exe')):
            vars.browser_yandex_installed = True
            vars.browser_yandex_installed_name = 'Яндекс Браузер'
            path = os.path.join(vars.appdata_roaming_path, 'Yandex', 'YandexBrowser', 'Application')
            vars.browser_yandex_installed_path = f"{os.path.join(path)}"

        else:
            vars.browser_yandex_installed = False
            vars.browser_yandex_installed_name = ''
            vars.browser_yandex_installed_path = ''

    # Проверяем наличие браузера Chromium-Gost
    check_chromium()

    # Проверяем наличие Яндекс Браузера
    check_yandex()

    if vars.browser_yandex_installed or vars.browser_gost_installed:
        return True
    else:
        return False


# Проверка установки сертификатов
def check_certs(self):
    import wincertstore
    import base64
    import ssl
    from cryptography import x509
    from cryptography.hazmat.backends import default_backend

    def get_old_certs():
        from datetime import date
        counter = 0
        send_data = list()
        temp_data = list()
        for storename in ("MY", ):
            with wincertstore.CertSystemStore(storename) as store:
                # for cert in store.itercerts(usage=wincertstore.SERVER_AUTH):
                for cert in store.itercerts(usage=None):

                    pem = cert.get_pem()
                    encodedDer = ''.join(pem.split("\n")[1:-2])

                    cert_bytes = base64.b64decode(encodedDer)
                    cert_pem = ssl.DER_cert_to_PEM_cert(cert_bytes)
                    cert_details = x509.load_pem_x509_certificate(cert_pem.encode('utf-8'),
                                                                  default_backend())

                    cert_after = cert_details.not_valid_after.date()

                    if cert_after < date.today():
                        temp_data.append((counter, cert.get_name(), cert_after))
                        counter += 1
                        print(counter)
        send_data.append((counter, temp_data))
        return send_data


    def get_cert_from_folder(node):
        new_certs_path = ''
        certs_list = list()
        if node == 'root':
            if vars.temp_path != '':
                new_certs_path = os.path.join(vars.temp_path, 'Сертификаты', 'Корневые')
            else:
                new_certs_path = os.path.join(vars.true_install_path, 'Сертификаты', 'Корневые')
        elif node == 'ca':
            if vars.temp_path != '':
                new_certs_path = os.path.join(vars.temp_path, 'Сертификаты', 'Промежуточные')
            else:
                new_certs_path = os.path.join(vars.true_install_path, 'Сертификаты', 'Промежуточные')
        else:
            mes.error('Обработка сертификатов', f'Внимание!\n\nУказан некорректный узел! {node}')
            return False
        try:
            certs_list = os.listdir(new_certs_path)
        except:
            return False

        for cert_filename in certs_list:
            certificate_path = os.path.join(new_certs_path, cert_filename)
            if check_path(certificate_path):
                if not certificate_path.lower().endswith('.cer') and not certificate_path.lower().endswith('.crt'):
                    continue
                else:
                    cert = fsb795.Certificate(certificate_path)
                    send_data = list()
                    conversion_table = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4',
                                        5: '5', 6: '6', 7: '7',
                                        8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C',
                                        13: 'D', 14: 'E', 15: 'F'}

                    def decimal_to_hexadecimal(decimal):
                        hexadecimal = ''
                        while (decimal > 0):
                            remainder = decimal % 16
                            hexadecimal = conversion_table[remainder] + hexadecimal
                            decimal = decimal // 16
                        return hexadecimal

                    hex_output = decimal_to_hexadecimal(cert.serialNumber())
                    sub, vlad_sub = cert.subjectCert()
                    for key in sub.keys():
                        if key == 'CN':
                            send_data.append((str(sub[key]), certificate_path, hex_output))
                        else:
                            continue
                    if node == 'root':
                        vars.certs_root_to_check.append(send_data)
                    elif node == 'ca':
                        vars.certs_ca_to_check.append(send_data)
                    else:
                        mes.error('Обработка сертификатов', f'Внимание!\n\nУказан некорректный узел! {node}')
                        return False
            else:
                continue
        vars.temp_path = ''
        return True

    def check_new_certs(node):
        store = list()
        if node in 'root':
            store = vars.certs_root_to_check
        elif node in 'ca':
            store = vars.certs_ca_to_check
        else:
            mes.error('Проверка новых сертификатов', f'Внимание!\n\nУказан некорректный узел! {node}')
            return False

        for cert_row in store:
            for cert_check in cert_row:
                need_install = 1
                finded = False

                certName = cert_check[0]
                certPath = cert_check[1]
                certSerialNumber = cert_check[2]

                if node == 'root':
                    for storename in ("ROOT", "MY"):
                        with wincertstore.CertSystemStore(storename) as store:
                            for cert in store.itercerts(usage=None):
                            # for cert in store.itercerts(usage=wincertstore.SERVER_AUTH):
                                pem = cert.get_pem()
                                encodedDer = ''.join(pem.split("\n")[1:-2])

                                cert_bytes = base64.b64decode(encodedDer)
                                cert_pem = ssl.DER_cert_to_PEM_cert(cert_bytes)
                                cert_details = x509.load_pem_x509_certificate(cert_pem.encode('utf-8'),
                                                                              default_backend())
                                serialnumber = hex(cert_details.serial_number).replace("0x", "")

                                if cert.get_name() == certName and certSerialNumber == serialnumber.upper():
                                    need_install = 0
                                    finded = True
                                    break
                                else:
                                    continue
                elif node == 'ca':
                    for storename in ("CA", "MY"):
                        with wincertstore.CertSystemStore(storename) as store:
                            for cert in store.itercerts(usage=None):
                                pem = cert.get_pem()
                                encodedDer = ''.join(pem.split("\n")[1:-2])

                                cert_bytes = base64.b64decode(encodedDer)
                                cert_pem = ssl.DER_cert_to_PEM_cert(cert_bytes)
                                cert_details = x509.load_pem_x509_certificate(cert_pem.encode('utf-8'),
                                                                              default_backend())
                                serialnumber = hex(cert_details.serial_number).replace("0x", "")

                                if cert.get_name() == certName and certSerialNumber == serialnumber.upper():
                                    need_install = 0
                                    finded = True
                                    break
                                else:
                                    continue

                if not finded and need_install == 1:
                    if node == 'root':
                        if need_install == 1:
                            vars.need_install_root_certs.append(certPath)
                        else:
                            continue
                    elif node == 'ca':
                        if need_install == 1:
                            vars.need_install_ca_certs.append(certPath)
                        else:
                            continue
                    else:
                        mes.error('Проверка новых сертификатов',
                                  f'Внимание!\n\nУказан некорректный узел! {node}')
                        return False
                    self.certs_progress.step()
        return True

    if get_cert_from_folder('root'):
        print('Рут прочитали')
    else:
        print('Ошибка чтения рут')
    if get_cert_from_folder('ca'):
        print('Са прочитали')
    else:
        print('Ошибка чтения Са')
    if check_new_certs('root'):
        print('Рут проверили')
    else:
        print('Ошибка проверки рут')
    if check_new_certs('ca'):
        print('Са проверили')
    else:
        print('Ошибка проверки са')
    print('Проверяем даты ----------')
    data = get_old_certs()
    print(data)

    print(data[0])
    result = data[0][0]
    print(data[0][0])
    print(data[0][1])
    certs = data[0][1]
    certs_txt = 'Список сертификатов:\n'
    for cert in certs:
        print(cert)
        certs_txt += str(cert[0]) + '. ' + str(cert[1]) + ' - ' + str(cert[2].strftime("%d-%m-%Y")) + '\n'
    if result > 0:
        mes.info(f'Проверка хранилища сертификатов', f'Обращаем ваше внимание на то, что на устройстве в личном'
                                                     f' хранилище обнаружено {result} шт. просроченных сертификатов,'
                                                     f' которые можно удалить!\n\n{certs_txt}')
    print('----------------')

    if len(vars.need_install_root_certs) > 0 or len(vars.need_install_ca_certs) > 0:
        mes.info('Проверка сертификатов',
                 f'При проверке обнаружено неустановленных сертификатов:\nКорневые: {len(vars.need_install_root_certs)}\nПромежуточные: {len(vars.need_install_ca_certs)}')
        return False
    else:
        return True


def check_shortcut(self):
    import glob
    import win32com.client
    import winshell

    paths = glob.glob(winshell.desktop() + "\\*.lnk")

    shell = win32com.client.Dispatch("WScript.Shell")
    finded = ''
    gost = ''
    yandex = ''
    for path in paths:
        shortcut = shell.CreateShortCut(path)
        wDir = shortcut.WorkingDirectory
        target = shortcut.Targetpath
        if 'Закупки' in str(path) and 'chrome.exe' in target:
            print(path)
            gost = 'Chromium-Gost'

        if 'Закупки' in str(path) and 'YandexBrowser' in target:
            print(path)
            yandex = 'Яндекс Браузера'
    if gost != '' and yandex != '':
        finded = gost + ' и ' + yandex
    elif gost != '' and yandex == '':
        finded = gost
    elif gost == '' and yandex != '':
        finded = yandex
    return finded