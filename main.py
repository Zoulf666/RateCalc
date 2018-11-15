import tkinter
import tkinter.messagebox
import utils
import contact_interface
import menu
import data_handle
import time

from tkinter import ttk


def select_contact_by_name(*args):
    custom_name = select_list.get()
    infos = contact_interface.get_contact_infos()
    remark.set(infos[custom_name])


# 更新进度条函数
def change_schedule(now_schedule, all_schedule):
    canvas.coords(fill_rec, (5, 5, 6 + (now_schedule / all_schedule) * 100, 25))
    root.update()
    progress_num.set(str(round(now_schedule / all_schedule * 100, 2)) + '%')
    if round(now_schedule / all_schedule * 100, 2) == 100.00:
        progress_num.set("完成")


def calc(select, ety_import):
    custom_name = select.get()
    path = ety_import.get()
    data_handle.excel_handle(path, custom_name)
    for i in range(10):
        time.sleep(0.1)
        change_schedule(i, 9)


root = tkinter.Tk()
root.title('费用计算工具')
root.resizable(False, False)  # 让窗口不可以缩放
size = utils.center_root(root, 600, 350)
root.geometry(size)
root.maxsize(600, 350)
root.minsize(300, 240)
menubar = menu.display_menu(root)  # 展示菜单

infos = contact_interface.get_contact_infos()
# 第零行：下拉列表、新增按钮、编辑按钮
tkinter.Label(root, text='请选择联系人:').grid(row=0, column=0, pady=10)
select_list = tkinter.ttk.Combobox(root, width=30)
select_list["values"] = list(infos.keys())
select_list.bind("<<ComboboxSelected>>", select_contact_by_name)
select_list.grid(row=0, column=1, pady=10)

btn_import_custom = tkinter.Button(root, text='导入', command=lambda: contact_interface.import_custom(select_list))
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

# tkinter.Label(root, text="输出文件夹路径:").grid(row=3, column=0, pady=10)
# tkinter.Entry(root, textvariable=output_path, width=50).grid(row=3, column=1, columnspan=2, pady=10)
# tkinter.Button(root, text="路径选择", command=select_output_path).grid(row=3, column=3, pady=10)

# 开始计算按钮
# 第四行：计算按钮
btn_calc = tkinter.Button(root, text="计算", width=40, command=lambda: calc(select_list, ety_import))
btn_calc.grid(row=4, column=0, columnspan=5, pady=20)

frame = tkinter.Frame(root).grid(row=5, column=0, columnspan=5)  # 使用时将框架根据情况选择新的位置
canvas = tkinter.Canvas(frame, width=150, height=30)
canvas.grid(row=5, column=0, columnspan=4, sticky=tkinter.E)
progress_num = tkinter.StringVar()
# 进度条以及完成程度
out_rec = canvas.create_rectangle(5, 5, 105, 25, outline="blue", width=0)
fill_rec = canvas.create_rectangle(5, 5, 5, 25, outline="", width=0, fill="blue")

tkinter.Label(frame, textvariable=progress_num).grid(row=5, column=4, sticky=tkinter.W)

root.config(menu=menubar)
root.mainloop()
