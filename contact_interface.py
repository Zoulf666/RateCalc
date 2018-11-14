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
        add_contacts(name, remark)
    except Exception as e:
        print(e)
        tkinter.messagebox.showerror('错误', e)


def add_contacts(name='', remark=''):
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

    # btn_provice_edit = tkinter.Button(
    #     contact_root,
    #     text='费用详细编辑',
    #     command=lambda: select_provice_info_by_contact(contact_root, name)
    # )
    # btn_provice_edit.grid(row=3, column=1, columnspan=3, pady=20)
    # tkinter.Label(contact_root, text="省份").grid(row=4, column=0, padx=10)
    # tkinter.Label(contact_root, text="首重重量").grid(row=4, column=1)
    # tkinter.Label(contact_root, text="首重价格").grid(row=4, column=2)
    # tkinter.Label(contact_root, text="续重价格").grid(row=4, column=3)
    #
    # provices = ['北京', '天津', '上海', '重庆', '河北', '山西', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北',
    #             '湖南', '广东', '海南', '四川', '贵州', '云南', '陕西', '甘肃', '青海', '内蒙', '广西', '西藏', '宁夏', '新疆']
    # for index, provice in enumerate(provices):
    #     row = 5 + index
    #     tkinter.Label(contact_root, text=provice).grid(row=row, column=0, pady=5)
    #     tkinter.Entry(contact_root, width=3).grid(row=row, column=1)
    #     tkinter.Entry(contact_root, width=3).grid(row=row, column=2)
    #     tkinter.Entry(contact_root, width=3).grid(row=row, column=3)
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
        command=lambda: save_contact(contact_root, ety_name.get(), ety_remrk.get('1.0', tkinter.END)))
    btn_confirm.grid(row=5, column=0, sticky=tkinter.E)
    btn_cancel = tkinter.Button(contact_root, text='取消', command=contact_root.destroy)
    btn_cancel.grid(row=5, column=1, columnspan=2, sticky=tkinter.E)


def get_contact_infos():
    data = model.query_all_custom()
    return {custom_name: remark for custom_name, remark in data}


def select_provice_info_by_contact(master, custom_name):
    pass


def save_contact(master, custom_name, remark):
    try:
        if not custom_name:
            raise Exception('客户名不能为空！')

        if model.query_custom_id(custom_name):
            raise Exception('重复客户名！')

        model.insert_custom(custom_name, remark)
        master.destroy()
    except Exception as e:
        print(e)
        tkinter.messagebox.showerror('错误', e)

