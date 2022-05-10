# Mysql-SDK

## 关键依赖组件版本信息

| 组件        | 版本          |说明|
|:--------:|:-------------:|:-----|
| Python | 3.6 | 可兼容python3.X版本，若出现不兼容情况请及时反馈 |
| MySQL | 5.7|推荐版本，5.7之后支持JSON类型字段，表设计扩展性较好  |
| MySQL-Python | 1.4.6 |whl二进制文件快捷安装：https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysql-python |
| sqlalchemy | 1.4.36| pip源安装，保持大版本一致即可，若出现不兼容情况请及时反馈 |

# 使用方法

## 第零步：安装datagrandSDK以及准备Mysql的配置文件

`【SDK安装临时方案】`: 手动下载SDK源码，文件夹至python的site-package文件夹中   
或采取其他，将代码文件夹以本地库的方式加入到项目Project中也可以达到同样效果

```
wget http://datagrand.com/dowload/datagrandSDK.tar.gz
tar -zxvf datagrandSDK.tar.gz -C /usr/lib/python3.6/site-packages
```

**【SDK安装目标方案】**：从pip源中直接下载 `(TODO:datagrandSDK发布至PyPi)`

```
pip3 install -U datagrandSDK
```

**【Mysql配置文件】**：主要格式内容如下
```json
{
    "mysql": {
        "host": "127.0.0.1",
        "port": 3306,
        "database": "test-sdk",
        "username": "sdk",
        "password": "awesome",
        "charset": "utf8"
    }
}
```

## 第一步：定义model(定义数据表)

基于SDK中提供的BaseModel进行自定义需要的model。而BaseModel，实际是基于SqlAlchemy的declarative_base()封装而来。   
请看代码：`通过一个model定义举例，实际可自定义多个，可参考样例代码提供的内容`

```python
# -*- coding: utf-8 -*-

from datagrandSDK.mysql.v57.mysql_model import BaseModel, Column
from datagrandSDK.mysql.v57.mysql_model import Integer, Float, String, Text, DateTime, JSON, ForeignKey


# 定义model(mysql数据表)对象
class User(BaseModel):
    __tablename__ = 'user'
    
    """
    补充说明：其中BaseModel里面定义了5个基础对象：id,name,description,create_time,update_time
    经此定义，实际user表最终包含5+6=11个字段属性
    """
    
    phone = Column(String(16), nullable=False, unique=True, comment='手机号')
    sex = Column(String(4), comment='性别')
    age = Column(Integer, comment='年龄')
    height = Column(Float(precision="2,2"), comment='身高(m)')
    weight = Column(Float(precision="4,2"), comment='体重(KG)')
    background = Column(JSON, comment='背景信息')
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
```

## 第二步：调用SDK工具方法创建mysql数据表(或更新表结构)

SDK中的utils工具类中已提供setup_db_table()方法,该方法会自动获取所有`基于BaseModel定义`的所有models。   
然后在mysql服务端逐个创建, 当碰到`表名已存在(重复)`的情况下会自动跳过。 关于具体使用的补充说明如下：

```
1. 创建表结构，调用utils.setup_db_table()，主要在搭建开发环境或部署阶段使用
2. 更新表结构，调用utils.update_db_schema()，主要在开发和升级过程中出现model定义更新的情况
3. 以上两个方法均需要提供mysql_config.json配置文件的【文件路径】作为入参
4. setup_db_table(已完成)和update_db_schema(进行中)均为可独立直接执行的工具方法，内部实际已包含初始化SDK的动作
5. 创建表或更新表这两个动作，实际也可以人工执行如DDL语句执行，或sql导入等方式方法.最终保证model定义与数据表相一致即可
```

请看代码
```python
import logging

from datagrandSDK.mysql.v57.utils import setup_db_table

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='[%Y%m%d|%H:%M:%S]')
    
    setup_db_table('./mysql_config.json')
```

运行后正常即可出现如下日志信息：

```bash
[20220508|16:32:34] INFO 读取Mysql配置文件
[20220508|16:32:34] INFO ................成功
[20220508|16:32:34] INFO 数据库链接成功
[20220508|16:32:34] INFO 开始创建mysql数据表
[20220508|16:32:34] INFO ..................创建完成
```

