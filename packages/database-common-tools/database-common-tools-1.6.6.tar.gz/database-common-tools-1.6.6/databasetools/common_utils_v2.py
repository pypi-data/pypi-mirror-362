import hashlib
import requests
import bson.json_util
import json
from datetime import datetime, timedelta, timezone

class CommonUtils:

    def __init__(self, log):
        self.log = log

    def dump_load(self, fn):
        with open(fn, 'r') as f:
            try:
                jmap = json.loads(f.read())
                return dict(jmap)
            except Exception as e:
                self.log.error('exception ... {}\tfile={}'.format(e, fn))
                return dict()
    
    def dump_loads(self, value):
        try:
            return bson.json_util.loads(value)
        except Exception as e:
            self.log.error('exception ... {}\tvalue={}'.format(e, value))
            return dict()
        
    def unix_to_formatted_time(self, unix_timestamp):
        """
        将Unix时间戳转换为格式化的时间字符串
        :param unix_timestamp: Unix时间戳(以秒为单位)
        :return: 格式化的时间字符串，格式为'%Y-%m-%d %H:%M:%S'
        """
        dt_object = datetime.fromtimestamp(unix_timestamp)
        formatted_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')
        return formatted_time
    
    def unix_to_formatted_datetime(self, unix_timestamp, tz=timezone.utc):
        """
        将Unix时间戳转换为datetime对象并将微妙去掉
        :param unix_timestamp: Unix时间戳(以秒为单位)
        :param tz: Unix时间戳时区 默认为UTC时间
        :return: datetime对象去除微秒部分'
        """
        dt_object_utc = datetime.fromtimestamp(unix_timestamp, tz=tz).replace(microsecond=0)
        return dt_object_utc
    
    def unix_to_formatted_datetime_hours(self, unix_timestamp, tz=timezone.utc, hours_to_add=0):
        """
        将Unix时间戳转换为datetime对象并将微妙去掉
        :param unix_timestamp: Unix时间戳(以秒为单位)
        :param tz: Unix时间戳时区 默认为UTC时间
        :return: datetime对象去除微秒部分'
        """
        dt_object_utc = datetime.fromtimestamp(unix_timestamp, tz=tz).replace(microsecond=0)
        if hours_to_add != 0:
            dt_object_utc += timedelta(hours=hours_to_add)
        return dt_object_utc
    
    def get_unix_time(self, time_str):
        """
        将格式化的时间字符串转换为Unix时间戳
        :param time_str: 格式化的时间字符串，格式为'%Y-%m-%d %H:%M:%S'
        :return: Unix时间戳(以秒为单位)
        """
        if time_str:
            try:
                dt_obj = datetime.strptime(str(time_str), "%Y-%m-%d %H:%M:%S")
                unix_timestamp = int(dt_obj.timestamp())
                return unix_timestamp
            except ValueError as e:
                try:
                    dt_obj = datetime.strptime(str(time_str), "%Y-%m-%d")
                    unix_timestamp = int(dt_obj.timestamp())
                    return unix_timestamp
                except ValueError as e:
                    return 0
        else:
            return 0
    
    def image_exists_get(self, url, timeout=10, max_retries=3):
        """
        Check if an image exists at the given URL.
        
        :param url: Image URL
        :param timeout: Timeout for the request in seconds
        :param max_retries: Maximum number of retries
        :return: True if image exists, False otherwise
        """
        attempt = 0
        while attempt < max_retries:
            try:
                response = requests.get(url, timeout=timeout)
                if response.status_code == 200:
                    return True
                else:
                    return False
            except requests.RequestException as e:
                self.log.error('Check image exist error: '.format(e))
            attempt += 1
        return False

    def image_exists_head(self, url, timeout=10, max_retries=3):
        """
        Check if an image exists at the given URL.
        
        :param url: Image URL
        :param timeout: Timeout for the request in seconds
        :param max_retries: Maximum number of retries
        :return: True if image exists, False otherwise
        """
        attempt = 0
        while attempt < max_retries:
            try:
                response = requests.head(url, timeout=timeout)
                if response.status_code == 200:
                    return True
                else:
                    return False
            except requests.RequestException as e:
                self.log.error('Check image exist error: '.format(e))
            attempt += 1
        return False

    def parse_sql_result(self, cursor):
        """
        Parse SQL result from a cursor object and return as list of dictionaries.
        
        :param cursor: SQL cursor object
        :return: List of dictionaries with column names as keys
        """
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def calculate_md5(self, input):
        """
        计算输入字符串的MD5哈希值, 并返回32位的十六进制字符串
        :param input_string: 输入字符串
        :return: 32位的MD5十六进制字符串
        """
        if isinstance(input, str):
            # 创建MD5哈希对象
            md5 = hashlib.md5()
            # 更新哈希对象的输入内容
            md5.update(input.encode())
            # 获取十六进制表示的MD5哈希值，并去除特殊符号
            md5_hex = md5.hexdigest()
            # 去除MD5字符串中的特殊符号
            md5_cleaned = ''.join(c for c in md5_hex if c.isalnum())
            # 返回32位的MD5十六进制字符串（无特殊符号）
            return md5_cleaned[:32]
        else:
            self.log.error('input not str,please input type str!')

    def get_time_threshold(self, time_unit, interval):
        """
        根据传入的时间单位和时间间隔计算时间阈值。

        参数:
        :param time_unit (str): 时间单位，可以是 'minutes', 'hours', 'days' 等。
        :param interval (int): 时间间隔。

        返回值:
        :return: datetime: 计算得到的时间阈值。
        """
        # 获取当前时间并设置为北京时区,并精确到秒
        current_time = datetime.now(timezone.utc).replace(microsecond=0)

        # 根据传入的时间单位和间隔计算时间阈值
        if time_unit == 'minutes':
            time_threshold = current_time - timedelta(minutes=interval)
        elif time_unit == 'hours':
            time_threshold = current_time - timedelta(hours=interval)
        elif time_unit == 'days':
            time_threshold = current_time - timedelta(days=interval)
        else:
            self.log.error("不支持的时间单位。请使用 'minutes', 'hours' 或 'days'。")

        return time_threshold