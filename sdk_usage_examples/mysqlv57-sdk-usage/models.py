# -*- coding: utf-8 -*- #

from datagrandSDK.mysql.v57.mysql_model import BaseModel, Column
from datagrandSDK.mysql.v57.mysql_model import Integer, Float, String, Text, DateTime, JSON, ForeignKey

"""
达观mysql-sdk工具使用步骤一：【基于BaseModel定义model】

BaseModel中已包含常规默认的5个属性如下：
id = Column(Integer, primary_key=True, autoincrement=True)
name = Column(String, comment="名称")
description = Column(Text, comment="备注描述")
create_time = Column(DateTime, default=datetime.now, comment="修改时间")
update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="最近修改时间", index=True)

开发者自定义model(对照表设计填充字段)。（当然，BaseModel里面的字段仍然是可以重新定义的）
"""


class User(BaseModel):
    """
    model定义: 用户表
    经此定义, 最终User表对象包含5+6=11个column字段
    """
    __tablename__ = 'user'
    
    phone = Column(String(16), nullable=False, unique=True, comment='手机号')
    sex = Column(String(8), comment='性别')
    age = Column(Integer, comment='年龄')
    height = Column(Float(precision="4,2"), comment='身高(m)')
    weight = Column(Float(precision="4,2"), comment='体重(KG)')
    background = Column(Text, comment='背景信息')
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)


class Role(BaseModel):
    """
    model定义：角色表

    """
    __tablename__ = 'role'
    
    extra_info = Column(JSON, comment='补充信息')  # mysql5.7支持JSON字段方便信息扩展
    
    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)


class UserRoleRel(BaseModel):
    __tablename__ = 'user_role_rel'
    
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), comment="用户关联ID")
    user_name = Column(String(32), comment='用户名称')  # 以写代读字段,方便前端展示
    
    role_id = Column(Integer, ForeignKey('role.id', ondelete='CASCADE'), comment="角色关联ID")
    role_name = Column(String(32), comment='角色名称')  # 以写代读字段,方便前端展示
    
    extra_info = Column(JSON, comment='补充信息')
    expire_time = Column(DateTime, comment='失效时间')
    
    def __init__(self, **kwargs):
        super(UserRoleRel, self).__init__(**kwargs)
