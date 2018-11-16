import math
import openpyxl
import model


def calc_price(weight, first_weight_num, first_weight_price, next_weight_price):
    weight = math.ceil(weight)  # 向上取整
    if weight <= first_weight_num:
        price = first_weight_price
    else:
        remain = math.ceil(weight - first_weight_num)
        remain_price = remain * next_weight_price
        price = first_weight_price + remain_price
    return float(price)


# def provice_dict_handle(custom_name):
#     """
#     :param custom_name:
#     :return: {'湖南':{'首重重量': 1.0 ...}}
#     """
#     custom = model.Custom()
#     custom_detail = model.CustomDetail()
#     custom_id = custom.find_custom(custom_name)
#     provice_info = custom_detail.fetch_custom_detail(custom_id)
#     custom.close()
#     custom_detail.close()
#     provice_dict = {}
#     for p in provice_info:
#         tmp = {}
#         provice, first_weight_num, first_weight_price, next_weight_price = p
#         tmp['首重重量'] = first_weight_num
#         tmp['首重价格'] = first_weight_price
#         tmp['续重价格'] = next_weight_price
#         provice_dict[provice] = tmp
#     return provice_dict


# def excel_handle(import_path, export_path, custom_name):
#     # TODO 异常处理，sheet为空异常
#     import_excel = xlrd.open_workbook(import_path)
#     output_excel = xlsxwriter.Workbook(export_path)
#
#     sheet_names = import_excel.sheet_names()
#     provice_dict = provice_dict_handle(custom_name)
#     for sheet_name in sheet_names:
#         import_sheet = import_excel.sheet_by_name(sheet_name)
#         output_sheet = output_excel.add_worksheet(sheet_name)
#         nrows = import_sheet.nrows
#         ncols = import_sheet.ncols
#         output_sheet.set_column(0, ncols, 22)  # 设定列的宽度为22像素
#         # weight_tr_name = sheet.cell(0, 2).value
#         # provice_tr_name = sheet.cell(0, 3).value
#         # if weight_tr_name != '重量' or weight_tr_name != '重量（kg）':
#         #     raise Exception('请检查位置（1, C）名称是否为重量或重量（kg）！')
#         # if provice_tr_name != '目的省份' or provice_tr_name != '目的地省份':
#         #     raise Exception('请检查位置（1, D）名称是否为目的省份！')
#
#         for row in range(sheet.nrows):
#             output_sheet.set_row(row, 22)  # 设定第i行单元格属性，高度为22像素，行索引从0开始
#
#             weight = sheet.cell(row, 2)
#             provice = sheet.cell(row, 3)
#             # TODO 异常处理，键异常
#             if provice in provice_dict:
#                 first_weight_num = provice_dict[provice]['首重重量']
#                 first_weight_price = provice_dict[provice]['首重价格']
#                 next_weight_price = provice_dict[provice]['续重价格']
#             else:
#                 raise KeyError('请检查文件中的省份名是否正确，位置({}, {})'.format(row + 1, 3 + 1))
#             price = calc_price(weight, first_weight_num, first_weight_price, next_weight_price)


# def provice_dict_handle(custom_name):
#     """
#     根据用户名提供该用户的全部详细资料
#     :param custom_name:
#     :return:
#     """
#     custom = model.Custom()
#     custom_detail = model.CustomDetail()
#     custom_id = custom.find_custom(custom_name)
#     provice_dict = custom_detail.fetch_custom_detail(custom_id)
#     return provice_dict


def excel_handle(path, custom_name):
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


def excel_provice_handle(path, progress):
    progress.start(10)
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

    progress.stop()

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
    excel_provice_handle('长大价格表.xlsx')


def progress(master):
    frame = tkinter.Frame(master).grid(row=5, column=0, columnspan=5)  # 使用时将框架根据情况选择新的位置
    canvas = tkinter.Canvas(frame, width=150, height=30)
    canvas.grid(row=5, column=0, columnspan=4, sticky=tkinter.E)
    progress_num = tkinter.StringVar()
    out_rec = canvas.create_rectangle(5, 5, 105, 25, outline="blue", width=0)
    fill_rec = canvas.create_rectangle(5, 5, 5, 25, outline="", width=0, fill="blue")
    tkinter.Label(frame, textvariable=progress_num).grid(row=5, column=4, sticky=tkinter.W)