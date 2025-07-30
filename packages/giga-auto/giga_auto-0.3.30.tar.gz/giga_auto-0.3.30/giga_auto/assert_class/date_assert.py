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


    @staticmethod
    def assert_time_difference_within_days(
            start_time_str: str,
            timezone: str = "America/Los_Angeles",
            max_days: int = 1,
            end_time_str: str = None,
            time_format = "%Y-%m-%d %H:%M:%S",
            end_time_format: str = None,

    ):
        """
        断言两个时间（start_time, end_time）之间的相差天数小于 max_days。
        若不提供 end_time，则默认为当前时间。
        :param start_time_str: 起始时间字符串（如 '2025-06-18 15:00:00'）
        :param time_format: 起始时间格式（如 '%Y-%m-%d %H:%M:%S'）
        :param timezone: 时区名（如 'America/Los_Angeles'）默认为美西时间
        :param max_days: 最大允许的天数差
        :param end_time_str: 可选，对比时间字符串（如 '2025-06-19 15:00:00'），如果不提供则默认为当前时间
        :raises AssertionError: 如果相差天数大于 max_days
        :param end_time_format : 可选，对比时间格式（如 '%Y-%m-%d %H:%M:%S'），如果不提供则使用与起始时间相同的格式
        """
        import pytz
        tz = pytz.timezone(timezone)

        # 解析开始时间
        naive_start_time = datetime.datetime.strptime(start_time_str, time_format)
        start_time = tz.localize(naive_start_time)

        # 解析结束时间或使用当前时间
        if end_time_str:
            fmt = end_time_format or time_format
            naive_end_time = datetime.datetime.strptime(end_time_str, fmt)
            end_time = tz.localize(naive_end_time)
        else:
            end_time = datetime.datetime.now(tz)

        # 计算时间差
        delta = end_time - start_time

        assert datetime.timedelta(days=max_days) < delta, \
            f"时间差超出允许范围: 最大允许 {max_days} 天，实际时间差 {delta.days} 天"