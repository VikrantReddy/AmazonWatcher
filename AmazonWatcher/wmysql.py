import mysql.connector
import os
import logging

class wmysql():
    def __init__(self, host=None, **kwargs):
        self.mydb = mysql.connector.connect(
            **kwargs,
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci',
            use_unicode=True,
            auth_plugin='mysql_native_password')

    def execute_tuple(self, sql, args):
        logging.info("Executing SQL: " + sql)
        self.mydb.start_transaction()
        c = self.mydb.cursor()
        c.execute(sql, args)
        res = c.fetchall() if self.mydb.unread_result else []
        self.mydb.commit()
        c.close()
        return res

    def execute_many(self, sql, args_list):
        logging.info("Executing many SQL: " + sql)
        self.mydb.start_transaction()
        c = self.mydb.cursor()
        c.executemany(sql, args_list)
        res = c.fetchall() if self.mydb.unread_result else []
        self.mydb.commit()
        c.close()
        return res

    def execute(self, sql, *args):
        return self.execute_tuple(sql, args)


class sql_queries:
    wsql = None

    def __init__(self):
        self.wsql = wmysql(host='127.0.0.1', user=os.environ.get("AMAZONWATCHER_DATABASE_USER"), passwd=os.environ.get("AMAZONWATCHER_DATABASE_PASSWORD"), database=os.environ.get("AMAZONWATCHER_DATABASE"))

        self.setup_tables()

    def declare_table(self, table_name, cols_list, extra_decl = []):
        tmp_name = "schtmp_" + table_name
        args_str = ', '.join(cols_list + extra_decl)

        rtable_sql = "CREATE TABLE IF NOT EXISTS {} ({}) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci".format(table_name, args_str)
        self.wsql.execute(rtable_sql)

    def setup_tables(self):
        self.declare_table(
            "items", [
                "item_id SMALLINT AUTO_INCREMENT PRIMARY KEY NOT NULL",
                "name VARCHAR(100)",
                "url VARCHAR(100) NOT NULL",
                "price MEDIUMINT"
            ]
        )
    def add_item(self,url=None,item=None):
        if not item:
            self.wsql.execute(f"INSERT INTO items(url) VALUES('{url}')")
        else:
            self.wsql.execute(f"UPDATE items SET name = '{item.name}',price = '{item.price}' WHERE item_id={item.item_id}")

    def update_item(self,item):
        self.wsql.execute(f"INSERT INTO items(price) VALUES('{item.price}') WHERE id = {item.item_id}")