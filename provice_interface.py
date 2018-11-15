import tkinter
import utils
import tkinter.messagebox
import model
import data_handle


def save_provice_info(master, data, custom_name):
    for provice, v in data.items():
        f_weight = float(v[0].get()) if v[0].get() else 0
        f_price = float(v[1].get()) if v[1].get() else 0
        n_price = float(v[2].get()) if v[2].get() else 0
        model.update_provice_info(
            custom_name=custom_name,
            provice_name=provice,
            f_num=f_weight,
            f_price=f_price,
            n_price=n_price
        )
    master.destroy()


def add_provice_info(custom_name):
    provice_root = tkinter.Toplevel()
    provice_root.title('编辑省份运费信息')
    provice_root.geometry(utils.center_root(provice_root, 400, 900))
    provices = ['长沙市', '湖南省', '北京市', '天津市', '上海市', '重庆市', '河北省', '山西省', '辽宁省', '吉林省', '黑龙江省', '江苏省', '浙江省', '安徽省',
                '福建省', '江西省', '山东省', '河南省', '湖北省', '广东省', '海南省', '四川省', '贵州省', '云南省', '陕西省', '甘肃省', '青海省', '内蒙古自治区',
                '广西壮族自治区', '西藏自治区', '宁夏回族自治区', '新疆维吾尔自治区']
    provice_dict = {}
    provice_info = data_handle.provice_dict_handle(custom_name)  # 返回值{'湖南':{'首重重量': 1.0 ...}}

    if not custom_name:
        tkinter.messagebox.showerror('错误', '请先填写客户名！')
        provice_root.destroy()
    else:
        model.insert_custom(custom_name)
        for provice in provices:
            if provice in provice_info:
                continue
            else:
                model.insert_provice_info(custom_name, provice, 0, 0, 0)

    provice_info = data_handle.provice_dict_handle(custom_name)

    tkinter.Label(provice_root, text='省份').grid(row=0, column=0)
    tkinter.Label(provice_root, text='首重重量(kg)').grid(row=0, column=1)
    tkinter.Label(provice_root, text='首重价格(元)').grid(row=0, column=2)
    tkinter.Label(provice_root, text='续重价格(元)').grid(row=0, column=3)
    for index, provice in enumerate(provices):
        # 设置值到输入框
        f_w_text = tkinter.StringVar()
        f_p_text = tkinter.StringVar()
        n_p_text = tkinter.StringVar()
        if provice in provice_info:
            f_w_text.set(provice_info[provice]['首重重量'])
            f_p_text.set(provice_info[provice]['首重价格'])
            n_p_text.set(provice_info[provice]['续重价格'])
        tmp = []
        tkinter.Label(provice_root, text=provice).grid(row=index + 1)
        f_weight = tkinter.Entry(provice_root, width=5, textvariable=f_w_text)
        f_weight.grid(row=index + 1, column=1)
        f_price = tkinter.Entry(provice_root, width=5, textvariable=f_p_text)
        f_price.grid(row=index + 1, column=2)
        n_price = tkinter.Entry(provice_root, width=5, textvariable=n_p_text)
        n_price.grid(row=index + 1, column=3)
        tmp.append(f_weight)
        tmp.append(f_price)
        tmp.append(n_price)
        provice_dict[provice] = tmp

    btn_save = tkinter.Button(provice_root, text='确定',
                              command=lambda: save_provice_info(provice_root, provice_dict, custom_name))
    btn_save.grid(row=len(provices) + 2, column=0)
    tkinter.Button(provice_root, text='取消', command=provice_root.destroy).grid(row=len(provices) + 2, column=1,
                                                                               columnspan=3, sticky=tkinter.E)
