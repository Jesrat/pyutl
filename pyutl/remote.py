import paramiko


class RemoteSSH:
    def __init__(self, auth_info):
        if not isinstance(auth_info, tuple) or len(auth_info) != 4:
            raise AssertionError(f'expected tuple (host, port, user, password) instead got {auth_info}')

        self.host = auth_info[0]
        self.port = auth_info[1]
        self.user = auth_info[2]
        self.pssw = auth_info[3]
        self.sock = paramiko.Transport((self.host, self.port))
        self.sock.connect(username=self.user, password=self.pssw)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sock.close()


class RemoteExecute(RemoteSSH):
    def __init__(self, auth_info):
        super().__init__(auth_info)
        self.session = self.sock.open_channel(kind='session')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        super().__exit__(exc_type, exc_val, exc_tb)

    def execute(self, command):
        stdout = b''
        self.session.exec_command(command)
        while True:
            stdout += self.session.recv(4096)
            if self.session.exit_status_ready():
                break
        return stdout


class Sftp(RemoteSSH):
    def __init__(self, auth_info):
        super().__init__(auth_info)
        self.sftp = paramiko.SFTPClient.from_transport(self.sock)

    def __enter__(self):
        return self.sftp

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sftp.close()
        super().__exit__(exc_type, exc_val, exc_tb)
