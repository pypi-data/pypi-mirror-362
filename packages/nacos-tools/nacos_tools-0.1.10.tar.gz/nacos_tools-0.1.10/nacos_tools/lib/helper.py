import hashlib
import time
from functools import wraps


def retry_on_exception(retries=3, delay=1, backoff=2, exceptions=(Exception,)):
    """
    重试装饰器
    :param retries: 重试次数
    :param delay: 初始延迟时间
    :param backoff: 延迟时间的增长倍数
    :param exceptions: 需要重试的异常类型
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retry_delay = delay
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if i == retries - 1:  # 最后一次重试
                        raise
                    print(f"Operation failed: {str(e)}, retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= backoff
            return None

        return wrapper

    return decorator


def calculate_md5(content):
    """计算配置内容的MD5值"""
    if content is None:
        return None
    md5 = hashlib.md5()
    md5.update(content.encode('utf-8'))
    return md5.hexdigest()