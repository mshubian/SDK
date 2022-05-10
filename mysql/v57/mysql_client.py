# -*- coding: utf-8 -*-

import logging as log

from sqlalchemy import desc
from sqlalchemy.exc import ResourceClosedError

from .mysql_model import BaseModel


class SQLAlchemyAdapterMetaClass(type):
    @staticmethod
    def wrap(func):
        """Return a wrapped instance method"""
        
        
        def auto_commit(self, *args, **kwargs):
            try:
                # todo a trick for DB transaction issue
                return_value = func(self, *args, **kwargs)
                self.commit()
                return return_value
            except Exception as ex:
                self.rollback()
                log.error(ex)
                raise
        
        return auto_commit
    
    def __new__(mcs, name, bases, attrs):
        """If the method in this list, DON'T wrap it"""
        no_wrap = ["commit", "merge", "rollback", "remove", "session"]
        
        def wrap(method):
            """private methods are not wrapped"""
            if method not in no_wrap and not method.startswith("__"):
                attrs[method] = mcs.wrap(attrs[method])
        
        map(lambda m: wrap(m), attrs.keys())
        return super(SQLAlchemyAdapterMetaClass, mcs).__new__(mcs, name, bases, attrs)


class DBAdapter(object):
    def __init__(self, db_session):
        self.db_session = db_session


class SQLAlchemyAdapter(DBAdapter):
    """Use MetaClass to make this class"""
    __metaclass__ = SQLAlchemyAdapterMetaClass
    
    def __init__(self, db_session):
        super(SQLAlchemyAdapter, self).__init__(db_session)
    
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
        self.db_session.add(model_instance)
        self.commit()
    
    # -------------------- 删：删除table中的对象数据，此操作为物理删除 ------------------ #
    
    def delete_object(self, instance):
        """ Delete object 'object'. """
        self.db_session.delete(instance)
    
    def delete_all_objects(self, model_obj, *criterion):
        model_obj.query.filter(*criterion).delete(synchronize_session=False)
    
    def delete_all_objects_by(self, model_obj, **kwargs):
        """ Delete all objects matching the case sensitive filters in 'kwargs'. """
        
        # Convert each name/value pair in 'kwargs' into a filter
        query = model_obj.query.filter_by(**kwargs)
        
        # query filter by in_ do not support none args, use synchronize_session=False instead
        return query.delete(synchronize_session=False)
    
    # -------------------- 改：修改表中的数据（model_object） ------------------ #
    
    def update_object(self, model_instance, **kwargs):
        for key, value in kwargs.items():
            if hasattr(model_instance, key):
                setattr(model_instance, key, value)
            else:
                raise KeyError("Object '%s' has no field '%s'." % (type(model_instance), key))
        
        self.commit()
    
    # -------------------- 查：针对表数据对象提供常用的几组查询方式：暂不支持跨表操作 ------------------ #
    
    def get_object(self, model_obj, model_id) -> BaseModel:
        """ Retrieve one object specified by the primary key 'pk' """

        return model_obj.query.get(model_id)
    
    def get_first_object(self, model_obj, *criterion):
        return model_obj.query.filter(*criterion).first()
    
    def get_first_object_by(self, model_obj, **kwargs):
        return model_obj.query.filter_by(**kwargs).first()
    
    def get_all_objects(self, model_obj, *criterion):
        return model_obj.query.filter(*criterion).order_by(desc(model_obj.id)).all()
    
    def get_all_objects_by(self, model_obj, **kwargs):
        return model_obj.query.filter_by(**kwargs).order_by(desc(model_obj.id)).all()

    def get_all_objects_page(self, model_obj, page_num, page_size=100, *criterion):
        begin = (page_num - 1) * page_size
        return model_obj.query.filter(*criterion).order_by(desc(model_obj.id)).limit(page_size).offset(begin)
    
    def get_all_objects_page_by(self, model_obj, page_num, page_size=100, **kwargs):
        begin = (page_num - 1) * page_size
        return model_obj.query.filter_by(**kwargs).order_by(desc(model_obj.id)).limit(100).offset(begin)

    def get_all_objects_order(self, model_obj, order_by, **kwargs):
        return model_obj.query.filter_by(**kwargs).order_by(*order_by).all()
    
    def get_all_objects_order_by(self, model_obj, order_by, **kwargs):
        return model_obj.query.filter_by(**kwargs).order_by(order_by).all()
    
    def get_all_objects_group(self, model_obj, group_by, *criterion):
        return model_obj.query.filter(*criterion).group_by(group_by).all()
    
    def get_all_objects_group_by(self, model_obj, *group_by, **kwargs):
        return model_obj.query.filter_by(**kwargs).group_by(*group_by).all()
    
    def count(self, model_obj, *criterion):
        return model_obj.query.filter(*criterion).count()
    
    def count_by(self, model_obj, **kwargs):
        return model_obj.query.filter_by(**kwargs).count()
    
    # -------------------- 其他：提供直接执行sql语句的方式，增加扩展性，以备不时之需 ------------------ #
    
    def exec_sql(self, sql_str):
        """
        return a json/dict list object [{},{},{}]

        :param sql_str: 完整的sql执行语句
        :return: 根据执行结果进行返回，若有结果则以list(dict)的方式返回 （主要是考虑兼容性）
        """
        log.debug(sql_str)
        try:
            sql_result = self.session().execute(sql_str)
            if sql_result:
                return [{key: value for (key, value) in row.items()} for row in sql_result]
            return [{}]
        
        except ResourceClosedError:
            return None

        except Exception as ex:
            log.error(ex)
            return None