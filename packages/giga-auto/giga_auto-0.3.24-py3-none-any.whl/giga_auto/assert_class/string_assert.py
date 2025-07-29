
class AssertString():

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
