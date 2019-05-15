import smtplib
from os.path import basename
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


class SendMail:
    def __init__(self, auth_info):
        if not isinstance(auth_info, tuple) or len(auth_info) != 4:
            raise AssertionError(f'expected tuple (host, port, user, password) instead got {auth_info}')

        self.host = auth_info[0]
        self.port = auth_info[1]
        self.user = auth_info[2]
        self.pssw = auth_info[3]
        self.conn = None
        self.msg = None

    def __enter__(self):
        self.open_conn()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def open_conn(self):
        if int(self.port) == 465:
            self.conn = smtplib.SMTP_SSL(self.host, 465)
        else:
            self.conn = smtplib.SMTP(self.host, self.port)
            self.conn.starttls()
        self.conn.login(self.user, self.pssw)

    def content(self, from_address, to_address, subject, msg):
        if not isinstance(to_address, list):
            raise AssertionError('destination address should be a list []')
        self.msg = MIMEMultipart()
        self.msg['Subject'] = subject
        self.msg['From'] = from_address
        self.msg['To'] = COMMASPACE.join(to_address)
        self.msg.attach(MIMEText(msg, 'html'))

    def attach(self, files):
        if not isinstance(files, list):
            raise AssertionError('file(s) to attach should be a list []')

        for file in files:
            filename = basename(file)
            with open(file, "rb") as f:
                fl = MIMEApplication(f.read(), Name=filename)
            fl['Content-Disposition'] = f'attachment; filename="{filename}"'
            self.msg.attach(fl)

        print(self.msg)

    def send(self):
        if self.msg is None:
            raise Exception('msg is not defined')
        self.conn.send_message(self.msg)
