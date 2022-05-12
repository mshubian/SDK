# -*- coding: utf-8 -*-

import logging as log

from sqlalchemy import desc
from sqlalchemy.exc import ResourceClosedError

from .mysql_model import BaseModel


class SQLAlchemyAdapterMetaClass(type):
    """
    此类主要是加入一个基类，通过基类增加一些必要通用操作，如：auto_commit操作.
    我们在使用sqlalchemy时出现过查询类的动作也需要加上commit才能正常的得到返回结果。因此想把所有的读写操作方法都进行一个commit动作
    采用基类能够避免重复，而且此部分工作还需要深究下，找到具体原因后，或可删除此部分内容。（也可能是因为版本老旧的问题所导致）
    
    TODO: 重新确认下此部分的内容，予以更新。
    """
    
    @staticmethod
    def auto_commit(func):
        """
        构建一个装饰器，方便进行自动commit操作
        TODO: 此次后续需优化（此处是一刀切的方式把读写操作都进行commit动作）
        """
        
        def wrap(self, *args, **kwargs):
            try:
                return_value = func(self, *args, **kwargs)
                self.commit()
                return return_value
            except Exception as ex:
                self.rollback()
                log.error(ex)
                raise
        
        return wrap
    
    def __new__(mcs, name, bases, attrs):
        no_wrap = ["commit", "merge", "rollback", "remove", "session"]
        
        def wrap(method):
            """private methods are not wrapped"""
            if method not in no_wrap and not method.startswith("__"):
                attrs[method] = mcs.auto_commit(attrs[method])
        
        map(lambda m: wrap(m), attrs.keys())
        return super(SQLAlchemyAdapterMetaClass, mcs).__new__(mcs, name, bases, attrs)


class DBAdapter(object):
    """
    此父类主要的主要目的是对整个Client进行分层：
        面向基础服务端【对内】：如面向数据基础服务相关的，如连接池，session池，以及必要的一些增强扩展等 （TODO）
        面向应用操作端【对外】：把具体应用方法(具体数据操作)放在子类(SQLAlchemyClient)中
    """
    
    def __init__(self, db_session):
        self.db_session = db_session


