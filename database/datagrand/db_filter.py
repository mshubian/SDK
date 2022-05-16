# -*- coding: utf-8 -*-

import json
import logging


class SingleFilter(object):
    """
    单条件Filter
    """
    
    column = None
    operator = None
    value = None
    
    def __init__(self, column=None, operator=None, value=None):
        if not (column and operator and value):
            logging.error("构造Filer的三个参数均不可为空，请检查")
            raise ValueError("invalid literal for SingleFilter() please check the __init__() requirement")
        
        if operator not in ["=", "!=", ">", ">=", "<", "<=", "in", "like", "is"]:
            raise ValueError("invalid operator for SingleFilter() please check operator validation")
        
        self.column = column
        self.operator = operator
        self.value = value
    
    def display(self):
        """
        辅助方法，辅助确认生成的但条件filter是否符合设计预期
        """
        return "%s %s %s" % (self.column.__name__, self.operator, str(self.value))


class MultiFilter(object):
    """
    多条件Filter
    """
    
    and_conditions = None
    or_conditions = None
    
    def __init__(self, and_conditions=None, or_conditions=None):
        """
        构造函数：支持两种方式：
            第一种：无参数声明的方式创建对象实例（声明式）
            第二种：通过具体参数内容直接构造对象实例（命令式）
        """
        if not and_conditions:
            self.and_conditions = []
        
        if not or_conditions:
            self.or_conditions = []
        
        # 如果通过构造函数生成对象，则需要对参数进行完整校验
        if and_conditions or or_conditions:
            self._check_init_args()
    
    def display(self):
        """
        辅助方法：辅助确认生成的多条件filter，以结构化的方式呈现条件组合结果形式
        """
        result = {
            "and_conditions": [],
            "or_conditions": []
        }
        
        for and_filter in self.and_conditions:
            result['and_conditions'].append(and_filter.display())
        
        for or_filter in self.or_conditions:
            result['or_conditions'].append(or_filter.display())
        
        return json.dumps(result, ensure_ascii=False, indent=4)
    
    def display_to_sql_condition(self):
        """
        辅助方法：辅助确认生成的多条件filter，以mock的方式展示sql语句的条件部分
        """
        result = "SELECT * FROM table WHERE 1=1"
        
        for and_condition in self.and_conditions:
            result += and_condition.display()
        
        for or_condition in self.or_conditions:
            result += or_condition.display()
    
    def _check_init_args(self):
        """
        验证构造函数的参数，保障生成MultiFilter有效合法

        主要支持以下几种方式：
        MultiFilter()

        只传一类条件：
        MultiFilter([SingleFilter1, ... SingleFilterN])   # 默认是and条件
        MultiFilter(and_conditions=[SingleFilter1, ... SingleFilterN])
        MultiFilter(or_conditions=[SingleFilter1, ... SingleFilterN])   #只传or条件必须参数名指定

        传两类条件：
        MultiFilter(SingleFilter，SingleFilter)                        # 1and+1or
        MultiFilter([SingleFilter1, ... SingleFilterN]，SingleFilter)  # 多and+多or
        MultiFilter([SingleFilter1, ... SingleFilterN]，SingleFilter)  # 多and+1or
        MultiFilter(SingleFilter, [SingleFilter1, ... SingleFilterN])  # 1and+多or

        """
        if type(self.and_conditions) == SingleFilter:
            self.and_conditions = [self.or_conditions]
        
        if type(self.or_conditions) == SingleFilter:
            self.or_conditions = [self.or_conditions]
        
        if len(self.and_conditions) + len(self.or_conditions) < 2:
            logging.fatal("构造MultiFiler的SingleFilter数量不应小于2，请检查")
            raise ValueError("invalid literal for MultiFilter() please check the __init__() requirement")
        
        for con in self.and_conditions + self.or_conditions:
            if type(con) != SingleFilter:
                logging.fatal("构造MultiFiler的参数内容不允许出现非SingleFilter对象元素，请检查")
                raise ValueError("invalid literal for MultiFilter() please check the __init__() requirement")
