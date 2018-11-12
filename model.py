import sqlite3


# 初始化数据库
def init_db():
    INIT_CUSTOM = '''CREATE TABLE Custom (
              id  INTEGER PRIMARY KEY DEFAULT NULL,
              custom_name VARCHAR(50) NOT NULL,
              remark TEXT DEFAULT NULL
            );'''
    INIT_PROVICE_INFO = """
    CREATE TABLE Provice_info(
          id INTEGER PRIMARY KEY NOT NULL,
          custom INT NOT NULL,
          provice_name VARCHAR(20) NOT NULL,
          first_weight_num DECIMAL(10,2) NOT NULL,
          first_weight_price DECIMAL(10,2) NOT NULL,
          next_weight_price DECIMAL(10,2) NOT NULL,
          FOREIGN KEY (custom) REFERENCES Custom(id) on delete cascade 
    )
    """
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute(INIT_CUSTOM)
    cursor.execute(INIT_PROVICE_INFO)
    conn.commit()
    conn.close()


# sqlite3.OperationalError


def insert_custom(custom_name, remak=None):
    SQL = """
    INSERT INTO Custom (custom_name, remark) VALUES ('%s', '%s');
    """ % (custom_name, remak)
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute(SQL)
    conn.commit()
    conn.close()


def update_custom(custom_id, custom_name, remark=None):
    SQL = """
    UPDATE Custom SET custom_name='%s', remark='%s' WHERE id='%d'
    """ % (custom_name, remark, custom_id)
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute(SQL)
    conn.commit()
    conn.close()


def query_custom_by_name(custom_name):
    SQL = """
    SELECT id FROM Custom WHERE custom_name="%s"
    """ % (custom_name)
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute(SQL)
    custom_id = cursor.fetchone()
    conn.commit()
    conn.close()
    return custom_id


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


def insert_provice(custom_id, provice_name, f_num, f_price, n_prive):
    SQL = """
    INSERT INTO Provice_info (custom, provice_name, first_weight_num, first_weight_price, next_weight_price)
    VALUES ('%d', '%s', '%f', '%f', '%f');
    """ % (custom_id, provice_name, f_num, f_price, n_prive)
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute(SQL)
    conn.commit()
    conn.close()


def update_provice(id, provice_name, f_num, f_price, n_prive):
    SQL = """
    UPDATE Provice_info SET provice_name='%s', first_weight_num='%f', first_weight_price='%f', next_weight_price='%f'
    WHERE id='%d';
    """ % (provice_name, f_num, f_price, n_prive, id)
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute(SQL)
    conn.commit()
    conn.close()


def query_provice_info(custom_name):
    custom_id = query_custom_by_name(custom_name)
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


def delete(db_name, id):
    SQL = """
    DELETE FROM '%s' WHERE id='%d'
    """ % (db_name, id)
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    # SQLite在3.6.19版本中才开始支持外键约束，但是为了兼容以前的程序，
    # 默认并没有启用该功能，如果要启用该功能每次都要需要使用如下语句：PRAGMA foreign_keys = ON来打开。
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.execute(SQL)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    # init_db()
    # insert_custom('z')
    # # update_custom(1, '哈哈超市dsa', 'xx')
    # insert_provice(1, '湖南', 2, 2.5, 1.5)
    provice_info = query_provice_info('创发')
    provice_dict = {}
    for p in provice_info:
        tmp = {}
        provice, first_weight_num, first_weight_price, next_weight_price = p
        tmp['首重重量'] = first_weight_num
        tmp['首重价格'] = first_weight_price
        tmp['续重价格'] = next_weight_price
        provice_dict[provice] = tmp
    print(provice_dict)
