
class AssertCommon():

    @staticmethod
    def assert_equal(actual, expected, msg=None):
        """
        断言两个值相等
        """
        assert actual == expected, f"{msg or ''} \nAssert Equal Failed: Expected:{expected},Actual:{actual}"

    @staticmethod
    def assert_not_equal(actual, expected, msg=None):
        """
        断言两个值不相等
        """
        assert actual != expected, f"{msg or ''} \nAssert Not Equal Failed: Expected:{expected},Actual:{actual}"

    @staticmethod
    def assert_in(expected, actual, msg=None):
        """
        断言actual在expected中，支持字符串和列表
        """
        if isinstance(actual, list) and isinstance(expected, list):
            assert all(item in actual for item in expected), \
                f"{msg or ''} \nAssert In Failed: Expected items {expected} not all in Actual:{actual}"
        else:
            assert expected in actual, \
                f"{msg or ''} \nAssert In Failed: Expected:{expected}"

    @staticmethod
    def assert_not_in(expect, actual, msg=None):
        """
        断言actual不在expected中
        """
        if isinstance(actual, list) and isinstance(expect, list):
            assert all(item not in actual for item in expect), \
                f"{msg or ''} \nAssert In Failed: Expected items {expect} not all in Actual:{actual}"
        else:
            assert expect not in actual, f"{msg or ''} \nAssert Not In Failed"

    @staticmethod
    def assert_not_none(actual, msg=None):
        assert actual is not None, f"{msg or ''} \nAssert Not None Failed: Actual:{actual}"

    @staticmethod
    def assert_is_none(actual, msg=None):
        assert actual is None, f"{msg or ''} \nAssert Not None Failed: Actual:{actual}"

    @staticmethod
    def assert_true(actual, msg=None):
        assert actual is True, f"{msg or ''} \nAssert True Failed: Actual:{actual}"

    @staticmethod
    def assert_false(actual, msg=None):
        assert actual is False, f"{msg or ''} \nAssert False Failed: Actual:{actual}"

    @staticmethod
    def assert_equal_ignore_type(actual, expected, msg=None):
        try:
            # 尝试将两者作为数值进行比较
            assert float(actual) == float(
                expected), f"{msg or ''} \nAssert Equal (Ignore Type) Failed: Expected:{expected}, Actual:{actual}"
        except (ValueError, TypeError):
            # 如果无法转成 float，则回退到字符串比较
            assert str(actual) == str(
                expected), f"{msg or ''} \nAssert Equal (Ignore Type) Failed: Expected:{expected}, Actual:{actual}"

    @staticmethod
    def assert_is_empty(value, msg=None):
        assert value in (None, '', [], {}, set(), tuple()), f"{msg or ''} \nAssert Empty Failed: Actual:{value}"

    @staticmethod
    def assert_not_empty(value, msg=None):
        """
        断言值不为空
        """
        assert value not in [None, '', [], {}, set(), tuple()], f"{msg or ''} \nAssert Not Empty Failed: Actual:{value}"

    @staticmethod
    def assert_greater(actual, expected, msg=None):
        """
        断言actual大于expected
        """
        assert actual > expected, f"{msg or ''} \nAssert Greater Failed: Expected greater than {expected}, Actual:{actual}"

    @staticmethod
    def assert_greater_equal(actual, expected, msg=None):
        """
        断言actual大于expected
        """
        assert actual >= expected, f"{msg or ''} \nAssert Greater Failed: Expected greater or equal {expected}, Actual:{actual}"

    @staticmethod
    def assert_less(actual, expected, msg=None):
        """
        断言actual小于expected
        """
        assert actual < expected, f"{msg or ''} \nAssert Less Failed: Expected less than {expected}, Actual:{actual}"

    @staticmethod
    def assert_less_equal(actual, expected, msg=None):
        """
        断言actual小于expected
        """
        assert actual <= expected, f"{msg or ''} \nAssert Less Failed: Expected less or equal {expected}, Actual:{actual}"

    @staticmethod
    def assert_between(actual, min_value, max_value, msg=None):
        """
        断言actual在min_value和max_value之间
        """
        assert min_value <= actual <= max_value, f"{msg or ''} \nAssert Between Failed: Expected between {min_value} and {max_value}, Actual:{actual}"



