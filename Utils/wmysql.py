import mysql.connector
import os
import logging
import time

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

        self.declare_table(
            "requests",[
                "rid SMALLINT AUTO_INCREMENT PRIMARY KEY NOT NULL",
                "uid SMALLINT",
                "item_id SMALLINT",
                "condn VARCHAR(20) NOT NULL",
                "last_executed INT UNSIGNED DEFAULT NULL",
                "frequency MEDIUMINT UNSIGNED NOT NULL",
                "expiry MEDIUMINT UNSIGNED NOT NULL"
            ]
        )

    def add_item(self,url=None,item=None):
        if not item:
            self.wsql.execute(f"INSERT INTO items(url) VALUES('{url}')")
        else:
            self.wsql.execute(f"UPDATE items SET name = '{item.name}',price = '{item.price}' WHERE url='{item.url}'")

    def update_item(self,item):
        self.wsql.execute(f"INSERT INTO items(price) VALUES('{item.price}') WHERE id = {item.item_id}")
    
    def add_request(self,request):
        self.wsql.execute(f'''INSERT INTO requests VALUES({request.rid},{request.uid},{request.item_id},'{request.condition}',{request.last_executed},
                            {request.frequency},{request.expiry})''')

    def update_request(self,rid,last_executed):
        self.wsql.execute(f"UPDATE requests SET last_executed = {last_executed} WHERE rid='{rid}'")

    def delete_request(self,rid):
        self.wsql.execute(f"DELETE FROM requests WHERE rid = {rid}")
    
    def get_todo(self):
        timestamp = str(int(time.time()))
        return self.wsql.execute(
            f"SELECT * FROM requests WHERE last_executed - {timestamp} > frequency"
        )