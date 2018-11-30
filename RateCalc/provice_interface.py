import model

from utils import center_root
from tkinter import Toplevel
from tkinter import Entry
from tkinter import Button
from tkinter import E
from tkinter import StringVar
from tkinter import Label
from tkinter.messagebox import showerror


def save_provice_info(master, data, custom_id):
    custom_detail = model.CustomDetail()
    for provice, v in data.items():
        f_weight = float(v[0].get()) if v[0].get() else 0
        f_price = float(v[1].get()) if v[1].get() else 0
        n_price = float(v[2].get()) if v[2].get() else 0
        custom_detail.update_custom_detail(
            custom_id=custom_id,
            provice_name=provice,
            f_num=f_weight,
            f_price=f_price,
            n_price=n_price
        )
    custom_detail.close()
    master.destroy()


def edit_provice_info(custom_name, btn_confirm):
    provice_root = Toplevel()
    if not custom_name:
        showerror('错误', '请先填写客户名！')
        provice_root.destroy()

    # 解除确认按钮不可编辑状态
    btn_confirm['state'] = 'normal'
    provice_root.title('编辑省份运费信息')
    if provice_root.winfo_screenheight() > 768:
        provice_root.geometry(center_root(provice_root, 400, 840))
    else:
        provice_root.geometry(center_root(provice_root, 1300, 200))
    provices = ['长沙市', '湖南省', '北京市', '天津市', '上海市', '重庆市', '河北省', '山西省', '辽宁省', '吉林省', '黑龙江省', '江苏省', '浙江省', '安徽省',
                '福建省', '江西省', '山东省', '河南省', '湖北省', '广东省', '海南省', '四川省', '贵州省', '云南省', '陕西省', '甘肃省', '青海省', '内蒙古自治区',
                '广西壮族自治区', '西藏自治区', '宁夏回族自治区', '新疆维吾尔自治区']
    provice_dict = {}

    custom = model.Custom()
    custom_detail = model.CustomDetail()
    custom_id = custom.find_custom(custom_name)
    provice_info = custom_detail.fetch_custom_detail(custom_id)
    print(custom_id)
    # 当为新建的联系人时，会自动新建联系人详细数据
    if custom_id == 0:
        custom_id = custom.add_custom(custom_name)
        for provice in provices:
            if provice in provice_info:
                continue
            else:
                custom_detail.add_custom_detail(custom_id, provice, 0, 0, 0)

    provice_info = custom_detail.fetch_custom_detail(custom_id)
    l1 = Label(provice_root, text='省份', font=('Helvetica', '9', 'normal'))
    l2 = Label(provice_root, text='首重重量(kg)', font=('Helvetica', '9', 'normal'))
    l3 = Label(provice_root, text='首重价格(元)', font=('Helvetica', '9', 'normal'))
    l4 = Label(provice_root, text='续重价格(元)', font=('Helvetica', '9', 'normal'))
    for index, provice in enumerate(provices):
        # 设置值到输入框
        f_w_text = StringVar()
        f_p_text = StringVar()
        n_p_text = StringVar()
        if provice in provice_info:
            f_w_text.set(provice_info[provice]['首重重量'])
            f_p_text.set(provice_info[provice]['首重价格'])
            n_p_text.set(provice_info[provice]['续重价格'])
        tmp = []
        provice_label = Label(provice_root, text=provice, font=('Helvetica', '9', 'normal'))
        f_weight = Entry(provice_root, width=5, textvariable=f_w_text, font=('Helvetica', '9', 'normal'))
        f_price = Entry(provice_root, width=5, textvariable=f_p_text, font=('Helvetica', '9', 'normal'))
        n_price = Entry(provice_root, width=5, textvariable=n_p_text, font=('Helvetica', '9', 'normal'))

        tmp.append(f_weight)
        tmp.append(f_price)
        tmp.append(n_price)
        provice_dict[provice] = tmp

        if provice_root.winfo_screenheight() > 768:
            provice_label.grid(row=index + 1)
            f_weight.grid(row=index + 1, column=1)
            f_price.grid(row=index + 1, column=2)
            n_price.grid(row=index + 1, column=3)
        else:
            provice_label.grid(row=0, column=index + 1)
            f_weight.grid(row=1, column=index + 1)
            f_price.grid(row=2, column=index + 1)
            n_price.grid(row=3, column=index + 1)

    btn_save = Button(provice_root, text='确定',
                              command=lambda: save_provice_info(provice_root, provice_dict, custom_id))
    btn_save.grid(row=len(provices) + 2, column=0)
    btn_cancel = Button(provice_root, text='取消', command=provice_root.destroy)
    if provice_root.winfo_screenheight() > 768:
        l1.grid(row=0, column=0)
        l2.grid(row=0, column=1)
        l3.grid(row=0, column=2)
        l4.grid(row=0, column=3)
        btn_save.grid(row=len(provices) + 2, column=0)
        btn_cancel.grid(row=len(provices) + 2, column=1, columnspan=3, sticky=E)
    else:
        l1.grid(row=0, column=0)
        l2.grid(row=1, column=0)
        l3.grid(row=2, column=0)
        l4.grid(row=3, column=0)
        btn_save.grid(row=4, column=0)
        btn_cancel.grid(row=4, column=1)

    custom.close()
    custom_detail.close()