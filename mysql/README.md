# Mysql-SDK

> Tips: 在看此文档之前,请先阅读[MysqlSDK使用介绍][1]

# 关键依赖组件版本信息

| 组件        | 版本          |说明|
|:--------:|:-------------:|:-----|
| Python | 3.6 | 可兼容python3.X版本，若出现不兼容情况请及时反馈 |
| MySQL-Python | 1.4.6 |whl二进制文件快捷安装：https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysql-python |
| sqlalchemy | 1.4.36| pip源安装，保持大版本一致即可，若出现不兼容情况请及时反馈 |
| MySQL | 5.7 | 推荐版本，5.7之后支持JSON类型字段表设计扩展性较好</br>实际SDK对数据库支持与sqlalchemy保持一致|

# Mysql-SDK 代码文件结构

```
datagrandSDK
├── __init__.py
├── LICENSE
├── README.md
├── mysql
│     ├── README.md
│     └── v57
│          ├── __init__.py       # SDK初始化相关方法
│          ├── mysql_client.py   # 针对mysql数据表相关的读写数据操作工具类
│          ├── mysql_model.py    # 基于sqlalchemy的Base封装出的BaseModel定义类
│          └── utils.py          # SDK其他工具方法类（创建表等）
```

# SDK 主要对外提供方法/类的列表

| 类型 |  名称 | 介绍说明 |
|:----------------:|:----|:-----------------|
|工具方法|init_mysql_sdk() |通过mysql配置文件初始化SDK, 返回SQLAlchemyAdapter结果实例| 
|工具方法|utils.setup_db_table() |通过提供的mysql配置文件,创建所有基于BaseModel定义的数据表| 
|工具方法|utils.update_db_schema() |【开发中】</br>通过提供的mysql配置文件,基于Model最新定义来更新表结构|
|模型基类|mysql_model.BaseModel | 基于sqlalchemy Base封装而来的Model定义基类</br>开发者需基于此BaseModel定义出自己的Model | 
|工具类|mysql_client.SQLAlchemyClient | 结合sqlalchemy的ORM,基于BaseModel提供的一套操作工具类.</br>开发者从init_mysql_sdk()初始化返回结果即为此工具类的实例结果 | 

# mysql-client 对外提供的方法列表

```
SQLAlchemyClient为整个SDK中最为常用的工具方法类，通过设计比较通用和泛化的方法来方便开发者的使用
同时，也是根据日常常用需求而进行持续迭代，大家可以一起加入进来帮助完善此SDK
```

| 函数方法     |  简介 | 入参说明 |返回结果| 方法说明 |
|:--------|:----|:---------|:-----|:-----|
| add_object | 新增单条数据 | Model对象的具体实例 | 无返回结果 ||
| | | | | |
| delete_object | 删除单条数据 | Model对象的具体实例 | 无返回结果||
| delete_all_object | 删除多条数据 | Model对象,</br>filter式 匹配条件 | 无返回结果 ||
| delete_all_object_by | 删除多条数据 | Model对象,</br>filter_by式 匹配条件 |无返回结果||
| | | | | |
| update_object | 修改单条数据 | Model对象的具体实例,</br>dict() | 无返回结果 | 入参中dict为要更新的目标字段及其目标值 |
| | | | | |
| get_object | 查询单条数据 | Model对象</br>主键 | Model结果实例 |  |
| get_first_object | 查询单条数据 | Model对象,</br>filter式 匹配条件 | Model结果实例 | |
| get_first_object_by | 查询单条数据 | Model对象,</br>filter_by式 匹配条件 | Model结果实例 | |
| get_all_objects | 查询多条数据 | Model对象,</br>filter式 匹配条件 | List<Model结果实例> | 默认ID倒序 |
| get_all_objects_by | 查询多条数据 | Model对象,</br>filter_by式 匹配条件 | List<Model结果实例> | 默认ID倒序 |
| get_all_objects_order_by| 自定义排序 | Model对象,</br>目标排序字段</br>filter_by式 匹配条件 | List<Model结果实例> | 按目标字段排序|
| get_all_objects_page | 分页查询 | Model对象,</br>目标页数</br>每页长度</br>filter式 匹配条件 | List<Model结果实例> | 默认ID倒序 |
| get_all_objects_page_by | 分页查询 | Model对象,</br>目标页数</br>每页长度</br>filter_by式 匹配条件 | List<Model结果实例> | 默认ID倒序 |
| get_all_objects_group | 分组查询 | Model对象,</br>分组字段</br>filter式 匹配条件 | List<Model结果实例> | 默认ID倒序|
| get_all_objects_group_by | 分组查询 | Model对象,</br>分组字段</br>filter_by式 匹配条件 | List<Model结果实例> | 默认ID倒序|
| count | 统计数量 | Model对象,</br>filter式 匹配条件 | Int |  |
| count_by | 统计数量 | Model对象,</br>filter_by式 匹配条件 | Int |  |
| | | | |  |
| exec_sql| 执行原生sql| String | [{}] </br> [{},{},{}] </br> None| 根据实际的sql结果返回不同的格式</br>注意：`None为sql执行异常状态`|

具体实现，请转至代码内部详探 ~

[1]: https://github.com/mshubian/datagrandSDK/tree/main/sdk_usage_examples/mysqlv57-sdk-usage
