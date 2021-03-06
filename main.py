import utils
import data_handle
import model
import os.path

from time import sleep
from tkinter import Tk
from tkinter import Label
from tkinter import Button
from tkinter import Entry
from tkinter import Canvas
from tkinter import StringVar
from tkinter import HORIZONTAL
from tkinter import LEFT
from tkinter import W
from tkinter.ttk import Combobox
from tkinter.ttk import Progressbar
from tkinter.messagebox import showinfo
from tkinter.messagebox import showerror
from tkinter.filedialog import askopenfilename
from contact_interface import add_contacts
from contact_interface import edit_contacts
from menu import display_menu


def select_contact_by_name(*args):
    custom_name = select_list.get()
    infos = custom.fetch_custom()
    remark.set(infos[custom_name])


def select_import_path(i_path):
    path = askopenfilename(defaultextension='xlsx')
    # path = askopenfilename(defaultextension='xlsx',  filetypes=[('excel', 'xlsx')])
    i_path.set(path)
    return path


def calc(path):
    btn_calc['state'] = 'disable'
    btn_import_custom['state'] = 'disable'
    try:
        if not path:
            raise Exception('导入文件路径不能为空！')
        if not os.path.exists(path):
            raise Exception('导入文件路径不存在！')
        if not os.path.splitext(path)[1] == '.xlsx':
            raise Exception('导入文件格式错误！请导入.xlsx结尾的文件！')
        for i in range(0, 45, 5):
            progress_bar["value"] = i + 1
            root.update()
            sleep(0.01)
        unsign, error_provice = data_handle.excel_handle2(path)
        print(unsign)
        print(error_provice)
        for i in range(40, 101, 10):
            progress_bar["value"] = i
            root.update()
            sleep(0.01)
        if unsign:
            msg = '未录入客户：\n'
            for k, v in unsign.items():
                msg += '未录入客户：{}, 共出现{}次 \n'.format(v[0], v[1])
            if error_provice:
                for error, index in error_provice.items():
                    msg += '\n 第{}行，省份名：{}有误或未录入数据库！'.format(index, error)
            showinfo(message='计算成功, ' + msg + '请正确录入上述用户')
        else:
            showinfo(message='计算成功！')
    except Exception as e:
        print(e)
        showerror(title='计算失败', message=e)
        progress_bar["value"] = 0
        root.update()
    finally:
        btn_calc['state'] = 'normal'
        btn_import_custom['state'] = 'normal'


def import_custom():
    try:
        path = askopenfilename(defaultextension='xlsx')
        # path = askopenfilename(defaultextension='xlsx',  filetypes=[('excel', 'xlsx')])
        if not path:
            return
        if not os.path.splitext(path)[1] == '.xlsx':
            raise Exception('导入文件格式错误！请导入.xlsx结尾的文件！')
        for i in range(0, 45, 5):
            progress_bar["value"] = i + 1
            root.update()
            sleep(0.05)
        new_customs, error_customs = data_handle.excel_provice_handle(path)
        for i in range(40, 101, 10):
            progress_bar["value"] = i
            root.update()
            sleep(0.05)

        select_list["values"] = list(model.Custom().fetch_custom().keys())
        msg = '导入成功！\n'
        if new_customs:
            for custom in new_customs:
                msg += '新增用户：{} \n'.format(custom)
        if error_customs:
            for custom in error_customs:
                msg += '导入格式有误用户：{}'.format(custom)
        showinfo(message=msg, title='success!')
    except Exception as e:
        print(e)
        showerror(title='导入失败', message=e)
        progress_bar["value"] = 0
        root.update()


model.init_db()

root = Tk()
root.title('费用计算工具')
root.resizable(False, False)  # 让窗口不可以缩放
size = utils.center_root(root, 600, 320)
root.geometry(size)
root.maxsize(600, 450)
root.minsize(300, 240)
custom = model.Custom()
infos = custom.fetch_custom()

# 第零行：下拉列表、新增按钮、编辑按钮
Label(root, text='联系人列表:').grid(row=0, column=0, pady=10)
select_list = Combobox(root, width=30)
select_list["values"] = list(infos.keys())
select_list.bind("<<ComboboxSelected>>", select_contact_by_name)
select_list.grid(row=0, column=1, pady=10)

btn_import_custom = Button(root, text='导入', command=import_custom)
btn_import_custom.grid(row=0, column=2, pady=10, sticky=W)
btn_edit = Button(root, text='编辑', command=lambda: edit_contacts(select_list))
btn_edit.grid(row=0, column=3, pady=10, sticky=W)
btn_add = Button(root, text='新增', command=lambda: add_contacts(select_list))
btn_add.grid(row=0, column=4, pady=10, sticky=W)

# 第一行：备注信息
remark = StringVar()
Label(root, text='备注: ').grid(row=1, column=0)
Label(root, textvariable=remark, wraplength=300, justify=LEFT, font=('Helvetica', '9', 'normal')).grid(row=1, column=1,
                                                                                                       columnspan=4,
                                                                                                       sticky=W)

# 第二行：下划线
Canvas(root, bg='black', height=1, width=600).grid(row=2, column=0, columnspan=5, pady=10)

# 第三行：文件导入标签、输入框、文件导入按钮
import_path = StringVar()
# output_path = StringVar()
Label(root, text="导入文件路径:").grid(row=3, column=0, pady=10)
ety_import = Entry(root, textvariable=import_path, width=50)
ety_import.grid(row=3, column=1, columnspan=3, pady=10)
btn_import = Button(root, text="路径选择", command=lambda: select_import_path(import_path))
btn_import.grid(row=3, column=4, pady=10)

# 第四行：计算按钮
btn_calc = Button(root, text="计算", width=40, command=lambda: calc(ety_import.get()))
btn_calc.grid(row=4, column=0, columnspan=5, pady=20)

# 进度条以及完成程度
progress_bar = Progressbar(root, length=350, mode="determinate", orient=HORIZONTAL)
progress_bar["maximum"] = 100
progress_bar["value"] = 0
progress_bar.grid(row=5, columnspan=5)

menubar = display_menu(root, select_list)  # 展示菜单
root.config(menu=menubar)
root.mainloop()
