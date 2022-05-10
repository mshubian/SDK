# -*- coding: utf-8 -*- #

import logging
import random

from datagrandSDK.mysql.v57 import init_mysql_sdk

from models import User, Role, UserRoleRel

"""
达观mysql-sdk工具使用步骤二：【初始化SDK以及操作mysql数据（读写）】

主要包含三个部分：
    第一部分：初始化mysql-SDK
    第二部分：调用SDK提供的常用方法读写数据库（样例展示增删改查四个基础方法）
    第三部分：Python+SDK联合完成多表操作(通过一个例子介绍)
    第四部分：生成sql语句，通过SDK推送至mysql服务端去执行

补充说明：
    第一部分：此动作应当在“服务初始化”时执行，可将初始化的结果对象mysql_client塞入全局变量中
            后续Service层或其他需要使用此client可从全局变量中快速获取

    第二部分：主要针对SDK提供常用工具类方法（增删改查）来对model对象（数据库单表数据）进行常用操作
             这个部分的代码主要在Service层多次出现，提供统一的一套工具函数来支撑不同service与数据的常规操作
             这个部分也是SDK使用的关键信息，请逐个吸收和理解，若碰到疑问请随时联系我们 (arch-team@datagrand.com)

    第三部分：主要通过一个例子示范Python代码+SDK完成跨表或联表的数据操作（查询操作）
             此部分主要通过SDK进行单表操作，通过python代码进行【串联】代码操作，整体完成多表联表查询等逻辑

    第四部分：主要针对一些复杂sql场景，通过生成sql直接交由MySQL执行（直接执行sql比python+SDK更加方便）
             此部分在一些涉及到统计计算（比如按不同维度来统计不同时间区间的同环比等），或批量更新等操作。
             Python也可以完成，但是就不如Mysql计算引擎本身去执行来的更加快捷。
"""

# 第一部分：通过制定的mysql连接配置信息，直接初始化SDK
mysql_client = init_mysql_sdk('mysql_config.json')


