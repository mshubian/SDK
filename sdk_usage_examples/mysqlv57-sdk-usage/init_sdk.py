# -*- coding: utf-8 -*- #

import logging

from datagrandSDK.mysql.v57 import init_mysql_sdk

"""
达观mysql-sdk工具使用步骤三：【初始化SDK】
"""

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='[%Y%m%d|%H:%M:%S]')
    
    # 初始化SDK
    mysql_client = init_mysql_sdk('mysql_config.json')
