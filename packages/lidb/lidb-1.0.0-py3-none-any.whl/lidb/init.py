# Copyright (c) ZhangYundi.
# Licensed under the MIT License. 
# Created on 2025/7/17 14:40
# Description:

from pathlib import Path
from dynaconf import Dynaconf
from loguru import logger
import sys


USERHOME = Path("~").expanduser() # 用户家目录
NAME = "lidb"
DB_PATH = USERHOME / NAME
CONFIG_PATH = DB_PATH / "conf" / "settings.toml"
LOGS_PATH = DB_PATH / "logs"

logger.remove()

console_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level}</level> | "
    f"<cyan>{NAME}</cyan>:<cyan>{{function}}</cyan>:<cyan>{{line}}</cyan> - "
    "<level>{message}</level>"
)

logger.add(
    sys.stderr,
    format=console_format,
    level="TRACE"
)

logger.add(
    LOGS_PATH / "{time:YYYYMMDD}.log",
    retention="10 days",
    format=f"{{time:YYYY-MM-DD HH:mm:ss}} | {{level}} | {NAME}:{{function}}:{{line}} - {{message}}",
    level="TRACE"
)

if not CONFIG_PATH.exists():
    try:
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logger.error(f"Create settings file failed: {e}")
    with open(CONFIG_PATH, "w") as f:
        template_content = f"""[global]
path="{DB_PATH}" 
"""
    with open(CONFIG_PATH, "w") as f:
        f.write(template_content)
    logger.info(f"Settings file created: {CONFIG_PATH}")

def get_settings():
    try:
        return Dynaconf(settings_files=[CONFIG_PATH])
    except Exception as e:
        logger.error(f"Read settings file failed: {e}")
        return {}

# 读取配置文件覆盖
_settiings = get_settings()
if _settiings is not None:
    setting_db_path = _settiings.get(f"global.path", "")
    if setting_db_path:
        DB_PATH = Path(setting_db_path)
