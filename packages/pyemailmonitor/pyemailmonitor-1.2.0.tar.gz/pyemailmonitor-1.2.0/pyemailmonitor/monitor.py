# -*- coding: utf-8 -*-
# @Author  : Zhao Yutao
# @Time    : 2025/7/15 19:58
# @Function: 邮件监控器
# @mails: zhaoyutao22@mails.ucas.ac.cn
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import traceback
import time
from contextlib import contextmanager
import logging
from .templates import EmailTemplates
from .exceptions import EmailMonitorConfigError

# 设置日志
logger = logging.getLogger("pyemailmonitor")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class EmailMonitor:
    def __init__(self, user_name, user_email,
                 smtp_server, smtp_port, smtp_user, smtp_password,
                 sender_name="System Monitor", use_ssl=True, test_mode=False):
        """
        初始化邮件监控器

        :param user_name: 用户名（收件人名称）
        :param user_email: 用户邮箱（收件人邮箱）
        :param smtp_server: SMTP服务器地址
        :param smtp_port: SMTP服务器端口
        :param smtp_user: SMTP登录用户名
        :param smtp_password: SMTP登录密码
        :param sender_name: 发件人名称（可选）
        :param use_ssl: 是否使用SSL连接（默认为True）
        :param test_mode: 测试模式（不实际发送邮件）
        """
        self.user_name = user_name
        self.user_email = user_email
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.sender_name = sender_name
        self.use_ssl = use_ssl
        self.test_mode = test_mode
        self.start_time = None
        self.program_name = "Unnamed Program"
        self.additional_recipients = []

        # 验证配置
        if not all([smtp_server, smtp_port, smtp_user, smtp_password]):
            raise EmailMonitorConfigError("SMTP configuration is incomplete")

        logger.info(f"EmailMonitor initialized for {user_name} <{user_email}>")
        if test_mode:
            logger.info("Running in TEST MODE - emails will not be sent")

    def add_recipient(self, email, name=None):
        """
        添加额外的收件人

        :param email: 收件人邮箱
        :param name: 收件人名称（可选）
        """
        self.additional_recipients.append((email, name or ""))
        logger.info(f"Added recipient: {name or ''} <{email}>")

    def _connect_to_smtp(self):
        """连接到SMTP服务器"""
        if self.test_mode:
            logger.info("Skipping SMTP connection (test mode)")
            return None

        try:
            if self.use_ssl:
                server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
                logger.info(f"Connected to SMTP_SSL server: {self.smtp_server}:{self.smtp_port}")
            else:
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()
                logger.info(f"Connected to SMTP server with STARTTLS: {self.smtp_server}:{self.smtp_port}")

            server.login(self.smtp_user, self.smtp_password)
            logger.info("SMTP login successful")
            return server
        except Exception as e:
            logger.error(f"SMTP connection failed: {str(e)}")
            raise

    def _send_email(self, subject, body):
        """发送邮件"""
        # 创建邮件对象
        msg = MIMEMultipart()
        msg['From'] = f"{self.sender_name} <{self.smtp_user}>"
        msg['To'] = f"{self.user_name} <{self.user_email}>"

        # 添加额外的收件人
        if self.additional_recipients:
            additional_emails = ", ".join(
                [f"{name} <{email}>" if name else email
                 for email, name in self.additional_recipients]
            )
            msg['Cc'] = additional_emails

        msg['Subject'] = subject

        # 添加邮件正文
        msg.attach(MIMEText(body, 'html'))

        # 获取所有收件人
        all_recipients = [self.user_email] + [email for email, _ in self.additional_recipients]

        try:
            # 如果是测试模式，不实际发送
            if self.test_mode:
                logger.info(f"TEST MODE: Would send email to {all_recipients}")
                logger.info(f"Subject: {subject}")
                logger.debug(f"Body:\n{body}")
                return True

            # 连接到SMTP服务器并发送邮件
            with self._connect_to_smtp() as server:
                server.sendmail(
                    self.smtp_user,
                    all_recipients,
                    msg.as_string()
                )
            logger.info(f"Email sent successfully to {all_recipients}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False

    def send_start_notification(self, program_name):
        """
        发送程序开始通知

        :param program_name: 程序名称
        """
        self.program_name = program_name
        self.start_time = time.time()
        subject = f"程序启动通知: {program_name}"
        body = EmailTemplates.start_template.format(
            user_name=self.user_name,
            program_name=program_name,
            start_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.start_time))
        )
        logger.info(f"Sending start notification for {program_name}")
        return self._send_email(subject, body)

    def send_success_notification(self):
        """发送程序成功完成通知"""
        if not self.start_time:
            raise RuntimeError("Program not started. Call send_start_notification first.")

        end_time = time.time()
        duration = end_time - self.start_time
        subject = f"程序成功完成: {self.program_name}"
        body = EmailTemplates.success_template.format(
            user_name=self.user_name,
            program_name=self.program_name,
            start_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.start_time)),
            end_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time)),
            duration=self._format_duration(duration)
        )

        logger.info(f"Sending success notification for {self.program_name}")
        return self._send_email(subject, body)

    def send_error_notification(self, exception):
        """发送程序错误通知"""
        if not self.start_time:
            raise RuntimeError("Program not started. Call send_start_notification first.")

        end_time = time.time()
        duration = end_time - self.start_time
        error_traceback = traceback.format_exc()

        subject = f"程序运行错误: {self.program_name}"
        body = EmailTemplates.error_template.format(
            user_name=self.user_name,
            program_name=self.program_name,
            start_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.start_time)),
            end_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time)),
            duration=self._format_duration(duration),
            exception_type=type(exception).__name__,
            exception_message=str(exception),
            error_traceback=error_traceback
        )

        logger.error(f"Sending error notification for {self.program_name}: {str(exception)}")
        return self._send_email(subject, body)

    def _format_duration(self, seconds):
        """格式化持续时间"""
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours)}小时{int(minutes)}分钟{int(seconds)}秒"

    @contextmanager
    def monitor(self, program_name):
        """
        上下文管理器，用于监控程序运行

        :param program_name: 程序名称
        """
        self.send_start_notification(program_name)
        try:
            yield
            self.send_success_notification()
        except Exception as e:
            self.send_error_notification(e)
            raise  # 重新抛出异常
        finally:
            # 重置状态
            self.start_time = None
            self.program_name = "Unnamed Program"