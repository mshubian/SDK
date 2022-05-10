# -*- coding: utf-8 -*- #

import logging

from datagrandSDK.mysql.v57 import init_mysql_sdk
from datagrandSDK.mysql.v57.utils import setup_db_table

from .service import user_service

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='[%Y%m%d|%H:%M:%S]')
    
    setup_db_table('mysql_config.json')
    mysql_client = init_mysql_sdk('mysql_config.json')
    
    user_service.add_user()
    user_service.delete_user()
    user_service.update_user()
    user_service.get_user_list()
    user_service.get_role_user_list()
    user_service.complex_sql_operation()
