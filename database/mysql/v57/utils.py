# -*- coding: utf-8 -*- #

import logging

from sqlalchemy import create_engine

from . import load_mysql_config
from .mysql_model import Base

"""
工具库：主要基于提供几个常用工具：
    1. 创建表（根据model的定义进行自动创建表的动作）
    2. 更新表结构（表结构升级推送至数据库端）
"""


def setup_db_table(mysql_config_file):
    """
    根据所有表的model定义来自动在数据库服务端创建所有表
    当出现数据表重名（表已存在）则跳过该表创建下一个
    
    此工具函数适合在【环境初始化阶段】以及【新增表】场景下执行
    """
    try:
        mysql_conn_str = load_mysql_config(mysql_config_file)
        
        engine = create_engine(mysql_conn_str)
        logging.info("数据库链接成功")
        
        logging.info("开始创建mysql数据表")
        Base.metadata.create_all(bind=engine)
        logging.info("..................创建完成")
    
    except Exception as ex:
        logging.error("数据表创建失败！请检查日志错误信息！")
        logging.error(ex)
        exit(1)


def update_db_schema(mysql_config_file):
    """
    根据所有表的model定义来对服务端的数据库表结构进行更新操作
    此工具函数适合在【开发阶段】和【版本升级时】场景下执行
    """
