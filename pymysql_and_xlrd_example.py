# coding=utf-8
import xlrd
import sys
import pymysql

from django.db.models import Q

from IPTVStopSystem import settings
from IPTVStopSystem.models import IPTVProgram
from IPTVStopSystem.models import IPTVCDNNode


reload(sys)
sys.setdefaultencoding('utf8')

SQL_FOR_CREATE_IPTVPROGRAME = 'INSERT INTO iptv_program (program_name, program_ip_type, program_ip ,status, platform)' \
                              ' VALUES (%s, %s, %s, %s, %s)'
SQL_FOR_CREATE_IPTVCDN = 'INSERT INTO iptv_cdn_node (city, ip, device_name, paltform, status) VALUES (%s, %s, %s, %s, %s)'
SQL_FOR_UPDATE_IPTVPROGRAM = 'UPDATE... '


class ExcelData:
    """
    使用Pymysql进行数据的上传处理，适合作为脚本单独使用
    """

    def __init__(self, file_name):
        self.conn = pymysql.connect(
            host=settings.DB_HSOT,
            user=settings.DB_USERNAME,
            passwd=settings.DB_PASSWD,
            db=settings.DB_NAME,
            port=3306,
            charset='utf8'
        )
        self.excel = xlrd.open_workbook(file_name)
        self.status = 2

    def program_insert(self):
        """
        根据iptvs.xlsx中的数据创建对应的数据
        TODO 增加条件判断，避免重复插入
        :return:
        """
        cur = self.conn.cursor()
        sheet_names = self.excel.sheet_names()  # [IPTV+ , IPTV]

        for sheet_name in sheet_names:
            sheet = self.excel.sheet_by_name(sheet_name)
            program_ip_type = sheet_name

            for row in range(sheet.nrows):
                program_name = sheet.cell(row, 0).value
                program_ip_for_zte = sheet.cell(row, 1).value

                # 因为可能有脏数据，所以需要做判空处理
                if not program_name:
                    continue

                if program_ip_type == 'IPTV':
                    values_for_zte = (program_name, program_ip_type, program_ip_for_zte, self.status, '旧版中兴')
                else:
                    values_for_zte = (program_name, program_ip_type, program_ip_for_zte, self.status, '中兴')
                cur.execute(SQL_FOR_CREATE_IPTVPROGRAME, values_for_zte)

                if program_ip_type == 'IPTV+':
                    program_ip_for_huawei = sheet.cell(row, 2).value
                    values_for_huawei = (program_name, program_ip_type, program_ip_for_huawei, self.status, '华为')
                    cur.execute(SQL_FOR_CREATE_IPTVPROGRAME, values_for_huawei)
        cur.close()
        self.conn.commit()

    # TODO 根据iptv_pro.xlsx中数据对频道进行分类
    def program_update(self):
        pass

    def cdn_insert(self):
        """
        根据cdns.xlsx的数据创建cdn表的数据
        TODO 加入条件判断，避免重复创建
        :return:
        """
        cur = self.conn.cursor()
        sheet_names = self.excel.sheet_names()
        for sheet_name in sheet_names:
            sheet = self.excel.sheet_by_name(sheet_name)
            platform = sheet_name
            is_range = False  # 华为与中兴与地区（岳阳，长沙...）的数据格式不一样，需要区分
            if sheet_name == u'华为IPTV+ CDN':
                is_range = True
            elif sheet_name == u'中兴IPTV+ CDN':
                is_range = True

            if is_range:
                for row in range(sheet.nrows):
                    city = sheet.cell(row, 0).value
                    ip = sheet.cell(row, 1).value
                    device_name = sheet.cell(row, 2).value
                    values = (city, ip, device_name, platform, self.status)
                    cur.execute(SQL_FOR_CREATE_IPTVCDN, values)
            else:
                for row in range(1, sheet.nrows):
                    city = platform[:-4]
                    ip = sheet.cell(row, 0).value
                    device_name = sheet.cell(row, 1).value
                    values = (city, ip, device_name, platform, self.status)
                    cur.execute(SQL_FOR_CREATE_IPTVCDN, values)
        self.conn.commit()

    def finish(self):
        self.conn.close()


