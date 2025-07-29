import random
import string
import time

db = None


def fetchone(query, *args, dict_cursor=True):
    data = db._fetchone(query, args, dict_cursor=dict_cursor)
    return data


def fetchall(query, *args, dict_cursor=True):
    return db._fetchall(query, args, dict_cursor=dict_cursor)


def execute(query, *args):
    rowcount = db._execute(query, [args])
    return rowcount


def execute_many(query, args):
    rowcount = db._execute(query, args)
    return rowcount


def generate_str(limit_length=50, start="autotest"):
    """生成唯一字符串,最大长度50，可指定小于50的长度"""
    print('generate_str:',limit_length,start)
    return f'{start}{round(time.time() * 1000)}{"".join(random.choices(string.hexdigits, k=42))}'[: int(limit_length)]


def random_choice(*values):
    """随机获取其中一个值"""
    return random.choice(values)


def other_choice(current_status, all_staus):
    """比方说当前current_status=1，all_status=[1,2,3,4],取[2,3,4]中的一个"""
    return random.choice([status for status in all_staus if status != current_status])


def random_sample(values, k=1, sep=None):
    """
    随机获取多个值,如果sep有值则返回字符串，否则返回列表
    ,作为解析参数的分割关键字，无法直接写到yml文件，这里直接通过
    """
    return (
        random.sample(values, int(k))
        if sep is None
        else f"{sep if sep != '~' else ','}".join([str(i) for i in random.sample(values, int(k))])
    )


def format_msg(msg):
    """
    多个字段报错时，顺序每次都不一致，转为字典进行比对
    :msg:多个字段报错格式，参考whId:仓库编码不能为空;whCode:仓库代码不能为空;timezone:时区不能为空;whStatus:状态不能为空
    :return {'whId:'仓库编码不能为空‘,'whCode:'仓库代码不能为空‘,...}
    """
    return {k.split(":")[0]: k.split(":")[1] for k in msg.split(";") if k.strip()}


def sub_dict_value(dict_data, keys):
    """
    获取字典部分键的值
    :params dict_data: {'a':2,'b':2,'c':3}
    :params key: ['a','b']
    :return {'a':2,'b':2}
    """
    return {k: dict_data[k] for k in keys}

def isinstance_of_obj(obj,_type='list'):
    """
    判断对象是否为列表
    :param obj:
    :return:
    """
    _type_map={'list':list,'tuple':tuple,'dict':dict,'int':int,'str':str,'float':float,'bool':bool,'none':None}
    return isinstance(obj, _type_map[_type])