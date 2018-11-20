import tkinter
import tkinter.messagebox
import utils
import contact_interface
import menu
import data_handle
import time
import tkinter.filedialog

import model
from tkinter import ttk


def select_contact_by_name(*args):
    custom_name = select_list.get()
    infos = custom.fetch_custom()
    remark.set(infos[custom_name])


def calc(path):
    try:
        for i in range(0, 45, 5):
            progress_bar["value"] = i + 1
            root.update()
            time.sleep(0.01)
        data_handle.excel_handle(path)
        for i in range(40, 101, 10):
            progress_bar["value"] = i
            root.update()
            time.sleep(0.01)
        tkinter.messagebox.showinfo(message='计算成功！')
    except Exception as e:
        print(e)
        tkinter.messagebox.showerror(message=e)
        progress_bar["value"] = 0
        root.update()


def import_custom():
    try:
        path = tkinter.filedialog.askopenfilename()
        for i in range(0, 45, 5):
            progress_bar["value"] = i + 1
            root.update()
            time.sleep(0.05)
        data_handle.excel_provice_handle(path)
        for i in range(40, 101, 10):
            progress_bar["value"] = i
            root.update()
            time.sleep(0.05)
        select_list["values"] = list(custom.fetch_custom().keys())
        tkinter.messagebox.showinfo(message='导入成功！')
    except Exception as e:
        print(e)
        tkinter.messagebox.showerror(message='导入数据不合法！')
        progress_bar["value"] = 0
        root.update()


root = tkinter.Tk()
root.title('费用计算工具')
root.resizable(False, False)  # 让窗口不可以缩放
size = utils.center_root(root, 600, 280)
root.geometry(size)
root.maxsize(600, 350)
root.minsize(300, 240)
custom = model.Custom()
infos = custom.fetch_custom()

# 第零行：下拉列表、新增按钮、编辑按钮
tkinter.Label(root, text='联系人列表:').grid(row=0, column=0, pady=10)
select_list = tkinter.ttk.Combobox(root, width=30)
select_list["values"] = list(infos.keys())
select_list.bind("<<ComboboxSelected>>", select_contact_by_name)
select_list.grid(row=0, column=1, pady=10)

btn_import_custom = tkinter.Button(root, text='导入', command=import_custom)
btn_import_custom.grid(row=0, column=2, pady=10, sticky=tkinter.W)
btn_edit = tkinter.Button(root, text='编辑', command=lambda: contact_interface.edit_contacts(select_list))
btn_edit.grid(row=0, column=3, pady=10, sticky=tkinter.W)
btn_add = tkinter.Button(root, text='新增', command=lambda: contact_interface.add_contacts(select_list))
btn_add.grid(row=0, column=4, pady=10, sticky=tkinter.W)

# 第一行：备注信息
remark = tkinter.StringVar()
tkinter.Label(root, text='备注: ').grid(row=1, column=0)
tkinter.Label(root, textvariable=remark, wraplength=200, justify=tkinter.LEFT).grid(row=1, column=1, columnspan=4,
                                                                                    pady=10, sticky=tkinter.W)

# 第二行：下划线
tkinter.Canvas(root, bg='black', height=1, width=600).grid(row=2, column=0, columnspan=5, pady=10)

# 第三行：文件导入标签、输入框、文件导入按钮
import_path = tkinter.StringVar()
# output_path = tkinter.StringVar()
tkinter.Label(root, text="导入文件路径:").grid(row=3, column=0, pady=10)
ety_import = tkinter.Entry(root, textvariable=import_path, width=50)
ety_import.grid(row=3, column=1, columnspan=3, pady=10)
btn_import = tkinter.Button(root, text="路径选择", command=lambda: utils.select_import_path(import_path))
btn_import.grid(row=3, column=4, pady=10)

# 第四行：计算按钮
btn_calc = tkinter.Button(root, text="计算", width=40, command=lambda: calc(ety_import.get()))
btn_calc.grid(row=4, column=0, columnspan=5, pady=20)

# 进度条以及完成程度
progress_bar = ttk.Progressbar(root, length=350, mode="determinate", orient=tkinter.HORIZONTAL)
progress_bar["maximum"] = 100
progress_bar["value"] = 0
progress_bar.grid(row=5, columnspan=5)

menubar = menu.display_menu(root, select_list)  # 展示菜单
root.config(menu=menubar)
root.mainloop()
