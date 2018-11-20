import math
import openpyxl
import model
import time


def calc_price(weight, first_weight_num, first_weight_price, next_weight_price):
    weight = math.ceil(weight)  # 向上取整
    if weight <= first_weight_num:
        price = first_weight_price
    else:
        remain = math.ceil(weight - first_weight_num)
        remain_price = remain * next_weight_price
        price = first_weight_price + remain_price
    return float(price)


def excel_handle(path):
    start = time.time()
    # 注：openpyxl 下标从1开始
    wb = openpyxl.load_workbook(path)
    sheets = wb.worksheets
    custom = model.Custom()
    custom_detail = model.CustomDetail()
    for sheet in sheets:
        price_col = sheet.max_column - 1
        price_sum_col = sheet.max_column
        max_row = sheet.max_row
        sum_price = 0

        if max_row <= 1:
            continue

        if not sheet.cell(row=1, column=price_sum_col).value == '运费总数':
            price_col = sheet.max_column + 1
            price_sum_col = price_col + 1
            sheet.cell(row=1, column=price_col).value = '运费'
            sheet.cell(row=1, column=price_sum_col).value = '运费总数'

        # 姓名集合（集合特性去重）
        custom_names = set(v.value for index, v in enumerate(sheet['M']) if not index == 0)
        """
        provice_dict字典格式：{
                                    '张三': {
                                                '湖南': {
                                                                '首重重量': 1.0,
                                                                ...                                            
                                                           }
                                                '湖北': ...
                                                }
                                    '李四': ...
                             }
        """
        name_dict = {}
        for custom_name in custom_names:
            custom_id = custom.find_custom_like(custom_name)
            # 没找到指定用户（custom_id=0）抛出异常
            if not custom_id:
                raise Exception('用户名: {} 未录入数据库中！'.format(custom_name))
            name_dict[custom_name] = custom_detail.fetch_custom_detail(custom_id)
        print(name_dict)

        # 从第2行开始为数据
        for row in range(2, max_row + 1):
            weight = sheet.cell(row=row, column=3).value
            provice = sheet.cell(row=row, column=4).value
            name = sheet.cell(row=row, column=13).value
            if provice in name_dict[name]:
                can_calc = True
            elif custom_detail.find_custom_detail(custom.find_custom_like(name), provice):
                can_calc = True
            else:
                can_calc = False

            if can_calc:
                first_weight_num = name_dict[name][provice]['首重重量']
                first_weight_price = name_dict[name][provice]['首重价格']
                next_weight_price = name_dict[name][provice]['续重价格']
                price = calc_price(weight, first_weight_num, first_weight_price, next_weight_price)
                sum_price += price
                sheet.cell(row=row, column=price_col).value = price
            else:
                raise Exception('位置({}, {})目的省份{}未录入数据库中！'.format(row, 'D', provice))

        # 写入总金额
        sheet.cell(2, price_sum_col).value = float(sum_price)

    wb.save(path)
    custom.close()
    custom_detail.close()
    end = time.time()
    print('耗时: {}'.format(end - start))


def excel_handle2(path, custom_name):
    start = time.time()
    # 注：openpyxl 下标从1开始
    wb = openpyxl.load_workbook(path)
    sheets = wb.worksheets
    custom = model.Custom()
    custom_detail = model.CustomDetail()
    custom_id = custom.find_custom(custom_name)
    provice_dict = custom_detail.fetch_custom_detail(custom_id)
    for sheet in sheets:
        price_col = sheet.max_column - 1
        price_sum_col = sheet.max_column
        max_row = sheet.max_row
        sum_price = 0

        if max_row <= 1:
            continue

        if not sheet.cell(row=1, column=price_sum_col).value == '运费总数':
            price_col = sheet.max_column + 1
            price_sum_col = price_col + 1
            sheet.cell(row=1, column=price_col).value = '运费'
            sheet.cell(row=1, column=price_sum_col).value = '运费总数'

        # 从第2行开始为数据
        for row in range(2, max_row + 1):
            weight = sheet.cell(row=row, column=3).value
            provice = sheet.cell(row=row, column=4).value
            if provice in provice_dict:
                first_weight_num = provice_dict[provice]['首重重量']
                first_weight_price = provice_dict[provice]['首重价格']
                next_weight_price = provice_dict[provice]['续重价格']
                price = calc_price(weight, first_weight_num, first_weight_price, next_weight_price)
                sum_price += price
                sheet.cell(row=row, column=price_col).value = price

        # 写入总金额
        sheet.cell(2, price_sum_col).value = float(sum_price)

    wb.save(path)
    end = time.time()
    print('耗时: {}'.format(end - start))


def excel_provice_handle(path):
    wb = openpyxl.load_workbook(path)
    sheetnames = wb.sheetnames

    custom = model.Custom()
    custom_detail = model.CustomDetail()
    for name in sheetnames:
        # 判断客户是否存在，不存在创建
        custom_id = custom.find_custom(name)
        if custom_id == 0:
            custom_id = custom.add_custom(name)
        sheet = wb[name]
        for row in range(2, sheet.max_row + 1):
            provice = sheet.cell(row=row, column=1).value
            # 因为可能把空的单元格算进去，所以需要判断
            if not provice:
                continue
            f_num = float(sheet.cell(row=row, column=2).value)
            f_price = float(sheet.cell(row=row, column=3).value)
            n_price = float(sheet.cell(row=row, column=4).value)

            if custom_detail.find_custom_detail(custom_id, provice):
                custom_detail.update_custom_detail(custom_id, provice, f_num, f_price, n_price)
            else:
                custom_detail.add_custom_detail(custom_id, provice, f_num, f_price, n_price)
    custom.close()
    custom_detail.close()


if __name__ == '__main__':
    # excel_handle('9月消防张10.18日发送.xlsx', '创发')

    # wb = xw.Book()  # 这句创建一个新的工作薄
    # wb = xw.Book('9月消防张10.18日发送.xlsx')  # 连接到当前工作目录中的现有文件
    # wb = xw.Book(r'C:\path\to\file.xlsx')  # 在Windows上:使用原始字符r来避免反斜转义
    # app = xw.App(visible=True, add_book=False)
    # app.display_alerts = False
    # app.screen_updating = False
    # wb = app.books.open('9月消防张10.18日发送.xlsx')
    # wb.save()
    # wb.close()
    # app.quit()
    # print(provice_dict_handle('tesx'))
    excel_provice_handle('客户表.xlsx')

# def progress(master):
#     frame = tkinter.Frame(master).grid(row=5, column=0, columnspan=5)  # 使用时将框架根据情况选择新的位置
#     canvas = tkinter.Canvas(frame, width=150, height=30)
#     canvas.grid(row=5, column=0, columnspan=4, sticky=tkinter.E)
#     progress_num = tkinter.StringVar()
#     out_rec = canvas.create_rectangle(5, 5, 105, 25, outline="blue", width=0)
#     fill_rec = canvas.create_rectangle(5, 5, 5, 25, outline="", width=0, fill="blue")
#     tkinter.Label(frame, textvariable=progress_num).grid(row=5, column=4, sticky=tkinter.W)
