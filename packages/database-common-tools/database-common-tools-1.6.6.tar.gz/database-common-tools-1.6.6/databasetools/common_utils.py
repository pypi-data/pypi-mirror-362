import hashlib
import requests
import logging
from logging import handlers
import bson.json_util
import json
from datetime import datetime

class CommonUtils:

    @staticmethod   
    def dump_load(fn, log):
        with open(fn, 'r') as f:
            try:
                jmap = json.loads(f.read())
                return dict(jmap)
            except Exception as e:
                log.error('exception ... {}\tfile={}'.format(e, fn))
                return dict()
    
    @staticmethod
    def dump_loads(value, log):
        try:
            return bson.json_util.loads(value)
        except Exception as e:
            log.error('exception ... {}\tvalue={}'.format(e, value))
            return dict()
        
    @staticmethod
    def unix_to_formatted_time(unix_timestamp):
        """
        将Unix时间戳转换为格式化的时间字符串
        :param unix_timestamp: Unix时间戳(以秒为单位)
        :return: 格式化的时间字符串，格式为'%Y-%m-%d %H:%M:%S'
        """
        dt_object = datetime.fromtimestamp(unix_timestamp)
        formatted_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')
        return formatted_time
    
    @staticmethod
    def get_unix_time(time_str):
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
    
    @staticmethod
    def image_exists_get(url, log, timeout=10, max_retries=3):
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
                log.error('Check image exist error: '.format(e))
            attempt += 1
        return False

    @staticmethod
    def image_exists_head(url, log, timeout=10, max_retries=3):
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
                log.error('Check image exist error: '.format(e))
            attempt += 1
        return False

    @staticmethod
    def parse_sql_result(cursor):
        """
        Parse SQL result from a cursor object and return as list of dictionaries.
        
        :param cursor: SQL cursor object
        :return: List of dictionaries with column names as keys
        """
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    @staticmethod
    def setup_logging(log_file, time_unit='D', backupCount=3, encoding='utf-8'):
        """
        Setup logging configuration.
        
        :param log_file: Path to the log file
        :param time_unit: time unit
        :param backupCount: log backup count
        :param encoding:  text encode
        """
        log_format = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
        handler = handlers.TimedRotatingFileHandler(filename=log_file, when=time_unit, backupCount=backupCount, encoding=encoding)
        handler.setFormatter(log_format)
        logger = logging.getLogger(log_file)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger
    
    @staticmethod
    def calculate_md5(input, log):
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
            log.error('input not str,please input type str!')

# Example usage:
if __name__ == "__main__":
    # URL encoding example
    url = "https://example.com/path/to resource?query=hello world"
    encoded_url = CommonUtils.url_encode(url)
    print(f"Encoded URL: {encoded_url}")

    # Image existence check example
    image_url = "https://example.com/image.jpg"
    exists = CommonUtils.image_exists(image_url)
    print(f"Image exists: {exists}")

    # DateTime to UNIX timestamp example
    dt = datetime.now()
    unix_time = CommonUtils.get_unix_time(dt)
    print(f"UNIX timestamp: {unix_time}")

    # MongoDB oplog reading example
    # Utils.read_mongo_oplog('mongodb://localhost:27017/')

    # Logging setup example
    log_file = "app.log"
    logger = CommonUtils.setup_logging(log_file)
    logger.info("This is a test log message.")
