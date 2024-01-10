import customtkinter as CTk
import tkinter as tk
import tkinter.filedialog as fd
import os
import threading
from functools import partial
from PIL import Image

import about, faq
import check_funcs
import install_funcs
import service
import variables as vars
import messages as mes
from path_funcs import path_confirm


def change_appearance_mode_event(new_appearance_mode):
    CTk.set_appearance_mode(new_appearance_mode)


class App(CTk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("700x715")
        self.title("ЕИС - старт")
        self.resizable(False, False)
        self.iconbitmap('logo_1.ico')
        CTk.set_default_color_theme("dark-blue")
        CTk.set_appearance_mode("system")
        self.configure(fg_color='#1F1E1E')
        CTk.set_appearance_mode("dark")

        # Шапка
        self.welcome_label_frame = CTk.CTkFrame(master=self, fg_color='transparent')
        self.welcome_label_frame.pack(fill='x', ipadx=10, ipady=10)

        self.welcome_label = CTk.CTkLabel(master=self.welcome_label_frame,
                                          text='Используйте программу для проверки и настройки рабочего места',
                                          width=250, anchor='center', font=CTk.CTkFont(family='sans-serif', size=16))
        self.welcome_label.pack(side='top', pady=10)

        # Модуль общего запуска
        self.welcome_func_frame = CTk.CTkFrame(master=self, fg_color='transparent')
        self.welcome_func_frame.pack(fill='x', ipadx=10, ipady=10)

        self.start_button = CTk.CTkButton(master=self.welcome_func_frame, text='Начать проверку', width=180,
                                          fg_color='#03DAC6', text_color='#000000', hover_color='#009688',
                                          command=self.start_all)
        self.start_button.pack(side='left', pady=5, padx=25)

        self.all_prVar = tk.IntVar(value=0)
        self.all_progress = CTk.CTkProgressBar(master=self.welcome_func_frame, variable=self.all_prVar, width=450,
                                               progress_color='#CDAAE3')
        self.all_progress.pack(side='left', pady=5, padx=25)

        # Модуль Браузер
        self.browser_frame = CTk.CTkFrame(master=self, fg_color='transparent')
        self.browser_frame.pack(fill='x', ipadx=10, ipady=10)

        self.browser_button = CTk.CTkButton(master=self.browser_frame, text='Браузер', width=180, state='disabled',
                                            fg_color='#CDAAE3', text_color='#000000', text_color_disabled='#4F4F4F',
                                            hover_color='#8755A6', command=self.install_browser)
        self.browser_button.pack(side='left', pady=5, padx=25)

        self.browser_checkbox = CTk.CTkCheckBox(master=self.browser_frame, text="Неизвестно", onvalue="on",
                                                offvalue="off", state=tk.DISABLED, border_width=2, corner_radius=5,
                                                text_color_disabled='#FFFFFF')
        self.browser_checkbox.pack(side='left', pady=5, padx=25)

        # Модуль КриптоПро CSP
        self.crypto_frame = CTk.CTkFrame(master=self, fg_color='transparent')
        self.crypto_frame.pack(fill='x', ipadx=10, ipady=10)

        self.crypto_button = CTk.CTkButton(master=self.crypto_frame, text='КриптоПро CSP', width=180, state='disabled',
                                           fg_color='#CDAAE3', text_color='#000000', text_color_disabled='#4F4F4F',
                                           hover_color='#8755A6')
        self.crypto_button.pack(side='left', pady=5, padx=25)

        self.crypto_checkbox = CTk.CTkCheckBox(master=self.crypto_frame, text="Неизвестно", onvalue="on",
                                               offvalue="off", state=tk.DISABLED, border_width=2, corner_radius=5,
                                               text_color_disabled='#FFFFFF')
        self.crypto_checkbox.pack(side='left', pady=5, padx=25)

        # Модуль КриптоПро Плагин
        self.plugin_frame = CTk.CTkFrame(master=self, fg_color='transparent')
        self.plugin_frame.pack(fill='x', ipadx=10, ipady=10)

        self.plugin_button = CTk.CTkButton(master=self.plugin_frame, text='КриптоПро Плагин', width=180,
                                           state='disabled', fg_color='#CDAAE3', text_color='#000000',
                                           text_color_disabled='#4F4F4F', hover_color='#8755A6',
                                           command=self.install_crypto_plugin)
        self.plugin_button.pack(side='left', pady=5, padx=25)

        self.plugin_checkbox = CTk.CTkCheckBox(master=self.plugin_frame, text="Неизвестно", onvalue="on",
                                               offvalue="off", state=tk.DISABLED, border_width=2, corner_radius=5,
                                               text_color_disabled='#FFFFFF')
        self.plugin_checkbox.pack(side='left', pady=5, padx=25)

        # Модуль Сертификаты
        self.certs_frame = CTk.CTkFrame(master=self, fg_color='transparent')
        self.certs_frame.pack(fill='x', ipadx=10, ipady=10)

        self.certs_button = CTk.CTkButton(master=self.certs_frame, text='Сертификаты', width=180, state='disabled',
                                          fg_color='#CDAAE3', text_color='#000000', text_color_disabled='#4F4F4F',
                                          hover_color='#8755A6', command=self.install_certs)
        self.certs_button.pack(side='left', pady=5, padx=25)

        self.certs_checkbox = CTk.CTkCheckBox(master=self.certs_frame, text="Неизвестно", onvalue="on",
                                              offvalue="off", state=tk.DISABLED, border_width=2, corner_radius=5,
                                              text_color_disabled='#FFFFFF')
        self.certs_checkbox.pack(side='left', pady=5, padx=25)

        self.certs_prVar = tk.IntVar(value=0)
        self.certs_progress = CTk.CTkProgressBar(master=self.certs_frame, variable=self.certs_prVar,
                                                 progress_color='#CDAAE3')
        self.certs_progress.pack(side='left', pady=5, padx=25)

        # Модуль Ярлык
        self.shortcut_frame = CTk.CTkFrame(master=self, fg_color='transparent')
        self.shortcut_frame.pack(fill='x', ipadx=10, ipady=10)

        self.shortcut_button = CTk.CTkButton(master=self.shortcut_frame, text='Ярлык', width=180, state='disabled',
                                             fg_color='#CDAAE3', text_color='#000000', text_color_disabled='#4F4F4F',
                                             hover_color='#8755A6', command=self.create_shortcut)
        self.shortcut_button.pack(side='left', pady=5, padx=25)

        self.shortcut_checkbox = CTk.CTkCheckBox(master=self.shortcut_frame, text="Неизвестно", onvalue="on",
                                                 offvalue="off", state=tk.DISABLED, border_width=2, corner_radius=5,
                                                 text_color_disabled='#FFFFFF')
        self.shortcut_checkbox.pack(side='left', pady=5, padx=25)

        # Модуль Путь до файлов
        self.files_frame = CTk.CTkFrame(master=self, fg_color='transparent', height=300)
        self.files_frame.pack(fill='x', ipadx=10, ipady=10, pady=10)

        self.files_button = CTk.CTkButton(master=self.files_frame, text='Указать', width=180,
                                          command=self.set_install_path, fg_color='#BB86FC', text_color='#000000',
                                          text_color_disabled='#4F4F4F', hover_color='#8755A6')
        self.files_button.pack(side='left', pady=5, padx=25)

        self.files_label = CTk.CTkLabel(master=self.files_frame,
                                        text='Если нет доступа к файловому серверу, то укажите папку с файлами для установки',
                                        width=250, wraplength=450, anchor='w')
        self.files_label.pack(side='left', pady=5)

        self.files_checkbox = CTk.CTkCheckBox(master=self.files_frame, text="Файлы обнаружены", onvalue="on",
                                              offvalue="off", state=tk.DISABLED, border_width=2, corner_radius=5,
                                              text_color_disabled='#FFFFFF')
        self.crypto_checkbox.pack(side='left', pady=5, padx=25)

        # Модуль Ссылок на драйверы
        self.drivers_frame = CTk.CTkFrame(master=self, fg_color='transparent')
        self.drivers_frame.pack(fill='x', ipadx=10, ipady=5, pady=7)

        self.drivers_label = CTk.CTkLabel(master=self.drivers_frame,
                                          text='Если носитель закрытого ключа ЭП не виден в системе, и windows не установила нужный драйвер:\n\nРутокен - "красная флешка"\nЕтокен - "синяя флешка"',
                                          width=250, wraplength=250)
        self.drivers_label.pack(pady=5, ipady=10, padx=25, side='left')

        self.rutoken_button = CTk.CTkButton(master=self.drivers_frame, text='Rutoken', width=120,
                                            command=self.show_rutoken, fg_color='#CDAAE3', text_color='#000000',
                                            text_color_disabled='#4F4F4F', hover_color='#8755A6')
        self.rutoken_button.pack(pady=5, padx=25, side='left')

        self.etoken_button = CTk.CTkButton(master=self.drivers_frame, text='Etoken', width=120,
                                           command=self.show_etoken,
                                           fg_color='#CDAAE3', text_color='#000000', text_color_disabled='#4F4F4F',
                                           hover_color='#8755A6')
        self.etoken_button.pack(pady=5, padx=5, side='left')

        # Модуль Дополнительных опций
        self.options_frame = CTk.CTkFrame(master=self, fg_color='transparent')
        self.options_frame.pack(fill='x', ipadx=20, ipady=10, pady=15)

        self.about_button = CTk.CTkButton(master=self.options_frame, text='О программе', width=120,
                                          command=self.show_about, fg_color='#CDAAE3', text_color='#000000',
                                          text_color_disabled='#4F4F4F', hover_color='#8755A6')
        self.about_button.pack(side='left', pady=5, padx=25)

        self.faq_button = CTk.CTkButton(master=self.options_frame, text='FaQ', width=120, command=self.show_faq,
                                        fg_color='#CDAAE3', text_color='#000000', text_color_disabled='#4F4F4F',
                                        hover_color='#8755A6')
        self.faq_button.pack(side='left', pady=5, padx=5)

        self.reload_image = CTk.CTkImage(Image.open(os.path.abspath('reload.png')), size=(30, 30))

        self.relaod_button = CTk.CTkButton(master=self.options_frame, text='', image=self.reload_image, width=30,
                                           height=30, fg_color='#CDAAE3', text_color='#000000',
                                           text_color_disabled='#4F4F4F', hover_color='#8755A6',
                                           command=self.update_connection)
        self.relaod_button.pack(side='right', pady=5, padx=15)

        self.connect_checkbox = CTk.CTkCheckBox(master=self.options_frame, text="Доступ к серверу", onvalue="on",
                                                offvalue="off", state=tk.DISABLED, border_width=2, corner_radius=5,
                                                text_color_disabled='#FFFFFF')
        self.connect_checkbox.pack(side='right', pady=5, padx=25)

        # Переменная всплывающего окна для предотвращения повторного открытия
        self.toplevel_window = None


    def show_rutoken(self):
        if not check_funcs.check_connection(self, False):
            mes.error('Открыть страницу драйвера Рутокен', 'Внимание!\n\nОтсутствует соединение с сетью Интернет! Не удалось открыть веб-страницу!')
            return False
        else:
            import webbrowser
            webbrowser.open('https://www.rutoken.ru/support/download/windows/', new=2)

    def show_etoken(self):
        temp = '\\'
        if not vars.path_confirmed:
            if not path_confirm(self, app):
                print('----')
                return False
            else:
                if vars.install_folder_changed_path != '' and vars.true_install_path != '' and install_funcs.check_path(
                        str(os.path.join(vars.true_install_path, 'Софт', 'Etoken PKI Client')).replace('/', temp)):
                    mes.info('PKI Client',
                             'Сейчас откроется папка с установочными файлами Etoken PKI Client.\n\nВыберите файл в зависимости от системы с расширением msi.')
                    print('*****************')
                    os.system(
                        f"explorer.exe {str(os.path.join(vars.true_install_path, 'Софт', 'Etoken PKI Client')).replace('/', temp)}")
                elif vars.install_folder_changed_path != '' and check_funcs.check_connection(self,
                                                                                             False) and install_funcs.check_path(
                        str(os.path.join(vars.install_folder, 'Софт', 'Etoken PKI Client')).replace('/', temp)):
                    print('1111111111111111')
                    mes.info('PKI Client',
                             'Сейчас откроется папка с установочными файлами Etoken PKI Client.\n\nВыберите файл в зависимости от системы с расширением msi.')

                    path = os.path.join(vars.install_folder, "Софт", "Etoken PKI Client")
                    os.system(
                        fr'explorer.exe "{str(path).replace("/", temp)}"')
                elif vars.install_folder_changed_path == '' and check_funcs.check_connection(self, False):
                    mes.info('PKI Client',
                             'Сейчас откроется стандартная сетевая папка с установочными файлами Etoken PKI Client.\n\nВыберите файл в зависимости от системы с расширением msi.')

                    path = os.path.join(vars.install_folder, "Софт", "Etoken PKI Client")
                    os.system(
                        fr'explorer.exe "{str(path).replace("/", temp)}"')
                else:
                    mes.error('Открыть расположение драйвера Етокен',
                              f"Внимание!\n\nУказанный вами путь некорректен, пробуем открыть веб-страницу загрузки!\n\n[{os.path.join(vars.true_install_path, 'Софт', 'Etoken PKI Client')}]")
                    if not check_funcs.check_connection(self, False):
                        mes.error('Открыть страницу драйвера Етокен',
                                  'Внимание!\n\nОтсутствует соединение с сетью Интернет! Не удалось открыть веб-страницу!')
                        return False
                    else:
                        mes.info('PKI Client',
                                 'Сейчас откроется страница загрузки в вашем браузере.\n\nНайдите на ней "Скачать драйвер eToken PKI Client для Microsoft Windows" и загрузите.')

                        import webbrowser
                        webbrowser.open('https://erim.ru/gde-skachat-i-kak-ustanovit-drayvery-etoken.html', new=2)
        else:
            if vars.install_folder_changed_path != '' and vars.true_install_path != '' and install_funcs.check_path(
                    str(os.path.join(vars.true_install_path, 'Софт', 'Etoken PKI Client')).replace('/', temp)):
                mes.info('PKI Client',
                         'Сейчас откроется папка с установочными файлами Etoken PKI Client.\n\nВыберите файл в зависимости от системы с расширением msi.')
                print('*****************')
                path = os.path.join(vars.true_install_path, "Софт", "Etoken PKI Client")
                os.system(
                    f"explorer.exe {str(os.path.join(vars.true_install_path, 'Софт', 'Etoken PKI Client')).replace('/', temp)}")
            elif vars.install_folder_changed_path != '' and check_funcs.check_connection(self,
                                                                                         False) and install_funcs.check_path(
                str(os.path.join(vars.install_folder, 'Софт', 'Etoken PKI Client')).replace('/', temp)):
                print('1111111111111111')
                mes.info('PKI Client',
                         'Сейчас откроется папка с установочными файлами Etoken PKI Client.\n\nВыберите файл в зависимости от системы с расширением msi.')

                path = os.path.join(vars.install_folder, "Софт", "Etoken PKI Client")
                os.system(
                    fr'explorer.exe "{str(path).replace("/", temp)}"')
            elif vars.install_folder_changed_path == '' and check_funcs.check_connection(self, False):
                mes.info('PKI Client',
                         'Сейчас откроется стандартная сетевая папка с установочными файлами Etoken PKI Client.\n\nВыберите файл в зависимости от системы с расширением msi.')

                path = os.path.join(vars.install_folder, "Софт", "Etoken PKI Client")
                os.system(
                    fr'explorer.exe "{str(path).replace("/", temp)}"')
            else:
                mes.error('Открыть расположение драйвера Етокен',
                          f"Внимание!\n\nУказанный вами путь некорректен, пробуем открыть веб-страницу загрузки!\n\n[{os.path.join(vars.true_install_path, 'Софт', 'Etoken PKI Client')}]")
                if not check_funcs.check_connection(self, False):
                    mes.error('Открыть страницу драйвера Етокен',
                              'Внимание!\n\nОтсутствует соединение с сетью Интернет! Не удалось открыть веб-страницу!')
                    return False
                else:
                    mes.info('PKI Client',
                             'Сейчас откроется страница загрузки в вашем браузере.\n\nНайдите на ней "Скачать драйвер eToken PKI Client для Microsoft Windows" и загрузите.')

                    import webbrowser
                    webbrowser.open('https://erim.ru/gde-skachat-i-kak-ustanovit-drayvery-etoken.html', new=2)

    def check_connection(self):
        up = False
        if install_funcs.check_connection(self, up):
            return True
        else:
            return False

    def update_connection(self):
        up = False
        install_funcs.check_connection(self, up)

    def set_install_path(self):
        if vars.last_folder == '':
            vars.install_folder_changed_path = fd.askdirectory(title="Укажите путь до файлов установки",
                                                               initialdir=f"{vars.usr_docs}")
            if vars.install_folder_changed_path != '':
                vars.last_folder = vars.install_folder_changed_path
                mes.info('Ручное указание пути',
                         f'Вы успешно указали путь к установочным файлам!\n\n{vars.install_folder_changed_path}')

            print(f"ch_Path: {vars.install_folder_changed_path}")
        else:
            vars.install_folder_changed_path = fd.askdirectory(title="Укажите путь до файлов установки",
                                                               initialdir=f"{vars.last_folder}")
            if vars.install_folder_changed_path != '':
                vars.last_folder = vars.install_folder_changed_path
                mes.info('Ручное указание пути',
                         f'Вы успешно указали путь к установочным файлам!\n\n{vars.install_folder_changed_path}')

            print(f"ch_Path: {vars.install_folder_changed_path}")

        install_funcs.path_confirm(self, app)

    def install_crypto_csp(self):
        if install_funcs.install_crypto_csp(self, app):
            self.crypto_checkbox.configure(text=f'Установлен')
            self.crypto_checkbox.configure(fg_color='green')
            self.crypto_checkbox.select()
            self.crypto_button.configure(state='disabled', fg_color='#CDAAE3', text_color='#000000',
                                         text_color_disabled='#4F4F4F')
        else:
            self.crypto_checkbox.configure(text=f'Ошибка установки')
            self.crypto_checkbox.deselect()
            self.crypto_button.configure(state='normal', fg_color='#BB86FC', text_color='#000000')

    def install_crypto_plugin(self):
        if install_funcs.install_crypto_plugin(self, app):
            if vars.plugin_done:
                self.plugin_button.configure(state='disabled', fg_color='#CDAAE3', text_color='#000000',
                                             text_color_disabled='#4F4F4F')
                self.plugin_checkbox.configure(text='Установлен')
                self.plugin_checkbox.configure(fg_color='green')
                self.plugin_checkbox.select()
            else:
                self.plugin_button.configure(state='normal', fg_color='#BB86FC', text_color='#000000')
                self.plugin_checkbox.configure(text='Не установлен')
                self.plugin_checkbox.deselect()
        else:
            self.plugin_button.configure(state='normal', fg_color='#BB86FC', text_color='#000000')
            self.plugin_checkbox.configure(text='Ошибка установки')
            self.plugin_checkbox.deselect()

    def install_certs(self):
        if install_funcs.install_certs(self):
            self.certs_checkbox.configure(text=f'Установлены')
            self.certs_checkbox.configure(fg_color='green')
            self.certs_checkbox.select()
            self.certs_button.configure(state='disabled', fg_color='#CDAAE3', text_color='#000000',
                                        text_color_disabled='#4F4F4F')
        else:
            self.certs_checkbox.configure(text=f'Ошибка установки')
            self.certs_checkbox.deselect()
            self.certs_button.configure(state='normal', fg_color='#BB86FC', text_color='#000000',
                                        command=self.install_certs)

    def install_browser(self):
        if install_funcs.install_browser(self, app):
            # После установки проверяем браузеры
            # чтобы прописались имена и пути в переменные
            if check_funcs.check_browser(self):
                if vars.browser_yandex_installed and vars.browser_gost_installed:
                    self.browser_button.configure(state='disabled', fg_color='#CDAAE3', text_color='#000000',
                                                  text_color_disabled='#4F4F4F')
                    self.browser_checkbox.configure(text=f'Установлены {vars.browser_gost_installed_name} и {vars.browser_yandex_installed_name}')
                    self.browser_checkbox.configure(fg_color='green')
                    self.browser_checkbox.select()
                elif vars.browser_yandex_installed and not vars.browser_gost_installed:
                    self.browser_button.configure(state='normal', fg_color='#BB86FC', text_color='#000000')
                    self.browser_checkbox.configure(text=f'Установлен {vars.browser_yandex_installed_name}')
                    self.browser_checkbox.configure(fg_color='green')
                    self.browser_checkbox.select()
                elif not vars.browser_yandex_installed and vars.browser_gost_installed:
                    self.browser_button.configure(state='disabled', fg_color='#CDAAE3', text_color='#000000',
                                                  text_color_disabled='#4F4F4F')
                    self.browser_checkbox.configure(text=f'Установлен {vars.browser_gost_installed_name}')
                    self.browser_checkbox.configure(fg_color='green')
                    self.browser_checkbox.select()
            else:
                self.browser_button.configure(state='normal', fg_color='#BB86FC', text_color='#000000')
                self.browser_checkbox.configure(text='Не установлен')
                self.browser_checkbox.deselect()
        else:
            if check_funcs.check_browser(self):
                if vars.browser_yandex_installed and vars.browser_gost_installed:
                    self.browser_button.configure(state='disabled', fg_color='#CDAAE3', text_color='#000000',
                                                  text_color_disabled='#4F4F4F')
                    self.browser_checkbox.configure(
                        text=f'Установлены {vars.browser_gost_installed_name} и {vars.browser_yandex_installed_name}')
                    self.browser_checkbox.configure(fg_color='green')
                    self.browser_checkbox.select()
                elif vars.browser_yandex_installed and not vars.browser_gost_installed:
                    self.browser_button.configure(state='normal', fg_color='#BB86FC', text_color='#000000')
                    self.browser_checkbox.configure(text=f'Установлен {vars.browser_yandex_installed_name}')
                    self.browser_checkbox.configure(fg_color='green')
                    self.browser_checkbox.select()
                elif not vars.browser_yandex_installed and vars.browser_gost_installed:
                    self.browser_button.configure(state='disabled', fg_color='#CDAAE3', text_color='#000000',
                                                  text_color_disabled='#4F4F4F')
                    self.browser_checkbox.configure(text=f'Установлен {vars.browser_gost_installed_name}')
                    self.browser_checkbox.configure(fg_color='green')
                    self.browser_checkbox.select()
            else:
                self.browser_button.configure(state='normal', fg_color='#BB86FC', text_color='#000000')
                self.browser_checkbox.configure(text='Ошибка установки')
                self.browser_checkbox.deselect()

    def create_shortcut(self):
        if install_funcs.install_shortcut(self):
            self.shortcut_button.configure(state='normal', fg_color='#BB86FC', text_color='#000000')
            # self.shortcut_button.configure(state='disabled', fg_color='#CDAAE3', text_color='#000000',
            #                                text_color_disabled='#4F4F4F')
            self.shortcut_checkbox.configure(text=f'Создан для "{vars.browser_installed_name_true}"')
            self.shortcut_checkbox.configure(fg_color='green')
            self.shortcut_checkbox.select()
        else:
            self.shortcut_button.configure(state='normal', fg_color='#BB86FC', text_color='#000000')
            self.shortcut_checkbox.configure(text=f'Ошибка создания')
            self.shortcut_checkbox.deselect()

    def start_all(self):
        def check_thread(self, thread):
            if thread.is_alive():
                self.all_progress.start()
                self.after(100, lambda: self.check_thread(thread))
            else:
                self.start_button.configure(state='normal', text='Начать проверку', fg_color='#03DAC6', text_color='#000000')
                self.files_button.configure(state='normal', fg_color='#BB86FC', text_color='#000000',
                                            text_color_disabled='#4F4F4F')

                self.all_progress.set(1)
                self.all_progress.stop()

                self.start_button.configure(state='disabled', text='Проверка окончена', fg_color='#8ED4CD', text_color='#000000',
                                            text_color_disabled='#4F4F4F')

                if not vars.browser_done:
                    self.browser_button.configure(state='normal', fg_color='#BB86FC', text_color='#000000')
                elif vars.browser_yandex_installed and not vars.browser_gost_installed:
                    self.browser_button.configure(state='normal', fg_color='#BB86FC', text_color='#000000')
                else:
                    self.browser_button.configure(state='disabled', fg_color='#CDAAE3', text_color='#000000',
                                      text_color_disabled='#4F4F4F')
                if not vars.crypto_done:
                    self.crypto_button.configure(state='normal', fg_color='#BB86FC', text_color='#000000',
                                                 command=self.install_crypto_csp)
                if not vars.plugin_done:
                    self.plugin_button.configure(state='normal', fg_color='#BB86FC', text_color='#000000')
                if not vars.certs_done:
                    self.certs_button.configure(state='normal', fg_color='#BB86FC', text_color='#000000',
                                                command=self.install_certs)
                self.shortcut_button.configure(state='normal', fg_color='#BB86FC', text_color='#000000',
                                               command=self.create_shortcut)
                # if not vars.shortcut_done:
                #     self.shortcut_button.configure(state='normal', fg_color='#BB86FC', text_color='#000000',
                #                                    command=self.create_shortcut)

        mes.info('Рекомендация к запуску',
                 'Рекомендуем запускать приложение с правами администратора для корректной установки программ!\n\nЗапускаем проверку...')

        # Подтверждаем путь установки
        if not vars.path_confirmed:
            if not path_confirm(self, app):
                print('----')
                return False
            else:
                print('++++')
                service.get_system_info()
                self.start_button.configure(state='disabled', text='Идет проверка...', fg_color='#8ED4CD', text_color='#000000',
                                            text_color_disabled='#4F4F4F')
                self.browser_button.configure(state='disabled', fg_color='#CDAAE3', text_color='#000000',
                                              text_color_disabled='#4F4F4F')
                self.crypto_button.configure(state='disabled', fg_color='#CDAAE3', text_color='#000000',
                                             text_color_disabled='#4F4F4F')
                self.plugin_button.configure(state='disabled', fg_color='#CDAAE3', text_color='#000000',
                                             text_color_disabled='#4F4F4F')
                self.certs_button.configure(state='disabled', fg_color='#CDAAE3', text_color='#000000',
                                            text_color_disabled='#4F4F4F')
                self.shortcut_button.configure(state='disabled', fg_color='#CDAAE3', text_color='#000000',
                                               text_color_disabled='#4F4F4F')
                self.files_button.configure(state='disabled', fg_color='#CDAAE3', text_color='#000000',
                                            text_color_disabled='#4F4F4F')

                thread = threading.Thread(target=check_funcs.start_all(self, app), daemon=False)
                thread.start()
                check_thread(self, thread)
        else:
            print('====')
            service.get_system_info()
            self.start_button.configure(state='disabled', text='Идет проверка...', fg_color='#8ED4CD', text_color='#000000',
                                        text_color_disabled='#4F4F4F')
            self.browser_button.configure(state='disabled', fg_color='#CDAAE3', text_color='#000000',
                                          text_color_disabled='#4F4F4F')
            self.crypto_button.configure(state='disabled', fg_color='#CDAAE3', text_color='#000000',
                                         text_color_disabled='#4F4F4F')
            self.plugin_button.configure(state='disabled', fg_color='#CDAAE3', text_color='#000000',
                                         text_color_disabled='#4F4F4F')
            self.certs_button.configure(state='disabled', fg_color='#CDAAE3', text_color='#000000',
                                        text_color_disabled='#4F4F4F')
            self.shortcut_button.configure(state='disabled', fg_color='#CDAAE3', text_color='#000000',
                                           text_color_disabled='#4F4F4F')
            self.files_button.configure(state='disabled', fg_color='#CDAAE3', text_color='#000000',
                                        text_color_disabled='#4F4F4F')

            thread = threading.Thread(target=check_funcs.start_all(self, app), daemon=False)
            thread.start()
            check_thread(self, thread)

    def show_about(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = about.AboutWin(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it

    def show_faq(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = faq.InstructionWin(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it

    def on_close(root):
        if len(vars.log_data_list) > 0:
            service.get_full_txt(service.get_info_for_log_file_name())
        vars.clear_vars()
        mes.info('Закрытие приложения', 'Благодарим вас за использование программы!\n\nВаши пожелания или найденные недочеты вы можете отправить на почту ikdomashenko@kkck.ru.')
        root.destroy()


if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", partial(app.on_close))
    app.mainloop()
