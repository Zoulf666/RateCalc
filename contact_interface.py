import model

from tkinter import Toplevel
from tkinter import Label
from tkinter import Button
from tkinter import Entry
from tkinter import W
from tkinter import E
from tkinter import S
from tkinter import N
from tkinter import StringVar
from tkinter import Canvas
from tkinter import Text
from tkinter import INSERT
from tkinter import END
from tkinter.messagebox import showerror
from utils import center_root
from provice_interface import edit_provice_info


def edit_contacts(select_list):
    name = select_list.get()
    custom = model.Custom()
    infos = custom.fetch_custom()
    remark = infos.get(name, '')
    try:
        if not name:
            raise Exception('未选定编辑对象！')
        custom_id = custom.find_custom(name)
        is_special = custom.get_special_value(custom_id)
        if is_special:
            raise Exception('该用户为特殊客户，不可编辑！')
        add_contacts(select_list, name, remark)
    except Exception as e:
        print(e)
        showerror('错误', e)
    finally:
        custom.close()


def add_contacts(select_list, name='', remark=''):
    contact_root = Toplevel()
    if name:
        title = '编辑联系人'
    else:
        title = '新建联系人'

    name_value = StringVar()
    name_value.set(name)
    contact_root.title(title)
    size = center_root(contact_root, 300, 300)
    contact_root.resizable(False, False)
    contact_root.geometry(size)

    # 第零行，客户名
    Label(contact_root, text="姓名：").grid(row=0, column=0, pady=20)
    ety_name = Entry(contact_root, textvariable=name_value)
    ety_name.grid(row=0, column=1, columnspan=2, sticky=W)

    # 第一、二行，备注
    Label(contact_root, text="备注：").grid(row=1, column=0, rowspan=2)
    ety_remrk = Text(contact_root, width=20, height=6)
    ety_remrk.insert(INSERT, remark)
    ety_remrk.grid(row=1, column=1, rowspan=2, columnspan=2, sticky=W)

    # 第三行，下划线
    canvas = Canvas(contact_root, bg='black', height=1, width=200)
    canvas.grid(row=3, column=0, columnspan=3, pady=20)

    # 第四行，编辑按钮
    btn_edit_provice = Button(
        contact_root,
        text='<--编辑省份数据-->',
        command=lambda: edit_provice_info(name if name else ety_name.get(), btn_confirm))
    btn_edit_provice.grid(row=4, column=0, columnspan=3, sticky=E + S + W + N)

    # 第五行，确定、取消按钮
    btn_confirm = Button(
        contact_root,
        text='确定',
        state='normal' if name else 'disabled',
        command=lambda: save_contact(contact_root, ety_name.get(), ety_remrk.get('1.0', END), select_list))
    btn_confirm.grid(row=5, column=0, sticky=E)
    btn_cancel = Button(contact_root, text='取消', command=contact_root.destroy)
    btn_cancel.grid(row=5, column=1, columnspan=2, sticky=E)


def save_contact(master, custom_name, remark, select_list):
    custom = model.Custom()
    try:
        if not custom_name:
            raise Exception('客户名不能为空！')
        old_custom_name = select_list.get()
        custom_id = custom.find_custom(old_custom_name)
        custom.update_custom(custom_id, custom_name, remark)
        select_list['values'] = list(custom.fetch_custom().keys())
        index = select_list['values'].index(custom_name)
        select_list.current(index)
        master.destroy()
    except Exception as e:
        print(e)
        showerror('错误', e)
    finally:
        custom.close()
