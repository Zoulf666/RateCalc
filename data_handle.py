import math
import xlrd
import xlwt

from xlutils.copy import copy as xl_copy
import model


def calc_price(weight, first_weight_num, first_weight_price, next_weight_price):
    weight = math.ceil(weight)  # 向上取整
    if weight <= first_weight_num:
        price = first_weight_price
    else:
        remain = math.ceil(weight - first_weight_num)
        remain_price = remain * next_weight_price
        price = first_weight_price + remain_price
    return price


def provice_dict_handle(custom_name):
    provice_info = model.query_provice_info(custom_name)
    provice_dict = {}
    for p in provice_info:
        tmp = {}
        provice, first_weight_num, first_weight_price, next_weight_price = p
        tmp['首重重量'] = first_weight_num
        tmp['首重价格'] = first_weight_price
        tmp['续重价格'] = next_weight_price
        provice_dict[provice] = tmp
    return provice_dict


def excel_handle(file_path, custom_name):
    # TODO 异常处理，sheet为空异常
    # formatting_info=True确保打开原文件时保留原格式
    excel = xlrd.open_workbook(file_path)
    new_excel = xl_copy(excel)
    new_sheet = new_excel.get_sheet(0)
    print(type(new_sheet))
    print(new_sheet)

    sheet_names = excel.sheet_names()
    # provice_dict = provice_dict_handle(custom_name)
    for sheet_name in sheet_names:
        sheet = excel.sheet_by_name(sheet_name)
        # weight_tr_name = sheet.cell(0, 2).value
        # provice_tr_name = sheet.cell(0, 3).value
        # if weight_tr_name != '重量' or weight_tr_name != '重量（kg）':
        #     raise Exception('请检查位置（1, C）名称是否为重量或重量（kg）！')
        # if provice_tr_name != '目的省份' or provice_tr_name != '目的地省份':
        #     raise Exception('请检查位置（1, D）名称是否为目的省份！')
        # for row in range(1, sheet.nrows):
        #     weight = sheet.cell(row, 2)
        #     provice = sheet.cell(row, 3)
        #     # TODO 异常处理，键异常
        #     if provice in provice_dict:
        #         first_weight_num = provice_dict[provice]['首重重量']
        #         first_weight_price = provice_dict[provice]['首重价格']
        #         next_weight_price = provice_dict[provice]['续重价格']
        #     else:
        #         raise KeyError('请检查文件中的省份名是否正确，位置({}, {})'.format(row+1, 3+1))
        #     price = calc_price(weight, first_weight_num, first_weight_price, next_weight_price)

if __name__ == '__main__':
    excel_handle('9月消防张10.18日发送.xlsx', 'xx')