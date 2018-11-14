import tkinter
import tkinter.messagebox


def display_menu(master):
    menubar = tkinter.Menu(master)
    file_menu = tkinter.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='文件', menu=file_menu)
    file_menu.add_command(label='新增联系人', command=show_version_info)
    file_menu.add_command(label='编辑联系人', command=show_version_info)
    file_menu.add_separator()
    file_menu.add_command(label='退出', command=master.quit)
    help_menu = tkinter.Menu(file_menu, tearoff=0)
    menubar.add_cascade(label='帮助', menu=help_menu)
    help_menu.add_command(label='版本信息', command=show_version_info)
    return menubar


def show_version_info():
    msg = """
    费用计算工具 V1.0
    Python版本 3.6
    """
    tkinter.messagebox.showinfo(title='版本信息', message=msg)
