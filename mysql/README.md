# Mysql-SDK

# MySQL-Client对外提供的方法列表
| 函数方法     |  简介 | 入参说明 |返回结果|
|:--------|:----|:---------|:-----|
| add_object | 新增单条数据 | Model对象的具体实例 | 无返回结果 |
| | | | |
| delete_object | 删除单条数据 | Model对象的具体实例 | 无返回结果|
| delete_all_object | 删除多条数据 | Model对象,</br>filter式 匹配条件 | 无返回结果 |
| delete_all_object_by | 删除多条数据 | Model对象,</br>filter_by式 匹配条件 |无返回结果|
| | | | |
| update_object | 更新单条数据 | Model对象的具体实例,</br>{更新目标字段和目标值} | 无返回结果 |
| | | | |
| get_object |  |  |  |
| get_first_object |  |  |  |
| get_first_object_by |  |  |  |
| get_all_objects |  |  |  |
| get_all_objects_by |  |  |  |
| get_all_objects_page |  |  |  |
| get_all_objects_page_by |  |  |  |
| get_all_objects_group |  |  |  |
| get_all_objects_group_by |  |  |  |
| count |  |  |  |
| count_by |  |  |  |
| get_all_objects_order_by| | | |
| | | | |
| exec_sql| | | |

【单条数据查询】 get_object get_first_object get_first_object_by

【多条数据筛选查询：默认以倒序返回列表】 get_all_objects(self, model_obj, *criterion)
get_all_objects_by(self, model_obj, **kwargs)

【分页筛选查询：默认以倒序返回制定长度的列表】 get_all_objects_page(self, page_num, model_obj, page_size=100, *criterion)
get_all_objects_page_by(self, page_num, model_obj, page_size=100, **kwargs)

【分组查询：主要是在返回结果上增加一个“归集”维度】 def get_all_objects_group(self, model_obj, group_by, *criterion)
def get_all_objects_group_by(self, model_obj, *group_by, **kwargs)

【统计计数：轻量统计】 count(self, model_obj, *criterion)
count_by(self, model_obj, **kwargs)

【自定义排序查询：随着前端技术组件和设备性能的逐渐强大，排序工作也逐渐交由前端来进行】 get_all_objects_order_by(self, model_obj, *order_by, **kwargs)