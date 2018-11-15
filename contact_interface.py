import model
import tkinter
import utils
import tkinter.messagebox

import provice_interface


def edit_contacts(select_list):
    name = select_list.get()
    infos = get_contact_infos()
    remark = infos.get(name, '')
    try:
        if not name:
            raise Exception('未选定编辑对象！')
        add_contacts(select_list, name, remark)
    except Exception as e:
        print(e)
        tkinter.messagebox.showerror('错误', e)


def add_contacts(select_list, name='', remark=''):
    contact_root = tkinter.Toplevel()
    if name:
        title = '编辑联系人'
    else:
        title = '新建联系人'

    name_value = tkinter.StringVar()
    name_value.set(name)
    contact_root.title(title)
    size = utils.center_root(contact_root, 300, 300)
    contact_root.resizable(False, False)
    contact_root.geometry(size)

    # 第零行，客户名
    tkinter.Label(contact_root, text="姓名：").grid(row=0, column=0, pady=20)
    ety_name = tkinter.Entry(contact_root, textvariable=name_value)
    ety_name.grid(row=0, column=1, columnspan=2, sticky=tkinter.W)

    # 第一、二行，备注
    tkinter.Label(contact_root, text="备注：").grid(row=1, column=0, rowspan=2)
    ety_remrk = tkinter.Text(contact_root, width=20, height=6)
    ety_remrk.insert(tkinter.INSERT, remark)
    ety_remrk.grid(row=1, column=1, rowspan=2, columnspan=2, sticky=tkinter.W)

    # 第三行，下划线
    canvas = tkinter.Canvas(contact_root, bg='black', height=1, width=200)
    canvas.grid(row=3, column=0, columnspan=3, pady=20)

    # 第四行，导入按钮与编辑按钮
    btn_import_provice = tkinter.Button(
        contact_root,
        text='导入省份数据',
        command=lambda: save_contact(contact_root, ety_name.get(), ety_remrk.get('1.0', tkinter.END)))
    btn_import_provice.grid(row=4, column=0, padx=10)
    btn_edit_provice = tkinter.Button(
        contact_root,
        text='编辑省份数据-->',
        command=lambda: provice_interface.add_provice_info(ety_name.get()))
    btn_edit_provice.grid(row=4, column=1, columnspan=2, sticky=tkinter.E)

    # 第五行，确定、取消按钮
    btn_confirm = tkinter.Button(
        contact_root,
        text='确定',
        # state='normal' if name else 'disabled',
        command=lambda: save_contact(contact_root, ety_name.get(), ety_remrk.get('1.0', tkinter.END), select_list))
    btn_confirm.grid(row=5, column=0, sticky=tkinter.E)
    btn_cancel = tkinter.Button(contact_root, text='取消', command=contact_root.destroy)
    btn_cancel.grid(row=5, column=1, columnspan=2, sticky=tkinter.E)


def get_contact_infos():
    data = model.query_all_custom()
    return {custom_name: remark for custom_name, remark in data}


def select_provice_info_by_contact(master, custom_name):
    pass


def save_contact(master, custom_name, remark, select_list):
    try:
        if not custom_name:
            raise Exception('客户名不能为空！')
        model.update_custom(custom_name, remark)
        select_list['values'] = list(get_contact_infos().keys())
        master.destroy()
    except Exception as e:
        print(e)
        tkinter.messagebox.showerror('错误', e)


def import_custom(select):
    pass