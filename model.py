import sqlite3


# 初始化数据库
def init_db():
    INIT_CUSTOM = '''CREATE TABLE Custom (
              id  INTEGER PRIMARY KEY DEFAULT NULL,
              custom_name VARCHAR(50) NOT NULL,
              remark TEXT DEFAULT NULL DEFAULT '无'
            );'''
    INIT_PROVICE_INFO = """
    CREATE TABLE Provice_info(
          id INTEGER PRIMARY KEY NOT NULL,
          custom INT NOT NULL,
          provice_name VARCHAR(20) NOT NULL,
          first_weight_num REAL,
          first_weight_price REAL,
          next_weight_price REAL,
          FOREIGN KEY (custom) REFERENCES Custom(id) on delete cascade 
    )
    """
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute(INIT_CUSTOM)
    cursor.execute(INIT_PROVICE_INFO)
    conn.commit()
    conn.close()


class Custom:
    def __init__(self):
        self.conn = sqlite3.connect('test.db')
        self.cur = self.conn.cursor()

    def add_custom(self, custom_name, remark='无'):
        """
        添加一条客户数据，加了去重检查，保证客户数据唯一性
        :param custom_name:
        :param remark:
        :return:
        """
        if self.find_custom(custom_name) > 0:
            raise Exception('你输入的用户名 {} 已存在！'.format(custom_name))
        SQL = """
        INSERT INTO Custom (custom_name, remark) VALUES (?, ?);
        """
        # 防止SQL注入攻击
        self.cur.execute(SQL, (custom_name, remark))
        self.conn.commit()
        custom_id = self.cur.lastrowid
        return custom_id

    def delete_custom(self, custom_id):
        SQL = """
        DELETE FROM Custom WHERE id=?
        """
        # SQLite在3.6.19版本中才开始支持外键约束，但是为了兼容以前的程序，
        # 默认并没有启用该功能，如果要启用该功能每次都要需要使用如下语句：PRAGMA foreign_keys = ON来打开。
        self.cur.execute("PRAGMA foreign_keys=ON")
        self.cur.execute(SQL, (custom_id,))
        self.conn.commit()

    def update_custom(self, custom_id, custom_name, remark='无'):
        SQL = """
        UPDATE Custom SET custom_name=?, remark=? WHERE id=?
        """
        self.cur.execute(SQL, (custom_name, remark, custom_id))
        self.conn.commit()

    def find_custom(self, custom_name):
        """
        通过客户名找到id
        :param custom_name:
        :return: id(int) / 0(没有该数据时)
        """
        SQL = """
        SELECT id FROM Custom WHERE custom_name=?
        """
        self.cur.execute(SQL, (custom_name,))
        custom_id = self.cur.fetchone()
        return custom_id[0] if custom_id else 0

    def find_custom_like(self, custom_name):
        """
        通过客户名找到id
        :param custom_name:
        :return: id(int) / 0(没有该数据时)
        """
        SQL = """
        SELECT id FROM Custom WHERE custom_name LIKE '%{}%'
        """.format(custom_name)
        self.cur.execute(SQL)
        custom_id = self.cur.fetchall()
        print(custom_id)
        if len(custom_id) > 1:
            raise Exception('客户名： {} 错误，请传入正确的客户名！'.format(custom_name))
        return custom_id[0][0] if custom_id else 0

    def fetch_custom(self):
        """
        返回所有custom对象
        :return: {'客户1': 'remark1', '客户2': 'remark2' ...}
        """
        SQL = """
        SELECT custom_name, remark FROM Custom
        """
        self.cur.execute(SQL)
        customs = self.cur.fetchall()
        data = {custom_name: remark for custom_name, remark in customs}
        return data

    def close(self):
        self.cur.close()
        self.conn.close()


class CustomDetail:
    def __init__(self):
        self.conn = sqlite3.connect('test.db')
        self.cur = self.conn.cursor()

    def add_custom_detail(self, custom_id, provice_name, f_num, f_price, n_price):
        if self.find_custom_detail(custom_id, provice_name) > 0:
            raise Exception('省份 {} 已存在'.format(provice_name))
        SQL = """
        INSERT INTO Provice_info (custom, provice_name, first_weight_num, first_weight_price, next_weight_price)
        VALUES (?, ?, ?, ?, ?);
        """
        self.cur.execute(SQL, (custom_id, provice_name, f_num, f_price, n_price))
        self.conn.commit()
        custom_detail_id = self.cur.lastrowid
        return custom_detail_id

    def update_custom_detail(self, custom_id, provice_name, f_num, f_price, n_price):
        SQL = """
        UPDATE Provice_info SET first_weight_num=?, first_weight_price=?, next_weight_price=?
        WHERE custom=? AND provice_name=?;
        """
        self.cur.execute(SQL, (f_num, f_price, n_price, custom_id, provice_name))
        self.conn.commit()

    def find_custom_detail(self, custom_id, provice_name):
        """
        找到明确的一条详情信息
        :param custom_id:
        :param provice_name:
        :return: id(int)
        """
        SQL = """
        SELECT id FROM Provice_info
        WHERE custom=? AND provice_name LIKE '%{}%';
        """.format(provice_name)
        self.cur.execute(SQL, (custom_id,))
        provice_id = self.cur.fetchall()
        if len(provice_id) > 1:
            raise Exception('目的省份 {} 错误！'.format(provice_name))
        return provice_id[0][0] if provice_id else 0

    def fetch_custom_detail(self, custom_id):
        """
        找到一个客户下的所有详情信息
        :param custom_id:
        :return: {'湖南': {'首重'重量: 1.0, ...}
        """
        SQL = """
        SELECT provice_name, first_weight_num, first_weight_price, next_weight_price FROM Provice_info
        WHERE custom=?;
        """
        self.cur.execute(SQL, (custom_id,))
        provice_info = self.cur.fetchall()
        provice_dict = {}
        for p in provice_info:
            tmp = {}
            provice, first_weight_num, first_weight_price, next_weight_price = p
            tmp['首重重量'] = first_weight_num
            tmp['首重价格'] = first_weight_price
            tmp['续重价格'] = next_weight_price
            provice_dict[provice] = tmp
        return provice_dict

    def close(self):
        self.cur.close()
        self.conn.close()


