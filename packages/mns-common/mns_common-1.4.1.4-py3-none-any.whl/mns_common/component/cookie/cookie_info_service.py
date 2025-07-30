import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 16
project_path = file_path[0:end]
sys.path.append(project_path)
from mns_common.db.MongodbUtil import MongodbUtil

mongodb_util = MongodbUtil('27017')

from functools import lru_cache


@lru_cache(maxsize=None)
def get_ths_cookie():
    stock_account_info = mongodb_util.find_query_data('stock_account_info', {"type": "ths_cookie", })
    ths_cookie = list(stock_account_info['cookie'])[0]
    return ths_cookie


def clear_ths_cookie():
    get_ths_cookie.cache_clear()


@lru_cache(maxsize=None)
def get_em_cookie():
    stock_account_info = mongodb_util.find_query_data('stock_account_info', {"type": "em_cookie", })
    em_cookie = list(stock_account_info['cookie'])[0]
    return em_cookie


def clear_em_cookie():
    get_em_cookie.cache_clear()


@lru_cache(maxsize=None)
def get_xue_qiu_cookie():
    stock_account_info = mongodb_util.find_query_data('stock_account_info', {"type": "xue_qiu_cookie", })
    cookie = list(stock_account_info['cookie'])[0]
    return cookie


def clear_xue_qiu_cookie():
    get_xue_qiu_cookie.cache_clear()