class ExcelDataORM:
    """
    采用Django ORM映射进行数据处理，适合在Django框架中使用
    """

    def __init__(self):
        self.status = 2

    def program_insert(self, file_path):
        """
        根据iptvs.xlsx中的数据创建对应的数据
        """
        excel = xlrd.open_workbook(file_path)
        sheet_names = excel.sheet_names()  # [IPTV+ , IPTV]
        for sheet_name in sheet_names:
            sheet = excel.sheet_by_name(sheet_name)
            program_ip_type = sheet_name

            for row in range(sheet.nrows):
                program_name = sheet.cell(row, 0).value.strip()
                program_ip_for_zte = sheet.cell(row, 1).value.strip()

                # 避免重复插入
                if program_name:
                    if IPTVProgram.objects.filter(program_name=program_name, program_ip_type=program_ip_type):
                        continue
                else:
                    continue

                try:
                    program_ip_for_huawei = sheet.cell(row, 2).value
                except IndexError:
                    continue
                else:
                    IPTVProgram.objects.create(
                        program_name=program_name,
                        program_ip_type=program_ip_type,
                        program_ip=program_ip_for_huawei,
                        platform='华为',
                        status=self.status
                    )
                finally:
                    IPTVProgram.objects.create(
                        program_name=program_name,
                        program_ip_type=program_ip_type,
                        program_ip=program_ip_for_zte,
                        platform='中兴' if program_ip_type == 'IPTV+' else '旧版中兴',
                        status=self.status
                    )

    def program_update(self, file_path):
        """
        根据iptv_pro.xlsx中的数据做相应的频道类型修整
        """
        excel = xlrd.open_workbook(file_path)
        sheets = excel.sheets()
        # 先按照名字初略更新一波
        IPTVProgram.objects.filter(Q(program_name__contains='卫视')).update(program_type='卫视')
        IPTVProgram.objects.filter(Q(program_name__contains='CCTV')).update(program_type='央视')
        IPTVProgram.objects.filter(Q(program_name__contains='湖南') |
                                   Q(program_name__contains='芒果') |
                                   Q(program_name__contains='潇湘') |
                                   Q(program_name__contains='长沙')).update(program_type='省内')
        IPTVProgram.objects.filter(Q(program_name__contains='高清') | Q(program_name__contains='HD')).update(program_type='高清')
        IPTVProgram.objects.filter(Q(program_name__contains='超清') | Q(program_name__contains='4K')).update(program_type='4K')

        for sheet in sheets:
            programs = IPTVProgram.objects.filter(program_type=None)  # 获取未分类的频道
            for row in range(1, sheet.nrows):
                try:
                    for col in range(1, 14, 2):
                        program_name = sheet.cell(row, col).value.strip()
                        program_type = sheet.cell(0, col).value.strip()
                        programs.filter(program_name=program_name).update(program_type=program_type)
                except IndexError:
                    continue

        IPTVProgram.objects.filter(program_type=None).update(program_type='其他')

    def cdn_insert(self, file_path):
        """
        根据cdns.xlsx的数据创建cdn表的数据
        :return:
        """
        excel = xlrd.open_workbook(file_path)
        sheet_names = excel.sheet_names()
        for sheet_name in sheet_names:
            sheet = excel.sheet_by_name(sheet_name)
            is_huawei_or_zte = False  # 华为与中兴与地区（岳阳，长沙...）的数据格式不一样，需要区分
            if sheet_name == u'华为IPTV+ CDN' or sheet_name == u'中兴IPTV+ CDN':
                is_huawei_or_zte = True

            for row in range(1, sheet.nrows):
                city = sheet.cell(row, 0).value if is_huawei_or_zte else sheet_name.replace('IPTV', '')
                ip = sheet.cell(row, 1).value if is_huawei_or_zte else sheet.cell(row, 0).value
                device_name = sheet.cell(row, 2).value if is_huawei_or_zte else sheet.cell(row, 1).value

                # 避免重复插入与脏数据
                if ip:
                    if IPTVCDNNode.objects.filter(ip=ip, device_name=device_name, city=city):
                        continue
                else:
                    continue

                IPTVCDNNode.objects.create(
                    ip=ip,
                    city=city,
                    device_name=device_name,
                    paltform=sheet_name,
                    status=self.status
                )
