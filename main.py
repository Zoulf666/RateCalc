import tkinter
import tkinter.filedialog
import tkinter.messagebox

import model
import utils
from tkinter import ttk


def select_import_path():
    p = tkinter.filedialog.askopenfilename()
    import_path.set(p)


def select_output_path():
    p = tkinter.filedialog.askdirectory()
    output_path.set(p)


def do_job():
    pass


def calc():
    pass


def show_version_info():
    msg = """
    费用计算工具 V1.0
    Python版本 3.6
    """
    tkinter.messagebox.showinfo(title='版本信息', message=msg)


# def go(*args):
#     value = select_list.get()


def get_contacts():
    data = model.query_all_custom()
    custom_nams = []
    remarks = []
    for d in data:
        c, r = d
        custom_nams.append(c)
        remarks.append(r)
    return custom_nams, remarks


def select_contact_by_name(*args):
    value = select_list.get()


def select_provice_info_by_contact(master, custom_name):
    pass


def save_contact(master, custom_name, remark):
    try:
        if not custom_name:
            raise Exception('客户名不能为空！')

        if model.query_custom_by_name(custom_name):
            raise Exception('重复客户名！')

        model.insert_custom(custom_name, remark)
        master.destroy()
    except Exception as e:
        print(e)
        tkinter.messagebox.showerror('错误', e)


def save_provice_info():
    pass


def add_provice_info(name=''):
    provice_root = tkinter.Toplevel()


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

    tkinter.Label(contact_root, text="姓名：").grid(row=0, column=0, pady=20, sticky=tkinter.E)
    ety_name = tkinter.Entry(contact_root, textvariable=name_value)
    ety_name.grid(row=0, column=1, columnspan=2, padx=10)

    tkinter.Label(contact_root, text="备注：").grid(row=1, column=0, sticky=tkinter.E)
    ety_remrk = tkinter.Text(contact_root, width=20, height=6)
    ety_remrk.insert(tkinter.INSERT, remark)
    ety_remrk.grid(row=1, column=1, rowspan=2, columnspan=2)

    # 下划线
    canvas = tkinter.Canvas(contact_root, bg='black', height=1, width=300)
    canvas.grid(row=3, column=0, columnspan=4, pady=20)

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
    btn_import_provice = tkinter.Button(
        contact_root,
        text='导入省份数据',
        command=lambda: save_contact(contact_root, ety_name.get(), ety_remrk.get('1.0', tkinter.END)))
    btn_import_provice.grid(row=4, column=0, columnspan=4)

    btn_confirm = tkinter.Button(
        contact_root,
        text='确定',
        state='normal' if name else 'disabled',
        command=lambda: save_contact(contact_root, ety_name.get(), ety_remrk.get('1.0', tkinter.END)))
    btn_confirm.grid(row=5, column=0, sticky=tkinter.E)

    btn_cancel = tkinter.Button(contact_root, text='取消', command=contact_root.destroy)
    btn_cancel.grid(row=5, column=3)


def display_menu(root):
    menubar = tkinter.Menu(root)
    file_menu = tkinter.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='文件', menu=file_menu)
    file_menu.add_command(label='新增联系人', command=do_job)
    file_menu.add_command(label='编辑联系人', command=do_job)
    file_menu.add_separator()
    file_menu.add_command(label='退出', command=root.quit)
    help_menu = tkinter.Menu(file_menu, tearoff=0)
    menubar.add_cascade(label='帮助', menu=help_menu)
    help_menu.add_command(label='版本信息', command=show_version_info)
    return menubar


root = tkinter.Tk()
root.title('费用计算工具')
root.resizable(False, False)  # 让窗口不可以缩放
# root.iconbitmap('/home/zoulf/mycode/RateCalc/logo.ico')
size = utils.center_root(root, 600, 300)
root.geometry(size)
root.maxsize(600, 300)
root.minsize(300, 240)

# 展示菜单
menubar = display_menu(root)

# 下拉列表及新增按钮
remarks = []
select_list = tkinter.ttk.Combobox(root, width=30)
select_list["values"], remarks = get_contacts()
select_list.bind("<<ComboboxSelected>>", select_contact_by_name)
select_list.grid(row=0, column=1, pady=10, padx=5)
tkinter.Label(root, text='请选择联系人:').grid(row=0, column=0, pady=10, padx=10)
edit_button = tkinter.Button(root, text='编辑', command=add_contacts).grid(row=0, column=2, pady=10, padx=5)
add_button = tkinter.Button(root, text='新增', command=add_contacts).grid(row=0, column=3, pady=10, padx=5)

# 下划线
canvas = tkinter.Canvas(root, bg='black', height=1, width=600)
canvas.grid(row=1, column=0, columnspan=4, pady=10)

# 文件导入按钮
import_path = tkinter.StringVar()
output_path = tkinter.StringVar()
tkinter.Label(root, text="导入文件路径:").grid(row=2, column=0, pady=10)
tkinter.Entry(root, textvariable=import_path, width=50).grid(row=2, column=1, columnspan=2, pady=10)
tkinter.Button(root, text="路径选择", command=select_import_path).grid(row=2, column=3, pady=10)

tkinter.Label(root, text="输出文件夹路径:").grid(row=3, column=0, pady=10)
tkinter.Entry(root, textvariable=output_path, width=50).grid(row=3, column=1, columnspan=2, pady=10)
tkinter.Button(root, text="路径选择", command=select_output_path).grid(row=3, column=3, pady=10)

# 开始计算按钮
tkinter.Button(root, text="计算", command=calc, width=40).grid(row=4, column=0, columnspan=4, pady=20)

root.config(menu=menubar)
root.mainloop()
