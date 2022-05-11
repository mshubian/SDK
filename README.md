# DataGrand-SDK

# Python开发组件SDK

# 介绍说明

```
事项背景（为什么要做这个SDK）
预期目标（达到什么样的目标期望）
预期计划（大致的交付计划）
参与人员（开发运维推广组织成员）
```

# SDK安装

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

# SDK主要构成部分

* 数据库
    * MySQL-SDK
        * ![src code](https://github.com/mshubian/datagrandSDK/tree/main/mysql)
        * ![usage description](https://github.com/mshubian/datagrandSDK/tree/main/sdk_usage_examples/mysqlv57-sdk-usage)
    * Oracle-SDK
        * src code : TODO
        * usage description : TODO
    * Dameng-SDK
        * src code : TODO
        * usage description : TODO
* 消息队列
    * Kafka-SDK
        * src code : TODO
        * usage description : TODO
* 缓存服务
    * Redis-SDK 
        * src code : TODO
        * usage description : TODO