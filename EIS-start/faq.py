import customtkinter as CTk
from datetime import datetime
from check_funcs import check_path
from variables import readme_path


def read_file_instr(path):
    file = open(path, mode="r")
    list_readme = file.read()
    file.close()
    return list_readme


class InstructionWin(CTk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("1300x450+500+300")
        self.minsize(600, 450)
        self.title('Инструкция к программе')
        self.iconbitmap('logo_1.ico')

        label_text_up = f'Настоящая инструкция осветит основные моменты взаимодействия с программой "ЕИС - старт"'
        label_text_down = f'КГКУЗ "Красноярский краевой центр крови №1"\n\n2023 - {datetime.now().year}'

        self.label_up = CTk.CTkLabel(self, text=label_text_up, wraplength=650)
        self.label_up.pack(padx=20, pady=10)

        self.readme_box = CTk.CTkTextbox(self, corner_radius=0, wrap='word')
        self.readme_box.pack(padx=20, pady=10, expand=True, fill='both')
        self.create_file()
        self.readme_box.configure(state='disabled')

        self.label_down = CTk.CTkLabel(self, text=label_text_down)
        self.label_down.pack(padx=20, pady=10)

        self.focus()
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", lambda: self.dismiss()) # перехватываем нажатие на крестик

    def dismiss(self):
        self.grab_release()
        self.destroy()

    def create_file(self):
        if check_path(readme_path):
            list_readme = read_file_instr(readme_path)
            self.readme_box.insert('0.0', list_readme)
        else:
            readme_text = '\t\t\tКак работать с программой?\n\n\nВАЖНО! Программу необходимо запускать от имени' \
                          ' администратора, т.к. она использует корневые хранилища и запускает установку файлов!\n\n\n' \
                          '1. При запуске программы, по кнопке "Начать проверку", выполняется проверка наличия требуемых компонентов на АРМ .\n' \
                          '\t\t- о ходе проверки вы можете судить по шкале прогресса в верхней части окна.\n' \
                          '\t\t- по ходу проверки вы можете получать уведомления.\n\n' \
                          '2. По окончанию проверки, кнопки для неустановленных компонентов разблокируются.\n' \
                          '\t\t- каждая кнопка запускает отдельный процесс установки, и о ходе его выполнения вы можете' \
                          ' судить по всплывающим уведомлениям или сообщениям в запускаемом приложении установки компонента.\n' \
                          '\t\t- во время установки интерфейс главного окна может не отвечать на нажатия до момента окончания установки.\n\n' \
                          '3. При отсутствии связи с сервером 192.168.15.4, вы можете вручную указать папку с установочными файлами.\n' \
                          '\t\t- программа ищет файлы по заданной иерархии в папке с установочными файлами, поэтому,' \
                          ' во избежание ошибок, исходный обновляемый пакет следует заранее скопировать с сервера из' \
                          ' директории "192.168.15.4\Soft\ЕИС\Настройка рабочего места".\n\n' \
                          '4. В случае, если КриптоПро CSP не может определить ваш носитель закрытого ключа ЭП - ' \
                          'в нижней части главного окна воспользуйтесь кнопками перехода к установочным файлам' \
                          ' драйверов носителей (Рутокен или Етокен).\n\n' \
                          '5. В случае возникновения ошибок или вопросов:\n\t\t- обращайтесь на почту ikdomashenko@kkck.ru\n' \
                          '\t\t- обращайтесь в отдел АСУ г.Красноярска\n' \

            file = open(readme_path, "w+")
            file.write(readme_text)
            file.close()

            list_readme = read_file_instr(readme_path)
            self.readme_box.insert('0.0', list_readme)