#
# def insert_custom(custom_name, remak=None):
#     if query_custom_id(custom_name):
#         return
#     SQL = """
#     INSERT INTO Custom (custom_name, remark) VALUES ('%s', '%s');
#     """ % (custom_name, remak)
#     conn = sqlite3.connect('test.db')
#     cursor = conn.cursor()
#     cursor.execute(SQL)
#     conn.commit()
#     conn.close()
#
#
# def update_custom(custom_name, remark=None):
#     custom_id = query_custom_id(custom_name)
#     if custom_id <= 0:
#         raise Exception('客户名不存在于数据库中！')
#     SQL = """
#     UPDATE Custom SET custom_name='%s', remark='%s' WHERE id='%d'
#     """ % (custom_name, remark, custom_id)
#     conn = sqlite3.connect('test.db')
#     cursor = conn.cursor()
#     cursor.execute(SQL)
#     conn.commit()
#     conn.close()
#
#
# def query_custom_id(custom_name):
#     SQL = """
#     SELECT id FROM Custom WHERE custom_name="%s"
#     """ % (custom_name)
#     conn = sqlite3.connect('test.db')
#     cursor = conn.cursor()
#     cursor.execute(SQL)
#     try:
#         custom_id = cursor.fetchone()[0]
#         conn.commit()
#         return custom_id
#     except TypeError:
#         return 0
#     finally:
#         conn.close()
#
#
# def query_all_custom():
#     SQL = """
#     SELECT custom_name, remark FROM Custom
#     """
#     conn = sqlite3.connect('test.db')
#     cursor = conn.cursor()
#     cursor.execute(SQL)
#     customs = cursor.fetchall()
#     conn.commit()
#     conn.close()
#     return customs
#
#
# def insert_provice_info(custom_name, provice_name, f_num, f_price, n_price):
#     custom_id = query_custom_id(custom_name)
#     SQL = """
#     INSERT INTO Provice_info (custom, provice_name, first_weight_num, first_weight_price, next_weight_price)
#     VALUES ('%d', '%s', '%f', '%f', '%f');
#     """ % (custom_id, provice_name, f_num, f_price, n_price)
#     conn = sqlite3.connect('test.db')
#     cursor = conn.cursor()
#     cursor.execute(SQL)
#     conn.commit()
#     conn.close()
#
#
# def update_provice_info(custom_name, provice_name, f_num, f_price, n_price):
#     custom_id = query_custom_id(custom_name)
#     SQL = """
#     UPDATE Provice_info SET first_weight_num='%f', first_weight_price='%f', next_weight_price='%f'
#     WHERE custom='%d' AND provice_name='%s';
#     """ % (f_num, f_price, n_price, custom_id, provice_name)
#     conn = sqlite3.connect('test.db')
#     cursor = conn.cursor()
#     cursor.execute(SQL)
#     conn.commit()
#     conn.close()
#
#
# def query_provice_info(custom_name):
#     custom_id = query_custom_id(custom_name)
#     SQL = """
#     SELECT provice_name, first_weight_num, first_weight_price, next_weight_price FROM Provice_info
#     WHERE custom='%d';
#     """ % (custom_id)
#     conn = sqlite3.connect('test.db')
#     cursor = conn.cursor()
#     cursor.execute(SQL)
#     provice_info = cursor.fetchall()
#     conn.commit()
#     conn.close()
#     return provice_info
#
#
# def delete_custom(custom_name):
#     SQL = """
#     DELETE FROM Custom WHERE custom_name='%s'
#     """ % (custom_name)
#     conn = sqlite3.connect('test.db')
#     cursor = conn.cursor()
#     # SQLite在3.6.19版本中才开始支持外键约束，但是为了兼容以前的程序，
#     # 默认并没有启用该功能，如果要启用该功能每次都要需要使用如下语句：PRAGMA foreign_keys = ON来打开。
#     cursor.execute("PRAGMA foreign_keys=ON")
#     cursor.execute(SQL)
#     conn.commit()
#     conn.close()
#
#
# def query_provice_id(custom_name, provice_name):
#     custom_id = query_custom_id(custom_name)
#     SQL = """
#     SELECT id FROM Provice_info
#     WHERE custom='%d' AND provice_name='%s';
#     """ % (custom_id, provice_name)
#     conn = sqlite3.connect('test.db')
#     cursor = conn.cursor()
#     cursor.execute(SQL)
#     provice_id = cursor.fetchone()
#     conn.commit()
#     conn.close()
#     return provice_id


if __name__ == '__main__':
    # custom_detail = CustomDetail()
    # print(custom_detail.find_custom_detail(1, '湖南'))
    #
    # custom_detail.close()
    custom = Custom()
    custom_id = custom.find_custom('客至')
    custom.delete_custom(custom_id)
    # custom_id = custom.find_custom('客')
    # print(custom_id)
