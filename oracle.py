import cx_Oracle


class OraConn:
    def __init__(self, str_conn, conn_name=None):
        self.conn = cx_Oracle.connect(str_conn, encoding='UTF-8')
        self.cur = self.conn.cursor()
        if conn_name is not None:
            self.cur.callproc('DBMS_APPLICATION_INFO.SET_MODULE', [conn_name, None])
        self.cur.close()

    def __enter__(self):
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
