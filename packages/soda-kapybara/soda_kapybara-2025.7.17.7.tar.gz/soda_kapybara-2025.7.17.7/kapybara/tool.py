import difflib
import time
from datetime import datetime, date, timedelta

import numpy as np
import pandas as pd
from pandas import Timestamp
from selenium.common import StaleElementReferenceException


def is_drug_name_similar(drug_name, drug_names_set, threshold=0.8):
    """
    判断一个药物名称是否与集合中的任何药物名称相似。

    :param drug_name: 当前待检查的药物名称
    :param drug_names_set: 已知药物名称的集合
    :param threshold: 相似度阈值，默认0.8
    :return: 如果相似的药物存在，则返回True，否则返回False
    """
    for name in drug_names_set:
        # 计算相似度
        similarity = difflib.SequenceMatcher(None, drug_name, name).ratio()

        # 如果相似度达到阈值，返回True
        if similarity >= threshold:
            return True

    # 如果没有找到相似药物，返回False
    return False


def safe_find_element(driver, by, value, retries=3):
    for attempt in range(retries):
        try:
            return driver.find_element(by, value)
        except StaleElementReferenceException:
            if attempt < retries - 1:
                time.sleep(1)  # 等待一会再重试
            else:
                raise


# 定义一个处理不同类型的安全比较函数
def safe_key(value):
    # 将所有值转换为字符串进行比较
    # 如果是 Timestamp 类型，先转换为字符串
    if isinstance(value, pd.Timestamp):
        return str(value)  # 你可以根据需要调整格式
    return str(value)  # 将其他类型转换为字符串


def process_date(new_sf_time) -> str:
    """
    处理日期字符串或 datetime 对象，返回格式化后的日期字符串。
    """
    # 判断 new_sf_time 是否为 datetime 对象
    if isinstance(new_sf_time, datetime):
        # 如果是 datetime 对象，直接进行格式化
        return new_sf_time.strftime('%Y-%m-%d')

    # 如果是字符串，检查是否符合日期格式
    elif isinstance(new_sf_time, str):
        try:
            # 尝试解析不同的日期格式
            # 假设日期格式有几种常见的格式，可以根据需求调整
            if (
                len(new_sf_time) == 10
                and new_sf_time[4] == '-'
                and new_sf_time[7] == '-'
            ):
                # 格式为 'YYYY-MM-DD'
                new_sf_time = datetime.strptime(new_sf_time, '%Y-%m-%d')
                return new_sf_time.strftime('%Y-%m-%d')
            elif (
                len(new_sf_time) == 19
                and new_sf_time[4] == '-'
                and new_sf_time[7] == '-'
                and new_sf_time[10] == ' '
            ):
                # 格式为 'YYYY-MM-DD HH:MM:SS'
                new_sf_time = datetime.strptime(new_sf_time, '%Y-%m-%d %H:%M:%S')
                return new_sf_time.strftime('%Y-%m-%d')
            else:
                raise ValueError('不支持的日期格式')
        except ValueError as e:
            return str(e)

    # 如果既不是字符串也不是 datetime 对象，返回错误信息
    return '输入无效'


def calculate_age(birthdate):
    """根据出生日期计算精确年龄（年、月、日）"""
    today = datetime.today()
    age = today.year - birthdate.year

    # 如果今年生日还没过，年龄减1
    if (today.month, today.day) < (birthdate.month, birthdate.day):
        age -= 1

    return age


def parse_date(date_value):
    """
    通用日期解析函数（支持12种日期格式）
    支持类型：
    - Pandas Timestamp
    - Python datetime/date
    - numpy.datetime64
    - 字符串（多种格式）
    - Excel序列日期数字
    - Unix时间戳
    """
    # 处理空值
    if pd.isnull(date_value):
        raise ValueError('输入日期值为空')

    # 类型1：Pandas Timestamp
    if isinstance(date_value, Timestamp):
        return date_value.to_pydatetime().replace(tzinfo=None)

    # 类型2：Python datetime对象
    if isinstance(date_value, datetime):
        return date_value

    # 类型3：Python date对象
    if isinstance(date_value, date):
        return datetime.combine(date_value, datetime.min.time())

    # 类型4：numpy.datetime64
    if isinstance(date_value, np.datetime64):
        return date_value.astype('datetime64[ns]').to_pydatetime()

    # 类型5：字符串日期
    if isinstance(date_value, str):
        # 去除前后空格和特殊字符
        clean_str = date_value.strip().replace('/', '-').replace('\\', '-')

        # 尝试常见日期格式
        formats = [
            '%Y-%m-%d',  # 2023-08-15
            '%Y%m%d',  # 20230815
            '%d-%m-%Y',  # 15-08-2023
            '%m-%d-%Y',  # 08-15-2023
            '%Y-%m-%d %H:%M',  # 2023-08-15 14:30
            '%Y/%m/%d',  # 2023/08/15
            '%d.%m.%Y',  # 15.08.2023
            '%Y年%m月%d日',  # 2023年08月15日
        ]

        for fmt in formats:
            try:
                return datetime.strptime(clean_str, fmt)
            except ValueError:
                continue

    # 类型6：Excel序列日期（整数/浮点数）
    try:
        if 0 < float(date_value) < 100000:
            # Excel日期从1900-01-01开始（Windows版本）
            return datetime(1899, 12, 30) + timedelta(days=float(date_value))
    except (ValueError, TypeError):
        pass

    # 类型7：Unix时间戳（秒/毫秒）
    try:
        ts = float(date_value)
        if 1e9 < ts < 2e12:  # 范围：2001-2033年
            return datetime.fromtimestamp(ts / 1000 if ts > 1e12 else ts)
    except (ValueError, TypeError):
        pass

    # 类型8：日期时间字符串（带时区）
    if isinstance(date_value, str) and 'T' in date_value:
        try:
            return datetime.fromisoformat(date_value.replace('Z', '+00:00'))
        except ValueError:
            pass

    # 最终尝试：dateutil解析（需要安装python-dateutil）
    try:
        from dateutil.parser import parse

        return parse(date_value)
    except ImportError:
        pass
    except (ValueError, OverflowError):
        pass

    raise ValueError(f'无法解析的日期格式：{type(date_value)} - {date_value}')
