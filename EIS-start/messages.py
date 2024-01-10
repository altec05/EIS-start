from tkinter import messagebox


def error(title, text):
    mb = messagebox.showerror(title=title, message=text)


def info(title, text):
    mb = messagebox.showinfo(title=title, message=text)


def warning(title, text):
    mb = messagebox.showwarning(title=title, message=text)
