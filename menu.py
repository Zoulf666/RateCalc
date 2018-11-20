import tkinter
import tkinter.messagebox
import contact_interface
import model
import utils


def display_menu(master, select_list):
    menubar = tkinter.Menu(master)
    file_menu = tkinter.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='文件', menu=file_menu)
    file_menu.add_command(label='新增联系人', command=lambda: contact_interface.add_contacts(select_list))
    file_menu.add_command(label='编辑联系人', command=lambda: contact_interface.edit_contacts(select_list))
    file_menu.add_command(label='删除联系人', command=lambda: delete_custom_interface(select_list))
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


def delete_custom_interface(select_list):
    root = tkinter.Toplevel()
    root.title('删除联系人')
    root.geometry(utils.center_root(root, 200, 100))

    ety_name = tkinter.Entry(root)
    btn_confirm = tkinter.Button(root, text='确认', command=lambda: delete_custom(root, ety_name.get(), select_list))
    btn_cancel = tkinter.Button(root, text='取消', command=root.destroy)

    ety_name.grid(columnspan=2, pady=10, padx=10)
    btn_confirm.grid(row=1, sticky=tkinter.W)
    btn_cancel.grid(row=1, column=1, sticky=tkinter.E)


def delete_custom(master, name, widget):
    try:
        custom = model.Custom()
        custom_id = custom.find_custom(name)
        if custom_id == 0:
            raise Exception('用户名：{} 未录入数据库！'.format(name))
        custom.delete_custom(custom_id)
        widget['values'] = list(custom.fetch_custom().keys())
        custom.close()
        master.destroy()
        tkinter.messagebox.showinfo(message='删除{}成功'.format(name))
    except Exception as e:
        print(e)
        tkinter.messagebox.showerror('错误', e)
