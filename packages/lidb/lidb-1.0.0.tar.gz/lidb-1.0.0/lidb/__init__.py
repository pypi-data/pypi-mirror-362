# Copyright (c) ZhangYundi.
# Licensed under the MIT License. 
# Created on 2025/7/17 14:09
# Description:

from .init import (
    NAME,
    DB_PATH,
    CONFIG_PATH,
    LOGS_PATH,
    get_settings,
)

from .database import (
    sql,
    put,
    has,
    tb_path,
)

__version__ = "1.0.0"