在数据库中即可看到实际的表结构信息，如下：

### 第三步：初始化SDK

SDK已提供一个完整的初始化函数init_mysql_sdk()，给定`mysql_config.json`文件路径作为入参，该函数返回SDK的工具类实例。   
该工具类则提供日常实际开发中，以ORM方式与数据库进行交互操作的最常用的工具方法（下文将做具体介绍）。额外补充说明如下：

```
1. 初始化SDK的实际操作就是一行代码即可，主要在服务或代码运行初始化的环节处执行此动作
2. 若在后端服务框架中可考虑在初始化环节生成sdk对象实例，然后塞入全局变量中，方便后续不同代码层次的地方来使用sdk
3. 随着SDK的持续迭代更加强大，兴许会对init_mysql_sdk()方法进行升级，二者需同步进行
```

请看代码：
```python
import logging

from datagrandSDK.mysql.v57 import init_mysql_sdk

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='[%Y%m%d|%H:%M:%S]')
    
    mysql_client = init_mysql_sdk('./mysql_config.json')
```

正常运行即可出现如下日志：
```bash
[20220508|16:32:34] INFO 开始初始化加载datagrand-mysql-sdk
[20220508|16:32:34] INFO 读取Mysql配置文件
[20220508|16:32:34] INFO ................成功
[20220508|16:32:34] INFO 连接接数据库
[20220508|16:32:34] INFO ...........成功
[20220508|16:32:34] INFO datagrand-mysql-sdk加载完成
```

初始化完成之后即可使用SDK，请参考![SDK函数方法列表]()
下文将开始介绍`如何使用mysql_client`

### 第四步：通过SDK操作mysql数据（读写数据）

SDK中提供了整体围绕`单表`的**增**，**删**，**改**，**查**等常用操作   
同时也会介绍如何通过Python+SDK联合完成`多表关联操作`,以及提供`执行原生sql`的方式提升SDK的适用范围。

#### 单表：增加数据

通过两种方式来创建对象，然后添加数据到mysql数据表中 第一种：常规创建空属性对象，逐个属性赋值 第二种：通过一个完整的字典数据，直接构建对象。（适合前端表单提交传过来已经是构建好的json直接生成目标对象）

创建完成对象后，通过sdk的方法：add_object()及时生效插入至mysql数据表中。 返回时，通过model对象的as_dict()方法，讲model对象转成dict数据，返回给调用方。

#### 单表：删除数据

#### 单表：修改数据

#### 单表：查询数据

#### 多表：查询数据

#### 其他：通用sql操作

```
主要包含四个部分个部分：
    第一部分：初始化mysql-SDK
    第二部分：调用SDK提供的常用方法读写数据库（样例展示增删改查四个基础方法）
    第三部分：Python+SDK联合完成多表操作(通过一个例子介绍)
    第四部分：生成sql语句，通过SDK推送至mysql服务端去执行

补充说明：
    第一部分：此动作实际就一行代码即可，需事先确认mysql的配置文件
            主要在“服务初始化”时执行，可将初始化的结果对象mysql_client塞入全局变量中
            后续Service层或其他需要使用此client可从全局变量中快速获取
           
    第二部分：主要针对SDK提供常用工具类方法（增删改查）来对model对象（数据库单表数据）进行常用操作
             这个部分的代码主要在Service层多次出现，提供统一的一套工具函数来支撑不同service与model对象数据的常规操作
             这个部分也是SDK使用的关键信息，请逐个吸收和理解，若碰到疑问请随时联系我们 (arch-team@datagrand.com)

    第三部分：主要通过一个例子示范Python代码+SDK完成跨表或联表的数据操作（查询操作）
             此部分主要通过SDK进行单表操作，通过python代码进行【串联】代码操作，整体完成多表联表查询等逻辑
    
    第四部分：主要针对一些复杂sql场景，通过生成sql直接交由MySQL执行（直接执行sql比python+SDK更加方便）
             此部分在一些涉及到统计计算（比如按不同维度来统计不同时间区间的同环比等），或批量更新等操作。
             Python也可以完成，但是就不如Mysql计算引擎本身去执行来的更加快捷。
```