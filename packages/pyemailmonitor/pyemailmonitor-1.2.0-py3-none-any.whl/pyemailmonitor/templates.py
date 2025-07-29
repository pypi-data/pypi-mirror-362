# -*- coding: utf-8 -*-
# @Author  : Zhao Yutao
# @Time    : 2025/7/15 19:58
# @Function: 邮件模板
# @mails: zhaoyutao22@mails.ucas.ac.cn
class EmailTemplates:
    """邮件模板"""

    # 程序开始模板
    start_template = """
    <html>
    <body>
        <h2>程序启动通知</h2>
        <p>尊敬的 {user_name}，您好！</p>
        <p>您的程序 <strong>{program_name}</strong> 已开始运行。</p>
        <p>启动时间: {start_time}</p>
        <p>系统将在程序完成或发生错误时发送通知。</p>
        <hr>
        <p style="color: #888; font-size: 0.9em;">
            此邮件由自动监控系统发送，请勿直接回复。
        </p>
    </body>
    </html>
    """

    # 程序成功完成模板
    success_template = """
    <html>
    <body>
        <h2 style="color: green;">程序成功完成</h2>
        <p>尊敬的 {user_name}，您好！</p>
        <p>您的程序 <strong>{program_name}</strong> 已成功完成运行。</p>
        <p>启动时间: {start_time}</p>
        <p>完成时间: {end_time}</p>
        <p>运行时长: {duration}</p>
        <hr>
        <p style="color: #888; font-size: 0.9em;">
            此邮件由自动监控系统发送，请勿直接回复。
        </p>
    </body>
    </html>
    """

    # 程序错误模板
    error_template = """
    <html>
    <body>
        <h2 style="color: red;">程序运行错误</h2>
        <p>尊敬的 {user_name}，您好！</p>
        <p>您的程序 <strong>{program_name}</strong> 在运行过程中发生了错误。</p>
        <p>启动时间: {start_time}</p>
        <p>错误发生时间: {end_time}</p>
        <p>运行时长: {duration}</p>

        <h3>错误信息</h3>
        <p><strong>错误类型:</strong> {exception_type}</p>
        <p><strong>错误消息:</strong> {exception_message}</p>

        <h3>错误堆栈跟踪</h3>
        <pre>{error_traceback}</pre>

        <hr>
        <p style="color: #888; font-size: 0.9em;">
            此邮件由自动监控系统发送，请勿直接回复。
        </p>
    </body>
    </html>
    """