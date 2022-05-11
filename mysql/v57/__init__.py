# -*- coding: utf-8 -*-

import json
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from .mysql_client import SQLAlchemyClient
from .mysql_model import BaseModel


def init_mysql_sdk(mysql_config_file):
    """初始化 mysql sdk
    
    :param mysql_config_file: mysql配置文件的绝对路径
    :return: SQLAlchemySDK 工具类实例
    
        第一步：读取mysql配置文件
        第二步：连接验证mysql访问信息
        第三步：生成mysql_sdk实例对象并返回
    """
    logging.info("开始初始化加载datagrand-mysql-sdk")
    conn_str = load_mysql_config(mysql_config_file)
    db_session = conn_mysql(conn_str)
    BaseModel.query = db_session.query_property()
    logging.info("datagrand-mysql-sdk加载完成")
    return SQLAlchemyClient(db_session)


def conn_mysql(mysql_conn_str):
    """
    连接mysql，验证配置信息，并返回链接session对象
    """
    try:
        logging.info("连接接数据库")
        mysql_engine = create_engine(mysql_conn_str,
                                     convert_unicode=True,
                                     pool_size=50,
                                     max_overflow=100,
                                     echo=False)
        db_session = scoped_session(sessionmaker(bind=mysql_engine))
        logging.info(".......................成功")
        return db_session
    
    except Exception as ex:
        logging.error("Mysql连接失败，请检查配置项！")
        logging.error(ex)
        exit(1)


def load_mysql_config(mysql_config_file):
    """
    读取mysql配置文件，生成mysql链接串联
    """
    logging.info("读取Mysql配置文件")
    try:
        config_json = json.load(open(mysql_config_file, 'r', encoding="utf-8"))
        host = config_json['mysql']['host']
        port = config_json['mysql']['port']
        database = config_json['mysql']['database']
        username = config_json['mysql']['username']
        password = config_json['mysql']['password']
        charset = config_json['mysql']['charset'] or "utf8"
        logging.info("................成功")
        return 'mysql+mysqldb://%s:%s@%s:%s/%s?charset=%s&use_unicode=False' % (username,
                                                                                password,
                                                                                host,
                                                                                port,
                                                                                database,
                                                                                charset)
    
    except Exception as ex:
        logging.error("Mysql数据库配置文件不存在或内容格式不正确，导致加载失败！请参考")