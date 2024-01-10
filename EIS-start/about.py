import customtkinter as CTk
from datetime import datetime


class AboutWin(CTk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("600x300+500+300")
        self.title('О программе')
        self.iconbitmap('logo_1.ico')

        label_text_up = f'Сведения о программе "ЕИС - старт"\n\n\n© Разработка и права: Домашенко Иван / Администратор ИБ ВС\n\n\nПрограмма была разработана в целях упрощения настройки АРМ в соответствии с требованиями сайта ЕИС\nПрограмма написана с применением языка программирования Python v3.11'
        label_text_center = f'Версия программы - ver. 1.2 от 26.05.2023 г.'
        label_text_down = f'КГКУЗ "Красноярский краевой центр крови №1"\n\n2023 - {datetime.now().year}'

        self.label_up = CTk.CTkLabel(self, text=label_text_up, wraplength=550)
        self.label_up.pack(padx=20, pady=15)

        self.label_center = CTk.CTkLabel(self, text=label_text_center, wraplength=550, anchor='center')
        self.label_center.pack(padx=20, pady=5)

        self.label_down = CTk.CTkLabel(self, text=label_text_down)
        self.label_down.pack(padx=20, pady=25)

        self.focus()
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", lambda: self.dismiss())  # перехватываем нажатие на крестик

    def dismiss(self):
        self.grab_release()
        self.destroy()
