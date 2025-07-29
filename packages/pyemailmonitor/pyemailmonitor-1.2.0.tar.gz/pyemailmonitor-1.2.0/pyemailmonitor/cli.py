# -*- coding: utf-8 -*-
# @Author  : Zhao Yutao
# @Time    : 2025/7/15 19:58
# @Function: 脚手架
# @mails: zhaoyutao22@mails.ucas.ac.cn
import os
import json
import argparse
from .monitor import EmailMonitor
from .exceptions import EmailMonitorConfigError

CONFIG_PATH = os.path.expanduser("~/.pyemailmonitor_config.json")


def configure(args):
    """保存用户配置到文件"""
    config = {
        "user_name": args.user_name,
        "user_email": args.user_email
    }

    # 添加可选参数
    if args.sender_name:
        config["sender_name"] = args.sender_name

    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)

    print(f"配置已保存至 {CONFIG_PATH}")


def get_config():
    """从文件加载配置"""
    if not os.path.exists(CONFIG_PATH):
        raise EmailMonitorConfigError(f"未找到配置文件，请先运行 'email-monitor configure'")

    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def run_monitor(args):
    """运行程序监控"""
    try:
        # 加载配置
        config = get_config()

        # 创建监控器
        monitor = EmailMonitor(
            user_name=config["user_name"],
            user_email=config["user_email"],
            smtp_server=args.smtp_server,
            smtp_port=args.smtp_port,
            smtp_user=args.smtp_user,
            smtp_password=args.smtp_password,
            sender_name=config.get("sender_name", "System Monitor"),
            use_ssl=not args.no_ssl,
            test_mode=args.test_mode
        )

        # 添加额外收件人
        if args.cc:
            for email in args.cc.split(","):
                monitor.add_recipient(email.strip())

        # 使用监控器
        with monitor.monitor(args.program_name):
            # 执行用户命令
            if args.command:
                print(f"执行命令: {' '.join(args.command)}")
                import subprocess
                result = subprocess.run(args.command, capture_output=True, text=True)

                if result.returncode != 0:
                    raise RuntimeError(f"命令执行失败 (退出码: {result.returncode})\n{result.stderr}")

                print(result.stdout)
            else:
                print(f"监控程序: {args.program_name}")
                input("按 Enter 继续...")

        print("程序执行完成，已发送成功通知")

    except Exception as e:
        print(f"发生错误: {str(e)}")


def main():
    """主命令行接口"""
    parser = argparse.ArgumentParser(
        description="PyEmailMonitor - 程序执行监控与邮件通知工具",
        formatter_class=argparse.RawTextHelpFormatter
    )

    subparsers = parser.add_subparsers(title="命令", dest="command", required=True)

    # 配置命令
    config_parser = subparsers.add_parser("configure", help="配置用户信息")
    config_parser.add_argument("--user-name", required=True, help="用户名")
    config_parser.add_argument("--user-email", required=True, help="用户邮箱")
    config_parser.add_argument("--sender-name", help="发件人名称（可选）")
    config_parser.set_defaults(func=configure)


    # MZqtAQDTX29hnyUd


    # 运行命令
    run_parser = subparsers.add_parser("run", help="运行监控程序")
    run_parser.add_argument("program_name", help="程序名称")
    run_parser.add_argument("--smtp-server", default='smtp.163.com', help="SMTP服务器地址")
    run_parser.add_argument("--smtp-port", default=465, type=int, help="SMTP服务器端口")
    run_parser.add_argument("--smtp-user", default='zzu_yutaozhao@163.com', help="SMTP用户名")
    run_parser.add_argument("--smtp-password", default='MZqtAQDTX29hnyUd', help="SMTP密码")
    run_parser.add_argument("--no-ssl", action="store_true", help="不使用SSL连接")
    run_parser.add_argument("--cc", help="抄送邮箱（多个用逗号分隔）")
    run_parser.add_argument("--test-mode", action="store_true", help="测试模式（不实际发送邮件）")
    run_parser.add_argument("command", nargs=argparse.REMAINDER, help="要执行的命令（可选）")
    run_parser.set_defaults(func=run_monitor)

    # 显示配置命令
    show_parser = subparsers.add_parser("show-config", help="显示当前配置")
    show_parser.set_defaults(func=lambda args: print(json.dumps(get_config(), indent=2)))

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()