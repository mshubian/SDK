# -*- coding: utf-8 -*-

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

# model定义基类
Base = declarative_base()


def to_dic(inst, model_obj):
    result = dict()
    for column in model_obj.__table__.columns:
        value = getattr(inst, column.name)
        
        # 时间类型字段特殊处理下
        if column.type.__class__ == DateTime and value:
            result[column.name] = ((value - datetime(1970, 1, 1)).total_seconds() * 1000) - 8 * 3600 * 1000
        else:
            result[column.name] = value
    
    return result


class BaseModel(Base):
    """模型基类
    主要包含以下几个基础属性：
        id : 主键ID,自增型整数
        name : 名称,32长度字符串，唯一不可重复
        description : 备注描述，文本类型
        create_time : 创建时间，自动填充now函数
        update_time : 更新时间，自动填充now函数，每次update动作会自动更新
    """
    __abstract__ = True
    
    def __init__(self, **kwargs):
        super(BaseModel, self).__init__(**kwargs)
    
    def as_dict(self):
        return to_dic(self, self.__class__)
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), unique=True, comment="名称")
    description = Column(Text, comment="备注描述")
    create_time = Column(DateTime, default=datetime.now, comment="修改时间")
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="最新修改时间")
