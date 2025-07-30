from redis import Redis
import logging
import json

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)
LOG_FT = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(LOG_FT)


##################################################
# redis function
##################################################

def rd_connect(host, port, password):
    return Redis(host=host, port=port, password=password)


def rd_del(connect, key):
    try:
        res = connect.delete(key)
        return res
    except Exception as e:
        LOG.error('exception ... {}'.format(e))
        return False


def rd_expire(connect, key, seconds):
    connect.expire(key, seconds)


def rd_set(connect, key, value):
    connect.set(key, value)


def rd_set_list(connect, key, value):
    connect.rpush(key, value)


def rd_set_zset(connect, key, value, score):
    connect.zadd(key, {value: score})


def rd_get(connect, key, code='utf-8'):
    try:
        res = connect.get(key)
        return res.decode(code)
    except Exception as e:
        LOG.error('exception ... {}'.format(e))
        return None


def rd_get_zset(connect, key, start, end):
    return connect.zrange(key, start, end)


def rd_get_list_len(connect, key):
    return connect.llen(key)


def rd_get_zset_len(connect, key):
    return connect.zcard(key)


def dump_docs_redis_set(con, key, timeout, docs):
    LOG.info('key:{},timeout:{},docs:{}'.format(key, timeout, docs))
    rd_set(con, key, json.dumps(docs, ensure_ascii=False))
    if timeout > 0:
        rd_expire(con, key, timeout)
    return key


def dump_data_redis_set_list(con, key, timeout, data):
    LOG.info('key:{},timeout:{},docs:{}'.format(key, timeout, data))
    for item in data:
        rd_set_list(con, key, item)
    if timeout > 0:
        rd_expire(con, key, timeout)
    return key


def dump_data_redis_set_zset(con, key, timeout, data):
    LOG.info('key:{},timeout:{},docs:{}'.format(key, timeout, data))
    for index, item in enumerate(data):
        rd_set_zset(con, key, item, index)
    if timeout > 0:
        rd_expire(con, key, timeout)
    return key


if __name__ == '__main__':
    RD_HOST = '127.0.0.1'
    RD_PORT = '6379'
    RD_PASS = '123456'
    rd_con = rd_connect(RD_HOST, RD_PORT, RD_PASS)
    rd_key = 'test_list'
    data_list = ['圣诞节', '冬至', '圣诞', '元旦', '电商主图', '免费', '拼图', '邀请函', '招聘', '主图', '直播间', '美食', '喜报', '图文带货', '名片', '新年',
                 '旅游', '招聘海报', '菜单', '早安', '双旦', '横版海报', '头像', '生日', '详情页', '水印', '去水印', '小红书', '横版', '海报', '雪', '直播背景',
                 '直播', '扩图', 'logo', '科技', '美容', '自我介绍', '滑雪', '龙年', '代金券', '地震', '封面', '日历', '汽车', '春节', '电商', '咖啡',
                 '双旦狂欢', '红色', '优惠券', '穿搭', 'ppt', '年会', '零食', '平安夜', '表格', '背景', '活动', '产品展示', '简历', '教育', '绿色', '倒计时',
                 '元旦放假通知', '火锅', '电影', '家具', '电商详情页', '茶', '宠物', '服装', '产品', '课程', '元旦放假', '茶叶', '美妆', '二维码', '古风',
                 '活动海报', '年夜饭', '人物介绍', '节目单', '酒', '蓝色', '培训', '抽奖', '日签', '详情', '肉', '男装', '抖音', '课程表', '贴片', '年货节',
                 '价格表', '运动', '2024', '龙', '母婴', '简约', '珠宝', '游戏', '招生', '家居', '压缩', '黑色', '视频', '公众号', '五金', '粉色',
                 '医疗', '女装', '战报', '邀请函海报', '烟花', '生日祝福', '圣诞贺卡', '元旦海报', '边框', '双旦鉅惠', '温馨提示', '音乐', '旅行', '婚礼', '冬',
                 '讲座', '对比', '促销', '通知', '寒假班', '直播贴片', '中国风', '儿童', '长图', '酒店', '冬天', '保密', '周岁', '年货', '直播间背景', '花',
                 '红包', '手抄报', '图书', '横版banner海报', '养生', '福利', '龙年新年祝福', '旅游攻略', '生鲜', '卡通', '招生海报', '周年庆', '生日会', '党建',
                 '知识科普', '公众号首图', '海鲜', '国风', '开业', '驾校', 'banner', '寒假招生', '水果', '颁奖', '冬季', '个人简介', '饺子', '美业',
                 '视频封面', '标题', '讲师', '公告', '背景图', '跨年', '直播预告', '民宿', '超市', '价目表', '倒计时海报', '人物', '店招', '横版banner',
                 '食品', '详情图', '星空', '厨房', '手机', '电脑', '雪花', '图文', '九宫格', '纯色背景', '考研', '猪蹄', '圣诞节海报', '圣诞风', '女装性感内衣',
                 '文字', '跨境电商', '风景', '露营', '金融', '喜庆', '工业', '医美', '证件照', '篮球', '圣诞老人', 'PPT', '下雪', '圣诞海报', '产品介绍']
    # dump_data_redis_set_zset(rd_con, rd_key, 0, data_list)
    # print(len(data_list))
    # print(rd_get_zset_len(rd_con, rd_key))
    # rd_del(rd_con, rd_key)
    # rd_get(rd_con, rd_key)
    zset_elements = rd_get_zset(rd_con, 'XIUXIU_PRO_SEO_TOP_SEARCH_WORD_LIST_20231219', 0, -1)
    decoded_elements = [element.decode('utf-8') for element in zset_elements]
    print(decoded_elements)
