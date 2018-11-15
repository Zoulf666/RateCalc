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


def insert_custom(custom_name, remak=None):
    if query_custom_id(custom_name):
        return
    SQL = """
    INSERT INTO Custom (custom_name, remark) VALUES ('%s', '%s');
    """ % (custom_name, remak)
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute(SQL)
    conn.commit()
    conn.close()


def update_custom(custom_name, remark=None):
    custom_id = query_custom_id(custom_name)
    if custom_id <= 0:
        raise Exception('客户名不存在于数据库中！')
    SQL = """
    UPDATE Custom SET custom_name='%s', remark='%s' WHERE id='%d'
    """ % (custom_name, remark, custom_id)
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute(SQL)
    conn.commit()
    conn.close()


def query_custom_id(custom_name):
    SQL = """
    SELECT id FROM Custom WHERE custom_name="%s"
    """ % (custom_name)
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute(SQL)
    try:
        custom_id = cursor.fetchone()[0]
        conn.commit()
        return custom_id
    except TypeError:
        return 0
    finally:
        conn.close()


def query_all_custom():
    SQL = """
    SELECT custom_name, remark FROM Custom
    """
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute(SQL)
    customs = cursor.fetchall()
    conn.commit()
    conn.close()
    return customs


def insert_provice_info(custom_name, provice_name, f_num, f_price, n_price):
    custom_id = query_custom_id(custom_name)
    SQL = """
    INSERT INTO Provice_info (custom, provice_name, first_weight_num, first_weight_price, next_weight_price)
    VALUES ('%d', '%s', '%f', '%f', '%f');
    """ % (custom_id, provice_name, f_num, f_price, n_price)
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute(SQL)
    conn.commit()
    conn.close()


def update_provice_info(custom_name, provice_name, f_num, f_price, n_price):
    custom_id = query_custom_id(custom_name)
    SQL = """
    UPDATE Provice_info SET first_weight_num='%f', first_weight_price='%f', next_weight_price='%f'
    WHERE custom='%d' AND provice_name='%s';
    """ % (f_num, f_price, n_price, custom_id, provice_name)
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute(SQL)
    conn.commit()
    conn.close()


def query_provice_info(custom_name):
    custom_id = query_custom_id(custom_name)
    SQL = """
    SELECT provice_name, first_weight_num, first_weight_price, next_weight_price FROM Provice_info
    WHERE custom='%d';
    """ % (custom_id)
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute(SQL)
    provice_info = cursor.fetchall()
    conn.commit()
    conn.close()
    return provice_info


def delete_custom(custom_name):
    SQL = """
    DELETE FROM Custom WHERE custom_name='%s'
    """ % (custom_name)
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    # SQLite在3.6.19版本中才开始支持外键约束，但是为了兼容以前的程序，
    # 默认并没有启用该功能，如果要启用该功能每次都要需要使用如下语句：PRAGMA foreign_keys = ON来打开。
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.execute(SQL)
    conn.commit()
    conn.close()


def query_provice_id(custom_name, provice_name):
    custom_id = query_custom_id(custom_name)
    SQL = """
    SELECT id FROM Provice_info
    WHERE custom='%d' AND provice_name='%s';
    """ % (custom_id, provice_name)
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute(SQL)
    provice_id = cursor.fetchone()
    conn.commit()
    conn.close()
    return provice_id


if __name__ == '__main__':
    # init_db()
    # insert_custom('z')
    # # update_custom(1, '哈哈超市dsa', 'xx')
    # insert_provice(1, '湖南', 2, 2.5, 1.5)
    # provice_info = query_provice_info('创发')
    # provice_dict = {}
    # for p in provice_info:
    #     tmp = {}
    #     provice, first_weight_num, first_weight_price, next_weight_price = p
    #     tmp['首重重量'] = first_weight_num
    #     tmp['首重价格'] = first_weight_price
    #     tmp['续重价格'] = next_weight_price
    #     provice_dict[provice] = tmp
    # print(provice_dict)
    pass
