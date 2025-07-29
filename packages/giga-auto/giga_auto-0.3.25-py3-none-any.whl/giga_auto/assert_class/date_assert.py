import datetime
from giga_auto.utils import to_date



class AssertDete():
    @staticmethod
    def assert_date_equal(expected, actual):
        """
        通用日期比较方法，支持 str、datetime、date 类型，精确度到天
        """
        expected_date = to_date(expected)
        actual_date = to_date(actual)

        assert expected_date == actual_date, f"Expected: {expected_date}, Actual: {actual_date}"

    @staticmethod
    def assert_time_range(start_time, end_time, actual_time, msg=None):
        """
        断言时间范围
        """
        start_time = to_date(start_time)
        end_time = to_date(end_time)
        actual_time = to_date(actual_time)
        assert start_time <= actual_time <= end_time, f"{msg or ''} \nAssert Time Range Failed: Expected between {start_time} and {end_time}, Actual:{actual_time}"

    @staticmethod
    def assert_date_has_overlap(period1, period2, label='', msg=None):
        # 将字符串转换为 datetime 对象
        if isinstance(period1, str):
            period1 = period1.split(label)
        if isinstance(period2, str):
            period2 = period2.split(label)
        start1, end1 = map(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"), period1)
        start2, end2 = map(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"), period2)
        # 判断是否有交集
        assert max(start1, start2) <= min(end1,
                                          end2), f"{msg or ''} \nAssert Date Has Overlap Failed: Expected no overlap, Actual:{period1} and {period2}"
