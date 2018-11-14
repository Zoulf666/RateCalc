import tkinter
import utils
import tkinter.messagebox
import model


# TODO 浮点数验证
def save_provice_info(data, custom_name):
    for provice, v in data.items():
        f_weight = float(v[0].get())
        f_price = float(v[1].get())
        n_price = float(v[2].get())
        model.insert_provice_info(
            custom_name=custom_name,
            provice_name=provice,
            f_num=f_weight,
            f_price=f_price,
            n_price=n_price
        )

def add_provice_info(custom_name):
    provice_root = tkinter.Toplevel()
    provice_root.title('编辑省份运费信息')
    provice_root.geometry(utils.center_root(provice_root, 400, 900))
    provices = ['北京市', '天津市', '上海市', '重庆市', '河北省', '山西省', '辽宁省', '吉林省', '黑龙江省', '江苏省', '浙江省', '安徽省', '福建省', '江西省',
                '山东省', '河南省', '湖北省', '湖南省', '广东省', '海南省', '四川省', '贵州省', '云南省', '陕西省', '甘肃省', '青海省', '内蒙古自治区',
                '广西壮族自治区', '西藏自治区', '宁夏回族自治区', '新疆维吾尔自治区']
    provice_dict = {}
    tkinter.Label(provice_root, text='省份').grid(row=0, column=0)
    tkinter.Label(provice_root, text='首重重量(kg)').grid(row=0, column=1)
    tkinter.Label(provice_root, text='首重价格(元)').grid(row=0, column=2)
    tkinter.Label(provice_root, text='首重价格(元)').grid(row=0, column=3)
    for index, provice in enumerate(provices):
        tmp = []
        tkinter.Label(provice_root, text=provice).grid(row=index + 1)
        f_weight = tkinter.Entry(provice_root, width=5)
        f_weight.grid(row=index + 1, column=1)
        f_price = tkinter.Entry(provice_root, width=5)
        f_price.grid(row=index + 1, column=2)
        n_price = tkinter.Entry(provice_root, width=5)
        n_price.grid(row=index + 1, column=3)
        tmp.append(f_weight)
        tmp.append(f_price)
        tmp.append(n_price)
        provice_dict[provice] = tmp
    btn_save = tkinter.Button(provice_root, text='确定',
                              command=lambda: save_provice_info(provice_dict, custom_name)).grid(row=len(provices) + 2,
                                                                                               column=0)
    tkinter.Button(provice_root, text='取消', command=provice_root.destroy).grid(row=len(provices) + 2, column=1,
                                                                               columnspan=3, sticky=tkinter.E)
    if not custom_name:
        tkinter.messagebox.showerror('错误', '请先完善客户资料！')
        provice_root.destroy()
    else:
        model.insert_custom(custom_name)
