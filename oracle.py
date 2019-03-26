import cx_Oracle

APP_CTX_NAMESPACE = "USERENV"
APP_CTX_ENTRIES = [
    ( APP_CTX_NAMESPACE, "MODULE", "modulo prueba"),
]


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
