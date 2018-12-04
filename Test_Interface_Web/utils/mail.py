"""
邮件类。用来给指定用户发送邮件。可指定多个收件人，可带附件。
"""
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from socket import gaierror, error
import logging
import urllib.request

class Email:
    def __init__(self, server, sender, password, receiver, title, message=None, path=None,emailtype=0):
        """初始化Email

        :param title: 邮件标题，必填。
        :param message: 邮件正文，非必填。
        :param path: 附件路径，可传入list（多附件）或str（单个附件），非必填。
        :param server: smtp服务器，必填。
        :param sender: 发件人，必填。
        :param password: 发件人密码，必填。
        :param receiver: 收件人，多收件人用“；”隔开，必填。
        """
        self.title = title
        self.message = message
        self.files = path

        self.msg = MIMEMultipart('related')

        self.server = server
        self.sender = sender
        self.receiver = receiver
        self.password = password

        self.emailtype=emailtype

    def _attach_file(self, att_file):
        """将单个文件添加到附件列表中"""
        att = MIMEText(open('%s' % att_file, 'rb').read(), 'plain', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        file_name = re.split(r'[\\|/]', att_file)
        att["Content-Disposition"] = 'attachment; filename="%s"' % file_name[-1]
        self.msg.attach(att)

    def send(self):
        self.msg['Subject'] = self.title
        self.msg['From'] = self.sender
        self.msg['To'] = self.receiver

        # 邮件正文
        if self.message:
            self.msg.attach(MIMEText(self.message,'html','utf-8'))

        # 添加附件，支持多个附件（传入list），或者单个附件（传入str）
        if self.files:
            if isinstance(self.files, list):
                for f in self.files:
                    self._attach_file(f)
            elif isinstance(self.files, str):
                self._attach_file(self.files)

        # 连接服务器并发送
        logger=logging.getLogger('ERROR')
        try:
            smtp_server = smtplib.SMTP(self.server)  # 连接sever
        except (gaierror and error) as e:
            logger.debug('发送邮件失败,无法连接到SMTP服务器，检查网络以及SMTP服务器. %s', e)
        else:
            try:
                smtp_server.login(self.sender, self.password)  # 登录
            except smtplib.SMTPAuthenticationError as e:
                logger.debug('用户名密码验证失败！%s', e)
            else:
                smtp_server.sendmail(self.sender, self.receiver.split(';'), self.msg.as_string())  # 发送邮件
            finally:
                smtp_server.quit()  # 断开连接
                logger.debug('发送邮件"{0}"成功! 收件人：{1}。如果没有收到邮件，请检查垃圾箱，'
                            '同时检查收件人地址是否正确'.format(self.title, self.receiver))


if __name__ == '__main__':

    emailtitle='接口自动化测试报告'
    #邮箱内容设置
    import datetime
    countinfo1=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    countinfo2=2
    countinfo3=3
    countinfo4=4
    countinfo5=5
    countinfo6=6
    _content = """
    <html>
        <body>
            <table>
                <tr>
                    <td>执行时间：</td>
                    <td>%s</td>
                </tr>
                <tr>
                    <td>用例总数：</td>
                    <td>%d个</td>
                </tr>
                <tr>
                    <td>通过数：</td>
                    <td>%d个</td>
                </tr>
                <tr>
                    <td>失败数：</td>
                    <td>%d个</td>
                </tr>
                <tr>
                    <td>错误数：</td>
                    <td>%d个</td>
                </tr>
                <tr>
                    <td>报告详情地址：</td>
                    <td><a href="http://10.9.2.142/report/testreport?id=%d" target="_blank">点击查看详情</a></td>
                </tr>
            </table>
        </body>
    </html>
    """%(countinfo1,countinfo2,countinfo3,countinfo4,countinfo5,countinfo6)

    #发邮件
    e = Email(title=emailtitle,
                  message=_content,
                  receiver='shilongzi@7lk.com',
                  server='smtp.7lk.com',
                  sender='7lktest@7lk.com',
                  password='29De8lhGibAE59Qw',
                  path=''
                  )
    e.send()


'''
    page = urllib.request.urlopen('http://127.0.0.1:8000/report/testreport?id=166')
    html = page.read()
    print(html)
    '''
