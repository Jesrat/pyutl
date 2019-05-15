import cx_Oracle

APP_CTX_NAMESPACE = "USERENV"
APP_CTX_ENTRIES = [
    (APP_CTX_NAMESPACE, "MODULE", "modulo prueba"),
]


def dbmsoutput(cursor):
    """
    dbmsoutput must be enabled before execute statement
    cur.callproc("dbms_output.enable",(None,))
    """
    output = str()
    status = cursor.var(cx_Oracle.NUMBER)
    dbmsline = cursor.var(cx_Oracle.STRING)
    while True:
        cursor.callproc("dbms_output.get_line", (dbmsline, status))
        if status.getvalue():
            break
        output += f'{dbmsline.getvalue()} \n'

    return output


def cur_as_dict(cursor): 
    """
    needs a open cursor and returns all rows as dict, be careful
    with large results
    """
    columns = [cols[0] for cols in cursor.description]
    ret = [dict(zip(columns, row)) for row in cursor]
    return ret


class OraConn(cx_Oracle.Connection):
    # instance can return a cursor or the whole conn
    def __init__(self, str_conn, ret="conn", module_name=None):
        super().__init__(str_conn, encoding='UTF-8')
        self.cur = super().cursor()
        self.ret = ret
        if module_name is not None:
            self.cur.callproc('DBMS_APPLICATION_INFO.SET_MODULE', [module_name, None])

        if self.ret == "conn":
            self.cur.close()

    def __enter__(self):
        if self.ret == "cursor":
            return self.cur
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.ret == "cursor":
            return self.cur.close()
        super().__exit__(exc_type, exc_val, exc_tb)
