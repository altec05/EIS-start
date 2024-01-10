import os
from pathlib import Path

# Системные папки
usr_docs = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents')
appdata_path = os.path.join(os.path.join(os.environ['LOCALAPPDATA']))
appdata_roaming_path = os.path.join(os.path.join(os.environ['APPDATA']))
desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

# Последняя открытая папка
last_folder = ''

# Серверная папка с установочными файлами
install_folder = str(Path(r"\\192.168.15.4\Soft\ЕИС\Настройка рабочего места"))

# Путь до сторонней папки с установочниками
install_folder_changed_path = ''

# Используемый путь при установке
true_install_path = ''

# Временный путь до необходимого файла задаваемый пользователем, в случае отсутствия
temp_path = ''

# Инструкция для пользователя
readme_path = os.path.abspath("Readme.txt")

# Флаг остановки потока
thread_stop = False

# Переменные установки браузеров
browser_firefox_installed = False

browser_installed_path_true = ''
browser_installed_name_true = ''
browser_done = False
browser_cheked = False
browser_gost_installed = False
browser_gost_installed_name = ''
browser_gost_installed_path = ''
browser_yandex_installed = False
browser_yandex_installed_name = ''
browser_yandex_installed_path = ''

# Флаги проверки установки компонентов
crypto_done = False
crypto_cheked = False
plugin_done = False
plugin_checked = False
certs_done = False
certs_cheked = False
shortcut_done = False
shortcut_cheked = False
path_confirmed = False

# Переменные прогрессов
all_prVar = int(0)

# Переменные всплывающего окна
temp_true_answer = ''

# Списки сертификатов
installed_root_certs = list()
installed_ca_certs = list()
need_install_root_certs = list()
need_install_ca_certs = list()
certs_root_to_check = list()
certs_ca_to_check = list()

# Переменные файла отчета
log_data_text = ''
log_data_list = []
log_folder = str(Path(r'\\192.168.15.4\Soft\Программирование\Py\ЕИС - старт\Log файлы'))


def clear_vars():
    temp_path = ''
    installed_root_certs.clear()
    installed_ca_certs.clear()
    need_install_root_certs.clear()
    need_install_ca_certs.clear()
    certs_root_to_check.clear()
    certs_ca_to_check.clear()

# Цвета для темной темы

# Фон
#121212

# Кнопки
#03DAC6 - 1
#BB86FC - 2
# fg_color='#03DAC6', text_color='#000000'
# fg_color='#BB86FC', text_color='#000000'

# Кнопки выделение
#009688 - 1
#8755A6 - 2

# Кнопки неактив
#8ED4CD - 1
#CDAAE3 - 2

# fg_color='#8ED4CD', text_color='#000000', text_color_disabled='#4F4F4F'
# fg_color='#CDAAE3', text_color='#000000', text_color_disabled='#4F4F4F'

# Текст
#000000 - Ч
#FFFFFF - Б

# Текст неактив
#4F4F4F
#FFFFFF
