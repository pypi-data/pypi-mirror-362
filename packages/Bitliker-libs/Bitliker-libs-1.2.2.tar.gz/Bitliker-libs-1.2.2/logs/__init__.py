#!/usr/bin/env python

"""
Author: Bitliker
Date: 2024-09-06 11:18:11
Version: 1.0
Description: 日志管理

引入库:
    logging
    requests
    colorama
"""

import logging
from colorama import init, Fore, Style
import requests

# 初始化Colorama
init()
# 创建Logger对象
_logger = logging.getLogger()
# 创建ConsoleHandler并设置日志级别
_console_handler = logging.StreamHandler()
# 设置日志级别
_logger.setLevel(logging.INFO)

# 将Handler添加到Logger中
_logger.addHandler(_console_handler)
# 设置不同级别的日志输出颜色
LOG_COLORS = {
    logging.DEBUG: Fore.CYAN,
    logging.INFO: Fore.GREEN,
    logging.WARNING: Fore.YELLOW,
    logging.ERROR: Fore.RED,
    logging.CRITICAL: Fore.MAGENTA,
}


class ColoredFormatter(logging.Formatter):
    """自定义日志输出格式"""

    def format(self, record):
        log_color = LOG_COLORS.get(record.levelno)
        message = super().format(record).replace("'", '"')
        tag = record.levelname if record.levelno != logging.CRITICAL else "HTTP"
        return f"{log_color}{tag} - {message}{Style.RESET_ALL}"


_console_handler.setFormatter(ColoredFormatter())

def info(message: str):
    """信息日志输出

    Args:
        message (str): 日志
    """
    _logger.info(message)

def debug(message: str):
    """信息日志输出

    Args:
        message (str): 日志
    """
    _logger.debug(message)

def error(message: str):
    """信息日志输出

    Args:
        message (str): 日志
    """
    _logger.error(message)


def warning(message: str):
    """信息日志输出

    Args:
        message (str): 日志
    """
    _logger.warning(message)



def format_bytes(bytes_size: int) -> str:
    """格式化大小格式

    Args:
        bytes_size (int): 字节数量

    Returns:
        str: 格式化的大小  52M12KB
    """

    # 定义单位
    if not bytes_size or bytes_size == 0:
        return "0B"
    units = ["B", "KB", "MB", "GB", "TB"]
    sign = "-" if bytes_size < 0 else ""
    bytes_size = abs(bytes_size)
    # 寻找合适的单位
    for unit in units:
        if bytes_size < 1024.0:
            return f"{sign}{bytes_size:.2f}{unit}"
        bytes_size /= 1024.0

    return f"{sign}{bytes_size:.2f}PB"  # 如果超过PB，这里可以继续扩展


def send_dingding(dd_token: str, title: str, content: str) -> None:
    """发送钉钉通知

    Args:
        dd_token (str): 钉钉机器人token
        title (str): 标题
        content (str): 内容
    """
    web_hook = "https://oapi.dingtalk.com/robot/send"
    headers = {"Content-Type": "application/json", "Charset": "UTF-8"}
    at = {"isAtAll": "false", "atUserIds": ["1ay-dujib2q3r1"]}
    markdown = {"title": title, "text": content}
    data = {"msgtype": "markdown", "at": at, "markdown": markdown}
    resopose = requests.post(
        f"{web_hook}?access_token={dd_token}", headers=headers, json=data, timeout=10
    )
    print(f"发送钉钉消息: {resopose.text}")


def log_http(response: requests.Response):
    """打印http请求日志"""
    _logger.critical("-------------start request------------------")
    url = response.request.url
    if "?" in url:
        data = url.split("?")[1]
        params_list = data.split("&")
        params = {}
        for param in params_list:
            params[param.split("=")[0]] = param.split("=")[1]
        url = url.split("?")[0]
    else:
        params = None
    _logger.critical("url: %s", url)
    _logger.critical("method: %s", response.request.method)
    _logger.critical("header: %s", response.request.headers)
    _logger.critical("params: %s", params)
    _logger.critical("status code : %d", response.status_code)
    _logger.critical("response : %s", response.text)
    _logger.critical("-------------end request------------------")
