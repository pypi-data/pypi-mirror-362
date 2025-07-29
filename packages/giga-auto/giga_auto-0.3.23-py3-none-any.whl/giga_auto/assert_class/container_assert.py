import json
import logging
from giga_auto.assert_class.common_assert import AssertCommon
from giga_auto.utils import deep_sort

logger = logging.getLogger('giga')


class AssertContainer():
    """
    容器断言工具类，提供对容器（如列表、字典等）的断言方法
    """
    @staticmethod
    def assert_starts_with(actual, prefix, msg=None):
        """
        断言actual以prefix开头
        """
        assert str(actual).startswith(
            str(prefix)), f"{msg or ''} \nAssert Starts With Failed: Expected prefix {prefix}, Actual:{actual}"

    @staticmethod
    def assert_ends_with(actual, suffix, msg=None):
        """
        断言actual以suffix结尾
        """
        assert str(actual).endswith(
            str(suffix)), f"{msg or ''} \nAssert Ends With Failed: Expected suffix {suffix}, Actual:{actual}"

    @staticmethod
    def assert_regex_match(actual, pattern, msg=None):
        import re
        assert re.match(pattern,
                        str(actual)), f"{msg or ''} \nAssert Regex Match Failed: Expected pattern {pattern}, Actual:{actual}"


    def assert_format(self, actual, expected):
        if isinstance(actual, str): actual = json.loads(actual)
        if isinstance(expected, str): expected = json.loads(expected)
        diff_key = self.diff_data(actual, expected)
        logger.info(f'格式断言actual:{actual},expected:{expected},diff_key:{diff_key}')
        # 如果diff_key为空，代表无任何格式异常，通过校验
        AssertCommon.assert_is_empty(diff_key, msg=f'格式断言actual:{actual},expected:{expected}')

    def assert_format_value_not_null(self, actual, expected):
        if isinstance(actual, str): actual = json.loads(actual)
        if isinstance(expected, str): expected = json.loads(expected)
        diff_key = self.diff_data(actual, expected, check_value=True)
        logger.info(f'格式断言actual:{actual},expected:{expected},diff_key:{diff_key}')
        # 如果diff_key为空，代表无任何格式异常，通过校验
        AssertCommon.assert_is_empty(diff_key, msg=f'格式断言actual:{actual},expected:{expected}')


    def diff_data(self, actual, expect, path='$', diff_key=None, check_value=False):
        if diff_key is None: diff_key = []
        if isinstance(expect, list):
            if type(actual) != list:
                diff_key.append(f'{path}该路径类型不一致')
            new_path = path + '.0'
            if isinstance(expect[0], list):
                self.diff_data(actual[0], expect[0], path=new_path, diff_key=diff_key, check_value=check_value)
            elif isinstance(expect[0], dict):
                self.diff_data(actual[0], expect[0], path=new_path, diff_key=diff_key, check_value=check_value)
            elif check_value and not actual[0]:
                diff_key.append(f'{new_path}该路径值不能为空')
        elif isinstance(expect, dict):
            if type(actual) != dict:
                diff_key.append(f'{path}该路径类型不一致')
            for k, v in expect.items():
                new_path = path + '.' + str(k)
                if k not in actual:
                    diff_key.append(f'{new_path}该路径key不存在期望格式中')
                elif isinstance(v, dict):
                    self.diff_data(actual[k], v, new_path, diff_key, check_value=check_value)
                elif isinstance(v, list):
                    self.diff_data(actual[k], v, new_path, diff_key, check_value=check_value)
                elif check_value and not actual[k]:
                    diff_key.append(f'{new_path}该路径值不能为空')
        return diff_key

    @staticmethod
    def assert_sorted_data(data, reverse=False):
        """
        利用sorted()辅助函数，用于判断数据是否按顺序排列
        """
        assert data == sorted(data, reverse=reverse)

    # 判断两个列表排序后是否相等
    @staticmethod
    def assert_sorted_equal(actual, expected, msg=None):
        """
        断言实际值和预期值在排序后是否相等，适用于多种数据结构（包括嵌套结构）

        :param actual: 实际值（支持 list, dict, tuple, set 等）
        :param expected: 预期值
        :param msg: 自定义错误信息
        :raises AssertionError: 如果排序后不相等
        """
        # 对数据进行深度排序
        actual_sorted = deep_sort(actual)
        expected_sorted = deep_sort(expected)
        assert actual_sorted == expected_sorted, \
            f"{msg or ''} \nSorted data mismatch:\nActual: {actual_sorted}\nExpected: {expected_sorted}"

    @staticmethod
    def assert_msg_code(response, expect):
        """统一校验响应码"""
        expect_msg = expect.get('msg') or expect.get('message')
        resp_msg = response.get('msg') or response.get('message')
        expect_code = expect.get('code')

        assert expect_code == response.get('code'), f"响应码校验失败: 预期 {expect_code}, 实际 {response.get('code')}"
        assert expect_msg == resp_msg, f"响应消息校验失败: 预期 {expect_msg}, 实际 {resp_msg}"

    @staticmethod
    def assert_msg(resp: dict, expect, msg=""):
        """通用响应msg断言"""
        response_msg = resp.get('msg') or resp.get('message')
        if isinstance(expect, str):
            expect_msg = expect
        elif isinstance(expect, dict):
            expect_msg = expect.get('msg') or expect.get('message')
        else:
            raise TypeError("expect参数类型错误")
        AssertCommon.assert_equal(response_msg, expect_msg,
                                 f"resp_msg: {response_msg},expect_msg: {expect_msg}, {msg}响应msg不符")

    @staticmethod
    def assert_code(resp: dict, expect: dict, msg=""):
        """通用响应code断言"""
        AssertCommon.assert_equal(resp.get('code'), expect.get('code'),
                                 f"resp_code: {resp.get('code')},expect_code: {expect.get('code')}, {msg}响应code不符")

    @staticmethod
    def assert_length(actual, expected, assert_method):
        """
        断言长度,如果一个为列表，另一个为数字或字符串等
        """
        if type(actual) != type(expected):
            actual_len = len(actual) if isinstance(actual, (list, tuple)) else int(actual)
            expected_len = len(expected) if isinstance(expected, (list, tuple)) else int(expected)
        else:
            actual_len, expected_len = len(actual), len(expected)
        assert_method(actual_len, expected_len, msg=f'比较actual:{actual},expected:{expected}长度相等')

    @staticmethod
    def assert_contains(actual, expected, msg=None):
        """
        判断期望是否在实际值中，适合模糊搜索字段匹配
        """
        assert expected in actual, f"{msg or ''} \nAssert Contains Failed: Expected {expected}, Actual:{actual}"


    @staticmethod
    def assert_deep_not_empty(value, msg=None):
        """
        断言值不为空，支持基本类型、字符串、列表、字典、集合以及列表中包含字典的情况。
        排除 None、空字符串、空列表、空字典、空集合。
        注意：该方法只支持最多二层嵌套的字典和列表。
        断言失败：
        ex: [[0,1],[None,1]] ，[None,1]
        [{a:1,b:2},{a:None,b:2}]，{a:None,b:2}
        {"a": None, "b": 2}
        """
        empty_conditions = [None, '', [], {}, set(), tuple()]

        def check_value(val):
            # 如果是列表，检查每个元素
            if isinstance(val, list):
                for item in val:
                    if isinstance(item, (list, dict)):
                        check_value(item)  # 递归检查
                    assert item not in empty_conditions, msg or "Value is empty"  # 断言元素不为空
            # 如果是字典，检查每个键值对
            elif isinstance(val, dict):
                for key, item in val.items():
                    if isinstance(item, (list, dict)):
                        check_value(item)  # 递归检查
                    assert item not in empty_conditions, msg or f"Key '{key}' value is empty"  # 断言值不为空
            # 对于其他类型，直接检查值
            assert val not in empty_conditions, msg or "Value is empty"

        # Start checking the value
        check_value(value)