class SQLAlchemyClient(DBAdapter):
    """
    面向开发者，提供的mysql数据库数据操作想过的工具类。
    整个工具类的核心实际上仍是基于sqlalchemy进行简单封装而来。（主要是Model继承declarative_base()而来）
    """
    
    # 通过基元类来构建对象：把auto_commit()的动作引入进来
    __metaclass__ = SQLAlchemyAdapterMetaClass
    
    def __init__(self, db_session):
        super(SQLAlchemyClient, self).__init__(db_session)
    
    # ------------------ ORM  basic functions -------------------- #
    
    def commit(self):
        self.db_session.commit()
    
    def remove(self):
        self.db_session.remove()
    
    def merge(self, obj):
        self.db_session.merge(obj)
    
    def rollback(self):
        self.db_session.rollback()
    
    def session(self):
        return self.db_session
    
    # -------------------- 增：新增对象insert至table中 ------------------ #
    
    def add_object(self, model_instance):
        """添加数据：将一个model实例插入至数据表中
        
        :param model_instance: 具体Model对象的结果实例
        :return:
        """
        self.db_session.add(model_instance)
        self.commit()
    
    # -------------------- 删：删除table中的对象数据，此操作为物理删除 ------------------ #
    
    def delete_object(self, model_instance):
        """删除一条数据：物理删除删除一个具体的model实例

        :param model_instance: 具体Model对象的结果实例
        :return:
        """
        self.db_session.delete(model_instance)
    
    def delete_all_objects(self, model_obj, *criterion):
        """删除多条数据：根据匹配条件，筛选删除多条数据（物理删除）

        :param model_obj: 某个Model定义对象class。（去哪张表里面执行删除动作）
        :param criterion: filter式筛选匹配条件 (可多个)
        :return:
        """
        model_obj.query.filter(*criterion).delete(synchronize_session=False)
    
    def delete_all_objects_by(self, model_obj, **kwargs):
        """删除多条数据：根据匹配条件，筛选删除多条数据（物理删除）

        :param model_obj: 某个Model定义对象class。（去哪张表里面执行删除动作）
        :param kwargs: filter_by式筛选匹配条件（dict）
        :return:
        """
        # 删除前，先查询
        query = model_obj.query.filter_by(**kwargs)
        return query.delete(synchronize_session=False)
    
    # -------------------- 改：修改表中的数据（model_object） ------------------ #
    
    def update_object(self, model_instance, **kwargs):
        """修改单条数据：对一个具体的model实例对指定属性和结果值进行修改

        :param model_instance: 具体Model对象的结果实例
        :param kwargs: 要修改的目标字段以及目标值（dict）
        :return:
        """
        for key, value in kwargs.items():
            if hasattr(model_instance, key):
                setattr(model_instance, key, value)
            else:
                raise KeyError("Object '%s' has no field '%s'." % (type(model_instance), key))
        
        self.commit()
    
    # -------------------- 查：针对表数据对象提供常用的几组查询方式：暂不支持跨表操作 ------------------ #
    
    def get_object(self, model_obj, model_id) -> BaseModel:
        """根据主键单条数据

        :param model_obj: 某个Model定义对象class。（去哪张表里面执行查询动作）
        :param model_id: 主键(model定义时制定的主键)
        
        :return: model对象结果实例
        """
        return model_obj.query.get(model_id)
    
    def get_first_object_filter(self, model_obj, *criterion):
        """根据filter式查询条件查询单条数据

        :param model_obj: 某个Model定义对象class。（去哪张表里面执行查询动作）
        :param criterion: filter式查询条件
        
        :return: model对象结果实例
        """
        return model_obj.query.filter(*criterion).first()
    
    def get_first_object_filter_by(self, model_obj, **kwargs):
        """根据filter_by式查询条件查询单条数据

        :param model_obj: 某个Model定义对象class。（去哪张表里面执行查询动作）
        :param kwargs: filter_by式查询条件

        :return: model对象结果实例
        """
        return model_obj.query.filter_by(**kwargs).first()
    
    def get_all_objects_filter(self, model_obj, *criterion):
        """根据filter式查询条件筛选查询多条数据

        :param model_obj: 某个Model定义对象class。（去哪张表里面执行查询动作）
        :param criterion: filter式查询条件

        :return: list[model]  列表：结果实例列表
        """
        return model_obj.query.filter(*criterion).order_by(desc(model_obj.id)).all()
    
    def get_all_objects_filter_by(self, model_obj, **kwargs):
        """根据filter_by式查询条件筛选查询多条数据

        :param model_obj: 某个Model定义对象class。（去哪张表里面执行查询动作）
        :param kwargs: filter_by式查询条件

        :return: list[model]  列表：结果实例列表
        """
        return model_obj.query.filter_by(**kwargs).order_by(desc(model_obj.id)).all()
    
    def get_all_objects_page_filter(self, model_obj, page_num, page_size=100, *criterion):
        """根据filter_by式查询条件分页查询

        :param model_obj: 某个Model定义对象class。（去哪张表里面执行查询动作）
        :param page_num: 查询第几页
        :param page_size: 每页数据量长度，默认为300
        :param criterion: filter式查询条件

        :return: list[model]  列表：结果实例列表
        """
        begin = (page_num - 1) * page_size
        return model_obj.query.filter(*criterion).order_by(desc(model_obj.id)).limit(page_size).offset(begin)
    
    def get_all_objects_page_filter_by(self, model_obj, page_num, page_size=100, **kwargs):
        """根据filter_by式查询条件分页查询

        :param model_obj: 某个Model定义对象class。（去哪张表里面执行查询动作）
        :param page_num: 查询第几页
        :param page_size: 每页数据量长度，默认为300
        :param kwargs: filter_by式查询条件

        :return: list[model]  列表：结果实例列表
        """
        begin = (page_num - 1) * page_size
        return model_obj.query.filter_by(**kwargs).order_by(desc(model_obj.id)).limit(100).offset(begin)
    
    def get_all_objects_order_filter(self, model_obj, order, *criterion):
        """指定排序字段，根据filter式筛选查询

        :param model_obj: 某个Model定义对象class。（去哪张表里面执行查询动作）
        :param order: 制定的排序字段
        :param criterion: filter式查询条件

        :return: list[model]  列表：结果实例列表
        """
        return model_obj.query.filter(*criterion).order_by(order).all()
    
    def get_all_objects_order_filter_by(self, model_obj, order, **kwargs):
        """指定排序字段，根据filter_by式筛选查询

        :param model_obj: 某个Model定义对象class。（去哪张表里面执行查询动作）
        :param order: 制定的排序字段
        :param kwargs: filter_by式查询条件

        :return: list[model]  列表：结果实例列表
        """
        return model_obj.query.filter_by(**kwargs).order_by(order).all()
    
    def get_all_objects_group_filter(self, model_obj, group_by, *criterion):
        """指定分组字段，根据filter式筛选进行分组查询

        :param model_obj: 某个Model定义对象class。（去哪张表里面执行查询动作）
        :param group_by: 指定的分组字段
        :param criterion: filter式查询条件

        :return: list[model]  列表：结果实例列表
        """
        return model_obj.query.filter(*criterion).group_by(group_by).all()
    
    def get_all_objects_group_filter_by(self, model_obj, group_by, **kwargs):
        """指定分组字段，根据filter_by式筛选进行分组查询

        :param model_obj: 某个Model定义对象class。（去哪张表里面执行查询动作）
        :param group_by: 指定的分组字段
        :param kwargs: filter_by式查询条件

        :return: list[model]  列表：结果实例列表
        """
        return model_obj.query.filter_by(**kwargs).group_by(group_by).all()
    
    def count_filter(self, model_obj, *criterion):
        """统计行数：根据filter式筛选进行统计

        :param model_obj: 某个Model定义对象class。（去哪张表里面执行查询动作）
        :param criterion: filter式查询条件

        :return: Int 计数结果
        """
        return model_obj.query.filter(*criterion).count()
    
    def count_filter_by(self, model_obj, **kwargs):
        """统计行数：根据filter_by式筛选进行统计

        :param model_obj: 某个Model定义对象class。（去哪张表里面执行查询动作）
        :param kwargs: filter式查询条件

        :return: Int 计数结果
        """
        return model_obj.query.filter_by(**kwargs).count()
    
    # -------------------- 其他：提供直接执行sql语句的方式，增加扩展性，以备不时之需 ------------------ #
    
    def exec_sql(self, sql_str):
        """执行原生sql语句
        
        :param sql_str: 完整的sql执行语句
        :return: 根据执行结果进行返回，若有结果则以list(dict)的方式返回 （主要是考虑兼容性），主要有以下三种情况：
            第一种：[{}], 表明SQL语句无返回结果，如执行的是个写操作(update语句)
            第二种：[{k:v},...,{k:v}], 表明SQL语句有返回结果，结果内容每行转义成一个{},最终整体以list返回
            第三种：None, 表明SQL执行报错，需查看Error日志确认具体错误信息
        """
        log.debug("执行原生SQL语句，内容如下：")
        log.debug(sql_str)
        try:
            sql_result = self.session().execute(sql_str)
            if sql_result:
                return [{key: value for (key, value) in row.items()} for row in sql_result]
            return [{}]
        
        except ResourceClosedError:
            return None
        
        except Exception as ex:
            log.error("SQL执行报错！！！")
            log.error(ex)
            return None
