from datetime import datetime, timedelta, timezone


def get__date_utc(date: str, pattern='%Y-%m-%d', replace_with_nowtime=False):
    """
    获取指定日期的UTC的时间字符串

    Args:
        date: 指定日期
        pattern: 日期格式
        replace_with_nowtime: 是否将时间替换为当前时间
    """

    shanghai_tz = timezone(timedelta(hours=8))

    dp = datetime.strptime(date, pattern).replace(tzinfo=shanghai_tz)
    if replace_with_nowtime is True:
        now = datetime.now(shanghai_tz)
        dp = dp.replace(
            hour=now.hour,
            minute=now.minute,
            second=now.second,
            microsecond=now.microsecond,
        )

    utc_time = dp.astimezone(timezone.utc).isoformat(timespec='milliseconds')
    return utc_time.replace('+00:00', 'Z')
