# -*- coding: utf-8 -*- #

from datagrandSDK.mysql.v57.mysql_model import BaseModel, Column
from datagrandSDK.mysql.v57.mysql_model import Integer, Float, String, Text, DateTime, JSON, ForeignKey

"""
达观mysql-sdk工具使用步骤一：【model定义以及创建表】

主要包含两个动作：
    1. model定义
    2. 调用SDK中提供的setup_db工具函数，在mysql服务端创建数据表

补充说明：
    1. model定义：此部分正常应当有一个独立的文件，把所有表模型的定义放在一处，此样例只定义两个model的对象来做参考
    2. 创建表：此动作实主要在开发或部署阶段使用（包含初创表，以及表升级）
              同时创建(更新)表的动作也可人工代替如：DDL语句执行，或sql导入等方式方法
              另外：此步骤用到的setup_db工具函数实际内置包含了SDK初始化的动作，具体将会在步骤二中进行介绍，此处先略过
"""


class User(BaseModel):
    """
    model定义: 用户表

    BaseModel中已包含常规默认的5个属性如下：
        id = Column(Integer, primary_key=True, autoincrement=True)
        name = Column(String, comment="名称")
        description = Column(Text, comment="备注描述")
        create_time = Column(DateTime, default=datetime.now, comment="修改时间")
        update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="最近修改时间", index=True)

    每个模型的定义基于表设计进行实际填充字段。（当然，BaseModel里面的字段仍然是可以重新定义的）
    最终User表对象包含5+6=11个column字段
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
