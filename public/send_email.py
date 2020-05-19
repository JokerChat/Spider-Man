# -*- coding: utf-8 -*-
# @Author       :junjie    
# @Time         :2020/5/4 13:07
# @FileName     :send_email.py
# @Motto        :AS the tree,so the fruit
#IDE            :PyCharm

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class SendMail(object):

    def __init__(self,smtp_server,
                 smtp_port,
                 smtp_sender,
                 smtp_senderpassword,
                 smtp_receiver,
                 smtp_subject,
                 smtp_body,
                 smtp_file=None):
        """
        to init parameter
        :param smtp_server: 邮件服务器
        :param smtp_port:端口号
        :param smtp_sender:发件人
        :param smtp_senderpassword:密码
        :param smtp_receiver:收件人
        :param smtp_subject:邮件主题
        :param smtp_body:邮件内容
        :param smtp_file_path:文件路径
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_sender = smtp_sender
        self.smtp_senderpassword = smtp_senderpassword
        self.smtp_receiver = smtp_receiver
        self.smtp_subject = smtp_subject
        self.smtp_body = smtp_body
        self.smtp_file = smtp_file

    def mail_content(self):
        """
        to edit mail content
        :param subject: 邮件主题
        :param body:邮件内容
        :return:msg
        """
        if self.smtp_file != None :
            msg = MIMEMultipart()
            with open(self.smtp_file,'rb') as fp:
                mail_body =fp.read()
            att = MIMEText(mail_body, "base64", "utf-8")
            att['Conten-Type'] = "application/octet-stream"
            att["Content-Disposition"] = 'attachment; filename="%s"' % self.smtp_file
            msg.attach(att)
            msg.attach(MIMEText(self.smtp_body, "html", "utf-8"))
            msg['from'] = self.smtp_sender
            msg['to'] = ";".join(self.smtp_receiver)
            msg['subject'] = self.smtp_subject
            return msg
        else:
            msg = MIMEText(self.smtp_body, "html", "utf-8")
            msg['from'] = self.smtp_sender
            msg['to'] = ";".join(self.smtp_receiver)
            msg['subject'] = self.smtp_subject
            return msg

    def send_mail(self):
        try:
            smtp = smtplib.SMTP()
            smtp.connect(self.smtp_server)
            smtp.login(user=self.smtp_sender,password=self.smtp_senderpassword)
        except:
            smtp = smtplib.SMTP_SSL()
            smtp.login(user=self.smtp_sender,password=self.smtp_senderpassword)
        aaa = self.mail_content()
        try:
            smtp.sendmail(self.smtp_sender,self.smtp_receiver,aaa.as_string())
            print("发送成功----")
        except Exception as e:
            print("发送失败...",e)
        smtp.quit()


if __name__ =='__main__':
    # SSL认证邮箱测试，如：QQ邮箱
    b = SendMail(smtp_server="smtp.qq.com",
                 smtp_port=465,
                 smtp_sender="664616581@qq.com",
                 smtp_senderpassword="xxxxx",
                 smtp_receiver=['664616581@qq.com','1927265398@qq.com'],
                 smtp_subject="测试邮件！！",
                 smtp_body="<p>我的简书地址：https://www.jianshu.com/u/c40cc1114855</p>")
    b.send_mail()
