#!/usr/local/bin/python
# -*- coding:utf-8 -*-
"""
 __createTime__ = 20250714-090655
 __author__ = "WeiYanfeng"
 __version__ = "0.0.1"

~~~~~~~~~~~~~~~~~~~~~~~~
程序单元功能描述
在 zmail 和 dotenv 基础，简洁封装邮件发送

改造要点如下：
- 封装常见的 163.com/qq.com 邮箱（由于 139.com 邮箱常拒发邮件，暂时放弃）
- 通过 dotenv 处理账号、密码等敏感信息
- 采用 SSL 协议

参考
[PYTHON实现自动发送邮件（QQ，163，139三种邮箱演示）](https://blog.csdn.net/hot7732788/article/details/121247711)
测试 [zmail](https://github.com/zhangyunhao116/zmail) 库
[Zmail--让邮件变得简单(python)](https://zhuanlan.zhihu.com/p/33699468)
[Zmail中文介绍](https://github.com/zhangyunhao116/zmail/blob/master/README-cn.md)

# 依赖包 Package required
# pip install weberFuncs
# pip install dotenv
# pip install zmail
"""

import sys
from weberFuncs import PrintTimeMsg
import os
import zmail
from dotenv import load_dotenv
import logging
# from smtplib import SMTPResponseException


class CEnvZMail:
    def __init__(self, sFullEnvFN):
        # sFullEnvFN 全路径的env文件
        self.sFullEnvFN = sFullEnvFN
        bLoad = load_dotenv(dotenv_path=self.sFullEnvFN, override=True)  # load environment variables from .env
        PrintTimeMsg(f"CEnvZMail.load_dotenv({self.sFullEnvFN})={bLoad}")
        if not bLoad:
            exit(-1)

        self.debug_zmail = True
        self.debug_zmail = False
        self.logger = self._setup_zmail_logger() if self.debug_zmail else None
        # self.logger = self._setup_zmail_logger()
        # self.logger.info("Zmail服务器连接成功建立")

        self.smtp_ssl = True
        # self.smtp_ssl = False

        self.oZmail = None  # 由应用层调用 init_zmail

    def _setup_zmail_logger(self):
        """配置一个专门用于Zmail的logger"""
        from logging.handlers import RotatingFileHandler

        logger = logging.getLogger('zmail')  # CEnvZMail
        logger.setLevel(logging.DEBUG)

        # 控制台输出
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # 文件输出（自动轮转）
        file_handler = RotatingFileHandler(
            'zmail.log',
            maxBytes=1024 * 1024,  # 1MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)

        # 设置日志格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger

    def _get_passwd_by_acct(self, sMailAcct):
        # 从环境变量中读取账号密码
        sAcctPasswd = os.getenv(sMailAcct, '')
        if not sAcctPasswd:
            PrintTimeMsg(f'_get_passwd_by_acct({sMailAcct}).sAcctPasswd={sAcctPasswd}=Not Set In {self.sFullEnvFN}!')
        return sAcctPasswd

    def _init_zmail(self, sOwnerMail):
        # 初始化zmail
        # sOwnerMail=所有者邮箱
        sOwnerPasswd = self._get_passwd_by_acct(sOwnerMail)
        if not sOwnerPasswd:
            return None

        oZmail = zmail.server(sOwnerMail, sOwnerPasswd,
                              smtp_ssl=self.smtp_ssl,
                              debug=self.debug_zmail,
                              log=self.logger)
        return oZmail

    def zmail_send(self, sSndMail, sRcvMail, dictMailContent):
        # 发送邮件
        # sSndMail 发送者邮箱
        # sRcvMail 接收者邮箱，可以是列表，也可以是逗号分隔的多个
        # dictMailContent 是邮件内容字典，支持如下键值
        #    subject=主题
        #    content_text=文本内容
        #    content_html=html内容
        #    attachments=附件文件名
        oZmail = self._init_zmail(sSndMail)
        if not oZmail: return False
        is_smtp_able = oZmail.smtp_able()
        PrintTimeMsg(f'zmail_send({sSndMail} -> {sRcvMail}).is_smtp_able={is_smtp_able}=')
        try:
            oZmail.send_mail(sRcvMail, dictMailContent)  # 发送邮件
            PrintTimeMsg(f'zmail_send({sSndMail} -> {sRcvMail})=OK!')
            return True
        except Exception as e:
            PrintTimeMsg(f'zmail_send({sSndMail} -> {sRcvMail}).e={repr(e)}=')
        return False

    def zmail_recv_init(self, sOwnerMail):
        # 初始化收取邮件
        # sOwnerMail=接收者邮箱
        # 返回 oZmail ，可进一步调用zmail的如下方法
        #   get_latest() 取得最新邮件
        #   get_mail(which) 取得指定邮件
        #   delete(which) 删除指定邮件
        #   get_headers(start_index=None,end_index=None) 遍历取得邮件头信息
        #   get_mails(subject=None,start_time=None,end_time=None,sender=None,start_index=None,end_index=None) 过滤邮件
        oZmail = self._init_zmail(sOwnerMail)
        if not oZmail: return None
        is_pop_able = oZmail.pop_able()
        PrintTimeMsg(f'zmail_recv_init({sOwnerMail}).is_pop_able={is_pop_able}=')
        mailbox_info = oZmail.stat()
        iMailMsgCnt, iMailBoxSize = mailbox_info
        PrintTimeMsg(f'zmail_recv_init.iMailMsgCnt={iMailMsgCnt}, iMailBoxSize={iMailBoxSize}=')
        oZmail.iMailMsgCnt = iMailMsgCnt
        return oZmail

    def zmail_recv_filter(self, oZmail, sSubjectWord, cbFilter):
        # 过滤处理邮件
        # oZmail=zmail对象
        # sSubjectWord=邮件主题要包含的主题词
        # cbFilter(iWhich, sSender, sTitle, sContent) 回调函数
        # 返回过滤匹配删除的邮件数
        iFilterDeleteCnt = 0
        # oRet = oZmail.get_headers()
        # PrintTimeMsg(f'zmail_recv.oRet=({oRet})!')
        for iIdx in range(oZmail.iMailMsgCnt):
            iWhich = oZmail.iMailMsgCnt - iIdx  # 倒序
            dictMail = oZmail.get_mail(iWhich)
            sTitle = dictMail['subject']
            sSender = dictMail['from']
            PrintTimeMsg(f'zmail_recv.get_mail({iWhich})={sSender},sTitle={sTitle}=')
            if sSubjectWord in sTitle:
                sContent = ''.join(dictMail['content_text'])
                bFilter = cbFilter(iWhich, sSender, sTitle, sContent)
                PrintTimeMsg(f'zmail_recv.cbFilter({iWhich})={bFilter}=')
                if bFilter:  # 回调处理成功，则删除邮件
                    oDeleteRet = oZmail.delete(iWhich)
                    PrintTimeMsg(f'zmail_recv.delete({iWhich})={oDeleteRet}=')
                    iFilterDeleteCnt += 1
        return iFilterDeleteCnt

        # latest_mail = oZmail.get_latest()
        # oRet = zmail.show(latest_mail)
        # PrintTimeMsg(f'zmail_recv.oRet=({oRet})!')

        # oRet = oZmail.get_mails(subject, start_time, end_time, sender, start_index, end_index)
        # PrintTimeMsg(f'zmail_recv.oRet=({oRet})!')

