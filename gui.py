import tkinter
import tkinter.filedialog
import tkinter.messagebox

from tkinter import ttk


def select_import_path():
    p = tkinter.filedialog.askopenfilename()
    import_path.set(p)


def select_output_path():
    p = tkinter.filedialog.askdirectory()
    output_path.set(p)


def do_job():
    pass


def show_version_info():
    msg = """
    费用计算工具 V1.0
    Python版本 3.6
    """
    tkinter.messagebox.showinfo(title='版本信息', message=msg)


def go(*args):
    value = select_list.get()


def add_contacts():
    pass


def calc():
    pass


def get_contact():
    return ["1231111111111111111111", "2", "3", "4"]


window = tkinter.Tk()
window.title('费用计算工具')
window.geometry('600x300')

# 菜单
menubar = tkinter.Menu(window)
file_menu = tkinter.Menu(menubar, tearoff=0)
menubar.add_cascade(label='文件', menu=file_menu)
file_menu.add_command(label='新增联系人', command=do_job)
file_menu.add_command(label='编辑联系人', command=do_job)
file_menu.add_separator()
file_menu.add_command(label='退出', command=window.quit)
help_menu = tkinter.Menu(file_menu, tearoff=0)
menubar.add_cascade(label='帮助', menu=help_menu)
help_menu.add_command(label='版本信息', command=show_version_info)

# 下拉列表及新增按钮
select_list = tkinter.ttk.Combobox(window)
select_list["values"] = get_contact()
select_list.bind("<<ComboboxSelected>>", go)
tkinter.Label(window, text='请选择联系人:').grid(row=1, column=1)
select_list.grid(row=1, column=2, padx=10, pady=10)
add_button = tkinter.Button(window, text='新增', command=add_contacts).grid(row=1, column=3, pady=10)

# 下划线
canvas = tkinter.Canvas(window, bg='black', height=1, width=600)
canvas.grid(row=2, columnspan=6, pady=10)

# 文件导入按钮
import_path = tkinter.StringVar()
output_path = tkinter.StringVar()
tkinter.Label(window, text="导入文件路径:").grid(row=3, column=1, pady=10)
tkinter.Entry(window, textvariable=import_path, width=50).grid(row=3, column=2)
tkinter.Button(window, text="路径选择", command=select_import_path).grid(row=3, column=3)

tkinter.Label(window, text="输出文件夹路径:").grid(row=4, column=1, pady=10)
tkinter.Entry(window, textvariable=output_path, width=50).grid(row=4, column=2)
tkinter.Button(window, text="路径选择", command=select_output_path).grid(row=4, column=3)

# 开始计算按钮
tkinter.Button(window, text="计算", command=calc, width=20).grid(row=5, column=2, pady=20)

window.config(menu=menubar)
window.mainloop()
