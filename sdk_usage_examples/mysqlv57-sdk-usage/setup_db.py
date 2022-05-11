# -*- coding: utf-8 -*- #

import logging

from datagrandSDK.mysql.v57.utils import setup_db_table

"""
达观mysql-sdk工具使用步骤二：【创建表】
"""

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='[%Y%m%d|%H:%M:%S]')
    
    # 创建表: SDK提供的方法会自动遍历所有基于BaseModel定义的Model列表逐个创建
    setup_db_table('mysql_config.json')
