import tkinter
import tkinter.messagebox
import utils
import contact_interface
import menu

from tkinter import ttk


def select_contact_by_name(*args):
    custom_name = select_list.get()
    infos = contact_interface.get_contact_infos()
    remark.set(infos[custom_name])


root = tkinter.Tk()
root.title('费用计算工具')
root.resizable(False, False)  # 让窗口不可以缩放
# root.iconbitmap('/home/zoulf/mycode/RateCalc/logo.ico')
size = utils.center_root(root, 600, 300)
root.geometry(size)
root.maxsize(600, 300)
root.minsize(300, 240)
menubar = menu.display_menu(root)  # 展示菜单

infos = contact_interface.get_contact_infos()
# 第零行：下拉列表、新增按钮、编辑按钮
tkinter.Label(root, text='请选择联系人:').grid(row=0, column=0, pady=10, padx=10)
select_list = tkinter.ttk.Combobox(root, width=30)
select_list["values"] = list(infos.keys())
select_list.bind("<<ComboboxSelected>>", select_contact_by_name)
select_list.grid(row=0, column=1, pady=10, padx=5)
btn_edit = tkinter.Button(root, text='编辑', command=lambda: contact_interface.edit_contacts(select_list))
btn_edit.grid(row=0, column=2, pady=10, padx=5)
btn_add = tkinter.Button(root, text='新增', command=contact_interface.add_contacts)
btn_add.grid(row=0, column=3, pady=10, padx=5)

# 第一行：备注信息
remark = tkinter.StringVar()
tkinter.Label(root, text='备注: ').grid(row=1, column=0)
tkinter.Label(root, textvariable=remark, wraplength=200).grid(row=1, column=1, columnspan=3, pady=10)

# 第二行：下划线
tkinter.Canvas(root, bg='black', height=1, width=600).grid(row=2, column=0, columnspan=4, pady=10)

# 第三行：文件导入标签、输入框、文件导入按钮
import_path = tkinter.StringVar()
# output_path = tkinter.StringVar()
tkinter.Label(root, text="导入文件路径:").grid(row=3, column=0, pady=10)
ety_import = tkinter.Entry(root, textvariable=import_path, width=50)
ety_import.grid(row=3, column=1, columnspan=2, pady=10)
btn_import = tkinter.Button(root, text="路径选择", command=lambda: utils.select_import_path(import_path))
btn_import.grid(row=3, column=3, pady=10)

# tkinter.Label(root, text="输出文件夹路径:").grid(row=3, column=0, pady=10)
# tkinter.Entry(root, textvariable=output_path, width=50).grid(row=3, column=1, columnspan=2, pady=10)
# tkinter.Button(root, text="路径选择", command=select_output_path).grid(row=3, column=3, pady=10)

# 开始计算按钮
# 第四行：计算按钮
btn_calc = tkinter.Button(root, text="计算", width=40, command=lambda: utils.calc(select_list, ety_import))
btn_calc.grid(row=4, column=0, columnspan=4, pady=20)

root.config(menu=menubar)
root.mainloop()
