# -*- coding: utf-8 -*-

import logging
from .monitor import EmailMonitor
from .exceptions import EmailMonitorConfigError
from .cli import main as cli_main

# 配置包级日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 公开接口
__all__ = [
    'EmailMonitor',
    'EmailMonitorConfigError',
    'cli_main'
]

# 元数据
__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your@email.com"
__license__ = "MIT"

# 初始化时显示版本信息（可选）
logger.info(f"PyEmailMonitor {__version__} initialized")