from concurrent.futures import ThreadPoolExecutor, wait
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import time

# 构建es客户端对象
def create_client(hosts,port):
    addrs = []
    for host in hosts:
        addr = {'host': host, 'port': port}
        addrs.append(addr)
    return Elasticsearch(addrs)

def create_client_auth(hosts, port, username, password, use_ssl=False):
    """
    创建一个使用基本用户名/密码认证的 Elasticsearch 客户端。

    :param hosts:         主机列表，如 ["es1.example.com", "es2.example.com"]
    :param port:          端口号，如 9200
    :param username:      Elasticsearch 用户名
    :param password:      对应的密码
    :param use_ssl:       是否启用 HTTPS（默认 False）
    :return:              已鉴权的 Elasticsearch 客户端实例
    """
    # 构造 hosts 列表，保留原函数结构
    addrs = []
    scheme = "https" if use_ssl else "http"
    for host in hosts:
        addr = {
            'host': host,
            'port': port,
            'scheme': scheme
        }
        addrs.append(addr)

    # 添加基本认证参数
    return Elasticsearch(
        hosts=addrs,
        http_auth=(username, password),
        use_ssl=use_ssl
    )

# es索引是否存在
def index_exists(es, index_name):
    return es.indices.exists(index=index_name)

# 创建索引
def create_index(es, index_name, mapping):
    res = es.indices.create(index=index_name, ignore=400, body=mapping)
    return res

# 删除索引
def delete_index(es, index_name):
    res = es.indices.delete(index=index_name)
    return res

# 多线程多批量写入向量数据
def write_index_bulk(es, vec_datas):
    pool = ThreadPoolExecutor(max_workers=8)
    tasks = []
    for vecs in vec_datas:
        tasks.append(pool.submit(write_bulk, es, vecs))
    wait(tasks)

# 批量写入向量数据
def write_bulk(es, vecs, timeout=3600):
    helpers.bulk(es, vecs, request_timeout=timeout)

#批量更新加入重试机制
def bulk_update_with_retry(es, actions, log, timeout=3600, retries=3):
    for attempt in range(retries):
        try:
            helpers.bulk(es, actions, request_timeout=timeout)
            break
        except helpers.BulkIndexError as e:
            version_conflict_errors = [error for error in e.errors if error['update']['status'] == 409]
            if version_conflict_errors:
                log.error(f"{len(version_conflict_errors)} version conflicts encountered. Retrying...")
            else:
                log.error(f"Bulk indexing error: {e}")
                break
            if attempt < retries - 1:
                time.sleep(1)  # 等待一段时间后重试
            else:
                log.error("Max retries reached. Some documents could not be indexed.")
                break

# 标准查询函数
def search_index(es, index_name, query, size=10):
    res = es.search(index=index_name, body=query, size=size)
    return res

# 带游标的查询函数
def scroll_search(es, index_name, query, scroll='2m', size=1000):
    page = es.search(index=index_name, body=query, scroll=scroll, size=size)
    sid = page['_scroll_id']
    scroll_size = page['hits']['total']['value']
    while scroll_size > 0:
        yield page['hits']['hits']
        page = es.scroll(scroll_id=sid, scroll=scroll)
        sid = page['_scroll_id']
        scroll_size = len(page['hits']['hits'])
    # 清理滚动上下文
    es.clear_scroll(scroll_id=sid)