class UserService(object):
    
    # 第二部分：增加数据
    @staticmethod
    def add_user():
        """添加数据至mysql数据表中

        通过两种方式来创建对象，然后添加数据到mysql数据表中
            第一种：常规创建空属性对象，逐个属性赋值
            第二种：通过一个完整的字典数据，直接构建对象。（适合前端表单提交传过来已经是构建好的json直接生成目标对象）

        创建完成对象后，通过sdk的方法：add_object()及时生效插入至mysql数据表中。
        返回时，通过model对象的as_dict()方法，讲model对象转成dict数据，返回给调用方。
        """
        # 生成一个model对象,逐个赋值属性
        new_user1 = User()
        new_user1.name = "李雷"
        new_user1.phone = '18812345678'
        new_user1.sex = "男"
        new_user1.age = 25
        new_user1.height = 1.75
        new_user1.weight = 68.88
        new_user1.background = {
            "birth_date": "1997-01-01",
            "hobbies": "basketball"
        }
        
        logging.info("构建第一个user对象实例")
        
        # 通过一个结构化的字典数据来生成对象
        new_user2_properties = {
            "name": "韩梅梅",
            "phone": "19987654321",
            "sex": "女",
            "age": 23,
            "height": 1.68,
            "background": {
                "birth_date": "1999-01-01",
                "birth_city": "ShangHai"
            }
        }
        new_user2 = User(**new_user2_properties)
        
        logging.info("构建第二个user对象实例")
        
        # 调用SDK的方法add_object()来插入数据至Mysql的数据表中
        mysql_client.add_object(new_user1)
        mysql_client.add_object(new_user2)
        
        logging.info("数据库user表插入完成")
        
        # 调用model对象的as_dict()方法，将model数据转成dict数据返回给调用方
        return [
            new_user1.as_dict(),
            new_user2.as_dict()
        ]
    
    # 第二部分：删除数据
    @staticmethod
    def delete_user():
        """删除mysql数据表的数据（此方法为物理删除，若要实现逻辑删除改用update数据方法更新【标识字段】来代替）
            delete的操作此处介绍两种方式：
                第一种：调用delete_object()方法针对某个具体的model对象进行删除动作
                第二种：调用delete_all_object通过筛选条件进行删除动作
        """
        logging.info("第一种删除方法")
        
        # 第一种方式：针对一个明确的model对象(先获取), 进行定点删除动作
        user = mysql_client.get_first_object(User)
        mysql_client.delete_object(user)  # 直接生效至数据库表中
        
        logging.info("第二种删除方法-1：对应底层的query.filter()")
        # 第二种方式-1：通过查询条件进行删除，以下方法均可会直接在数据库中生效
        mysql_client.delete_all_objects(User, User.age > 30)
        mysql_client.delete_all_objects(User, User.sex == 30)
        mysql_client.delete_all_objects(User, User.age.in_([10, 20, 30, 40, 50, 60]))
        mysql_client.delete_all_objects(User, User.name.like('%%'))
        mysql_client.delete_all_objects(User, User.age == 30 and User.sex == '女')  # 逻辑组合条件
        mysql_client.delete_all_objects(User, User.age >= 30 or User.sex == '男')  # 逻辑组合条件
        
        logging.info("第二种删除方法-2：对应底层的query.filter_by()")
        # 第二种方式-2：针对等式判断也使用可稍简化一点的方法
        mysql_client.delete_all_objects_by(User, id=30)  # 等式查询
        mysql_client.delete_all_objects_by(User, age=40, sex='女')  # 联等式查询
        mysql_client.delete_all_objects_by(User, {"age": 40, "sex": "女"})  # 连等式dict查询条件
    
    # 第二部分：修改数据
    @staticmethod
    def update_user():
        """更新mysql数据表中的某一行（即某一个具体的model对象）的内容
            第一步：获取要更新的目标对象
            第二步：明确要更新那些column属性，以及要更新的目标结果值
            第三步：调用SDK的update_object()进行数据库更新操作
            第四步：可将更新的结果model对象调用as_dict()方法，返回给调用方

            补充说明，暂未提供批量删除的对象的直接工具方法。
            若真实场景碰到此需求，或可直接使用exec_sql()方法，也可将批量修改拆解为单个更新
        """
        # 明确要更新的目标对象，关于查询的部分下文再详细介绍，此处先简单跳过
        user = mysql_client.get_first_object(User)
        if not user:
            return
            
            # 明确要更新的内容, 此处应为要更新的目标结果内容
        update_content = {
            "name": "李雷",
            "description": "这是一段更新的内容，此处省去300字",
            "height": random.choice([1.65, 1.60, 1.70, 1.75]),
            "background": {
                "update_item1": "updated_value",
                "update_item2": "updated_value"
            }
        }
        
        # 调用SDK方法更新数据
        mysql_client.update_object(user, **update_content)
        
        # 将更新的结果数据，以dict对象返回给调用方
        return user.as_dict()
    
    # 第二部分：查询数据(根据条件筛选查询数据)
    @staticmethod
    def get_user_list():
        """查询数据

        主要是通过SDK提供的常用方法来操作数据库的数据表（主要是单表操作）

        同时针当前sqlalchemy的filter(非等式条件)和filter_by（纯等式条件），SDK也成对的提供两种查询方法给开发者
        开发者需事先理解二者的不同，根据实际的需要进行合理选择。以下提供一些选择思路：
            1. 写法上filter_by比filter更加简单直观（所见即所得），小条件查询更方便快捷：
                    user = get_first_object(User, User.phone == '18612345678', User.age == 18)
                    user = get_first_object_by(User, phone='18612345678', age=18)

            2. 适用范围上filter更广一些：filter_by主要支持等式和联等式判断，filter支持各种判断条件（非等式）
                    filter_by 不支持：小于/大于，like（模糊匹配），in（包含），or（或），等判断
                    filter 都支持，并且能用filter_by全都能够用filter重写，但反过来不可以。

            3. 支持场景上filter更加灵活一些：filter支持动态的查询条件，而filter_by相对来说对静态查询条件跟有好一些
                    例如在一个多维度和多属性的宽表查询时，用户可选的查询条件比较多，
                    这种情况下在后台就更适合根据入参，动态组装生成【查询条件元组】(*criterion), 然后操作数据库

            4. 从性能上，二者差异并不大。filter和filter_by最终都会转义成同一个"SQL语句"交给db_engine去执行。

        目前mysql-SDK提供的查询相关的方法如下。

            【单条数据查询】
            get_object
            get_first_object
            get_first_object_by

            【多条数据筛选查询：默认以倒序返回列表】
            get_all_objects(self, model_obj, *criterion)
            get_all_objects_by(self, model_obj, **kwargs)

            【分页筛选查询：默认以倒序返回制定长度的列表】
            get_all_objects_page(self, page_num, model_obj, page_size=100, *criterion)
            get_all_objects_page_by(self, page_num, model_obj, page_size=100, **kwargs)

            【分组查询：主要是在返回结果上增加一个“归集”维度】
            def get_all_objects_group(self, model_obj, group_by, *criterion)
            def get_all_objects_group_by(self, model_obj, *group_by, **kwargs)

            【统计计数：轻量统计】
            count(self, model_obj, *criterion)
            count_by(self, model_obj, **kwargs)

            【自定义排序查询：随着前端技术组件和设备性能的逐渐强大，排序工作也逐渐交由前端来进行】
            get_all_objects_order_by(self, model_obj, *order_by, **kwargs)

        :return: SDK返回的主要是model对象(列表), service可通过model.as_dict()方法来转成dict对象返回给调用方


        PS: 实际SDK仍然是可扩展增加工具函数的，基于当前Python轻应用平台开发需求应当满足
            使用过程中碰到若碰到需要扩展增加的，可先临时通过exec_sql()方法，同步也请随时与我们反馈，再行排期追加
        """
        
        # 查询单条数据
        user = mysql_client.get_object(User, 17)  # 根据主键ID直接查询返回model_Object
        user = mysql_client.get_first_object(User, User.phone == '18612345678' or User.name == '李雷' and User.age > 18)
        user = mysql_client.get_first_object_by(User, phone='18612345678', name='李雷')
        
        # 查询多条数据: 默认返回结果均以倒序返回
        condition = User.age == 30 or User.sex != '女' and User.create_time > '2022-01-01'
        user_list = mysql_client.get_all_objects(User, *condition)
        user_list = mysql_client.get_all_objects_by(User, age=30, set='男')
        user_list = mysql_client.get_all_objects_by(User, {"age": 30, "set": '男'})
        
        # 分页查询：2：页数，10：每页长度 (查询条件同上文介绍相一致)
        page_user_list = mysql_client.get_all_objects_page(User, 2, 10, User.sex == '男')
        page_user_list = mysql_client.get_all_objects_page_by(User, 2, 10, sex='男')
        
        # 分组查询：按照维度归集返回
        page_user_list = mysql_client.get_all_objects_group(User, User.age, User.sex == '男')  # filter只支持单层group_by
        page_user_list = mysql_client.get_all_objects_group_by(User, User.age, User.height, sex='男')  # 多层group_by
        
        # 统计计数：
        num = mysql_client.count(User, User.height > 1.60)
        num = mysql_client.count_by(User, height=1.60)
        
        # 对查询结果进行补充赋值或其他逻辑处理
        user_dict = user.as_dict()
        user_dict['additional_info'] = "增加信息"
        user_dict['work_years'] = user.age - 22  # 取值可直接对象.property的方式
        
        # 对于列表结果处理，可通过as_dict()方式进行整体转义成dict对象列表
        # return [logic_with_user(user) for user in user_list] # 也可以额外逻辑处理
        return [user.as_dict() for user in user_list]
    
    # 第三部分：综合类联表查询（涉及到多个表的操作）
    @staticmethod
    def get_role_user_list():
        """ 涉及多表关联信息的操作

            此需求主要基于user与role的【多对多】关联情况下返回一个完整的角色->用户的完整树形结构信息
            ER关系图主要为  user  <->  user_role_rel <-> role
            user_role_rel里面主要有关联到user的user_id，以及role表role_id

            最终返回结果格式为：
                [
                    {
                        role_id: 1
                        role_name: 角色1
                        user_num: 3
                        user_list_data:[
                            {用户1完整信息}，
                            {用户2完整信息}，
                            {用户3完整信息}
                        ]
                    },
                    ...
                    {
                    }
                ]
        """
        result = []
        
        # 获取所有角色
        role_list = mysql_client.get_all_objects(Role)
        for role in role_list:
            role_data = {
                "role_id": role.id,
                "role_name": role.name
            }
            
            # 获取此角色所关联的所有用户ID列表，从而获取此角色关联的所有用户信息
            rel_list = mysql_client.get_all_objects_by(UserRoleRel, role_id=role.id)
            user_id_list = [rel.user_id for rel in rel_list]  # 获取关联所有的user_id列表
            user_list = mysql_client.get_all_objects(User, User.id in user_id_list)  # 根据ID列表查询用户列表
            
            # 将用户列表信息塞入至角色信息中
            role_data['user_num'] = len(user_list)
            role_data['user_list_date'] = [user.as_dict() for user in user_list]
            
            # 完整的角色信息添加至返回结果列表中
            result.append(role_data)
        
        return result
    
    # 第四部分：更复杂的数据查询或数据处理相关(通过生成sql语句，交由mysql执行，获取其返回结果)
    @staticmethod
    def complex_sql_operation():
        # 模拟生成sql的方法
        def generate_sql():
            sql_str = "select sex, count(*) as a, sum(weight)/sum(height) as b, sum(height)/count(*) as c " \
                      "from user " \
                      "where create_time > '2021-01-01' " \
                      "group by sex"
            return sql_str
        
        exec_sql_str = generate_sql()
        
        """
        调用SDK提供的exec_sql()获取sql执行的返回结果,该方法的返回结果主要有三种：
            第一种：[{}], 表明SQL语句无返回结果，如执行的是个写操作(update语句)
            第二种：[{k:v},...,{k:v}], 表明SQL语句有返回结果，结果内容每行转义成一个{},最终整体以list返回
            第三种：None, 表明SQL执行报错，需查看Error日志，确认具体错误信息
        """
        result = mysql_client.exec_sql(exec_sql_str)
        if not result:
            logging.error("SQL语句执行出错，请检查错误日志！")
        
        return result


user_service = UserService()
