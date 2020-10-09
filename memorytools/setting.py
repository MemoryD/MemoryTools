from string import punctuation
from easydict import EasyDict

from pic import *

ABOUT_IMG = 'README.png'
CONFIG = 'config.json'
SRC_PATH = 'src'
LOG_PATH = 'log'
ICONS = {
    'icon.ico': ICON_ICO, 'trans.ico': TRANS_ICO, 'ocr.ico': OCR_ICO,
    'alert.ico': ALERT_ICO, 'exit.ico': EXIT_ICO, 'about.ico': ABOUT_ICO,
    'check.ico': CHECK_ICO, 'pick.ico': PICK_ICO
}

HOVER_TEXT = "Memory Tools"
ALERT_MSG = 'tip: 连续在电脑前工作太久容易脱发，得颈椎病，猝死。'

ALPHADIG = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
COLOR = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255), (0, 255, 255)]
PUNCTUATION_MAP = dict((ord(char), None) for char in punctuation)
NOTAS = u'[’·°–!"#$%&\'()*+,-./:;<=>?@，。?★、…【】（）《》？“”‘’！[\\]^_`{|}~]+'

DEFAULT_CONFIG = {
    '复制翻译':
        {
            'is_trans': True,
            'newline': False,
            'strict': False,
            'mode': 'en2zh',
            'src': 'en',
            'dest': 'zh-cn'
        },
    'OCR识别':
        {
            'is_ocr': True,
            'newline': True,
            'mode': 'text'
        },
    '休息提醒':
        {
            'is_alert': True,
            'alert_time': 90
        }
}

DEFAULT_CONFIG = EasyDict(DEFAULT_CONFIG)

# 学而思AI开方平台的账号
XUEERSI_ACCOUNTS = [
    {
        'app_key': '2a449a7feb2a73b99e6d2b2f3642aa9e73e40e64',
        'app_secret': 'dd8f56acf88895367c738cd9c1255507d081746210c5dbee3022795ba9cc9b83'
    },
    {
        'app_key': '5aa0ae48e4b03fe034cb547f9ebfa47190d88739',
        'app_secret': '96bc4d214831921740fcc383681460f4a60558992ac1c20cba85da49f2fb408f'
    },
    {
        'app_key': 'cde7ff598c932b589b80d8b8c84aee88f563ff93',
        'app_secret': '3aeb7acbe8b5f3118da2bf59db42d0cbbf4237453fd3f03bee721c52a02eafcc'
    },
    {
        'app_key': 'b8818b44c59c420848ed01eff8e965b315510cf0',
        'app_secret': 'e3d70584da64bea52af859866b7d5bd1b6eaeed6f0dde333bbf17f6b4af72dea'
    }
]

# 百度AI开方平台的账号
BAIDU_ACCOUNTS = [
    {
        'APP_ID': '18054283',
        'APP_KEY': 'UnwUzcDzzMcR6smt5xm9vIwi',
        'SECRET_KEY': '755vO7iZGV0DDIlzH7DHpkWjGDOBZzav',
    },
    {
        'APP_ID': '19027780',
        'APP_KEY': 'c86EqlNtYwlIeMNvl6Pb1F1d',
        'SECRET_KEY': 'lDSIICh8MDAaa7fi6xYTpXQD5kUdQ5Ap',
    }
]

# 学而思平台的所有错误码，来源：https://docai.xueersi.com/books/ai%E6%95%99%E8%82%B2%E5%BC%80%E6%94%BE%E5%B9%B3%E5%8F%B0/page/%E8%BF%94%E5%9B%9E%E7%A0%81%E5%88%97%E8%A1%A8
XUEERSI_ERROR_CODES = {
    -15000: {'reason': 'json字符串化发生错误', 'solution': '联系客服linqi@100tal.com，反映此问题'},
    -15001: {'reason': 'json对象化发生错误', 'solution': '检查发送给API接口的请求Body中，字符串是否符合Json结构'},
    -15002: {'reason': '内部请求错误', 'solution': '联系客服linqi@100tal.com，反映此问题'},
    -15101: {'reason': 'OCR服务内部异常', 'solution': '联系客服linqi@100tal.com，反映此问题'},
    14000: {'reason': '参数非法', 'solution': '检查请求参数是否缺失，或参数类型有误'},
    14001: {'reason': '缺少app_key参数', 'solution': '检查是否缺失"app_key"参数'},
    14002: {'reason': '缺少time_stamp参数', 'solution': '检查是否缺失"time_stamp"参数'},
    14003: {'reason': '缺少nonce_str参数', 'solution': '检查是否缺失"nonce_str"参数或长度是否满足要求(1-32个字符长度)'},
    14004: {'reason': '缺少sign参数', 'solution': '检查是否缺失"sign"参数'},
    14005: {'reason': '图像不存在', 'solution': '检查传入图像URL是否有效，或者图像Base64是否完整且规范'},
    14011: {'reason': '应用不存在', 'solution': '检查当前请求API的URL拼写是否正确'},
    14012: {'reason': '请求签名无效', 'solution': '检查签名是否正确，或尝试重新获取签名'},
    14013: {'reason': 'time_stamp参数无效', 'solution': '检查"time_stamp"参数是否有误'},
    15001: {'reason': 'qps超过限制', 'solution': '您的每秒并发量超过了最大限制，请降低并发量重试；或者联系客服申请提高每秒并发量限制'},
    15002: {'reason': 'qpd超过限制', 'solution': '您的每日调用量超过了最大限制，请隔日再试；或者联系客服申请提高每日调用量限制'},
    15003: {'reason': 'qpm超过限制', 'solution': '您的每分钟并发量超过了最大限制，请降低并发量重试；或者联系客服申请提高每秒并发量限制'},
    15004: {'reason': 'interval超过限制', 'solution': '接口调用频率超过访问允许间隔。如果是试用账号，请登录后使用自己的账号。如果希望扩容，请联系商务为您免费提高调用频率。'},
    15010: {'reason': '图片解析失败，请重试', 'solution': '检查图片URL是否有效，或者图像Base64是否完整 且规范'},
    15011: {'reason': '图片有些问题，请重新拍照', 'solution': '检查图片成像是否正常，图片内部是否有有效图案'},
    15012: {'reason': '图片太暗啦，请开启照明', 'solution': '检查图片成像是否过暗，尝试开启闪光灯拍照重试'},
    15013: {'reason': '图片太模糊啦，请保证拍照清晰', 'solution': '检查图片成像是否模糊，请保证拍照清晰之后重试'},
    15020: {'reason': '客户端发包异常', 'solution': '检查网络是否有波动'},
    15021: {'reason': 'Sid获取异常', 'solution': '联系客服linqi@100tal.com，反映此问题'},
    15022: {'reason': 'Idx获取异常', 'solution': '联系客服linqi@100tal.com，反映此问题'},
    15023: {'reason': '图像获取异常', 'solution': '检查图片URL是否有效，或者图像Base64是否完整且规范'},
    15024: {'reason': '图像损坏', 'solution': '检查图片成像是否正常，图片内部是否有有效图案'},
    15025: {'reason': '图像模糊', 'solution': '检查图片成像是否模糊，请保证传入清晰图片重试'},
    15026: {'reason': '其他图像异常', 'solution': '检查图片问题，或联系客服linqi@100tal.com，反映此问题'},
    15100: {'reason': '传入图像尺寸过大或过小', 'solution': '不能大于4MB,长边不能超过4096,短边不能小于15'},
    16010: {'reason': 'base64音频编码为[]byte失败', 'solution': '检查base64音频内容是否无效'},
    16011: {'reason': '构造请求消息结构失败', 'solution': '检查发送参数是否不符合规范'},
    16012: {'reason': '解码服务器返回的响应body中，未获取到响应数据', 'solution': '联系客服linqi@100tal.com，反映此问题'},
    16013: {'reason': '对解码服务器发送的http请求，请求失败或未响应', 'solution': '联系客服linqi@100tal.com，反映此问题'},
    16014: {'reason': 'socket接收失败', 'solution': 'socket接收失败'},
    16015: {'reason': '拉学生名单错误', 'solution': '输入学生名单有误，请检查。'},
    16016: {'reason': '解码器返回超时，比如端长时间占用连接', 'solution': '解码服务器连接超时，请稍后再试。'},
    16017: {'reason': 'Sid提前结束', 'solution': '您的这段语音已完成识别或者测评。'},
    16018: {'reason': '解码器目前繁忙', 'solution': '服务器繁忙，请稍后重试。'},
    16107: {'reason': '音频格式错误', 'solution': '请检查您的传入音频格式是否是允许的格式'},
    16108: {'reason': '评测文本格式错误，如出现了违规字符', 'solution': '请检查您的传入评测文本是否包含违规字符'},
    16019: {'reason': '解码器返回数据无有效声音', 'solution': '请检查您的传入音频是否有有效信息。'},
    16020: {'reason': 'pcm错误', 'solution': '请检查您的传入音频是否完整且有效'},
    16100: {'reason': 'WebSocket建立连接时，请求协议不是WebSocket握手', 'solution': '请检查您的WebSocket连接'},
    16101: {'reason': 'WebSocket建立连接时，无法设置WebSocket连接', 'solution': '请检查您的WebSocket连 接'},
    16102: {'reason': '可能是您的WebSocket长链接异常中断了，在WebSocket长连接中，服务端无法正常读取消息', 'solution': '请检查您的WebSocket连接'},
    16103: {'reason': '您传入的请求json中：common参数部分的idx属性不是字符型数字', 'solution': '请检查 您的请求数据common中idx的数据类型'},
    16104: {'reason': '您传入的请求json中：spec参数部分的assessRef评测文本为空', 'solution': '请检查您 的请求数据spec中是否包含assessRef'},
    16105: {'reason': '没有sid或者idx，或者在需要assess_ref的业务中没有传', 'solution': '请检查传入参数中是否缺失sid或idx或assess_ref。'},
    16106: {'reason': '音频数据为空', 'solution': '请检查您的传入音频是否有有效信息。'},
    16109: {'reason': '此sid已经结束', 'solution': '当前sid服务端已经处理结束'},
    16110: {'reason': '此sid已经完全结束', 'solution': '当前sid服务端已经处理结束且触发超时，处于待清理状态'},
    16111: {'reason': '您传入的请求json中：common参数部分的sid属性长度不符合长度要求(16-64个字符)', 'solution': '请检查您的传入的sid是否符合要求的长度'}
}

# 百度平台的错误码
BAIDU_ERROR_CODES = {
    4: '集群超限额',
    14: 'IAM鉴权失败，建议用户参照文档自查生成sign的方式是否正确，或换用控制台中ak sk的方式调用',
    17: '每天流量超限额',
    18: 'QPS超限额，请稍后再试',
    19: '请求总量超限额',
    100: '无效参数',
    110: 'Access Token失效',
    111: 'Access token过期',
    282000: '服务器内部错误，如果您使用的是高精度接口，报这个错误码的原因可能是您上传的图片中文字过多，识别超时导致的，建议您对图片进行切割后再识别，其他情况请再次请求， 如果持续出现此类错误，请通过QQ群 '
            '（631977213）或工单联系技术支持团队。',
    216100: '请求中包含非法参数，请检查后重新尝试',
    216101: '缺少必须的参数，请检查参数是否有遗漏',
    216102: '请求了不支持的服务，请检查调用的url',
    216103: '请求中某些参数过长，请检查后重新尝试',
    216110: 'appid不存在，请重新核对信息是否为后台应用列表中的appid',
    216200: '图片为空，请检查后重新尝试',
    216201: '上传的图片格式错误，现阶段我们支持的图片格式为：PNG、JPG、JPEG、BMP，请进行转码或更换图片',
    216202: '上传的图片大小错误，现阶段我们支持的图片大小为：base64编码后小于4M，分辨率不高于4096*4096 ，请重新上传图片',
    216630: '识别错误，请再次请求，如果持续出现此类错误，请通过QQ群（631977213）或工单联系技术支持团队 。',
    216631: '识别银行卡错误，出现此问题的原因一般为：您上传的图片非银行卡正面，上传了异形卡的图片或上传的银行卡正品图片不完整',
    216633: '识别身份证错误，出现此问题的原因一般为：您上传了非身份证图片或您上传的身份证图片不完整',
    216634: '检测错误，请再次请求，如果持续出现此类错误，请通过QQ群（631977213）或工单联系技术支持团队 。',
    282003: '请求参数缺失',
    282005: '处理批量任务时发生部分或全部错误，请根据具体错误码排查',
    282006: '批量任务处理数量超出限制，请将任务数量减少到10或10以下',
    282110: 'URL参数不存在，请核对URL后再次提交',
    282111: 'URL格式非法，请检查url格式是否符合相应接口的入参要求',
    282112: 'url下载超时，请检查url对应的图床/图片无法下载或链路状况不好，您可以重新尝试一下，如果多次尝试后仍不行，建议更换图片地址',
    282113: 'URL返回无效参数',
    282114: 'URL长度超过1024字节或为0',
    282808: 'request id xxxxx 不存在',
    282809: '返回结果请求错误（不属于excel或json）',
    282810: '图像识别错误'
}

LANGUAGE = {'自动检测': '', '中文': 'zh-cn', '中文繁体': 'zh-tw', '英语': 'en', '德语': 'de', '俄语': 'ru', '法语': 'fr',
            '阿尔巴尼亚语': 'sq', '阿拉伯语': 'ar', '阿姆哈拉语': 'am', '阿塞拜疆语': 'az', '爱尔兰语': 'ga',
            '爱沙尼亚语': 'et', '巴斯克语': 'eu', '白俄罗斯语': 'be',
            '保加利亚语': 'bg', '冰岛语': 'is', '波兰语': 'pl', '波斯尼亚语': 'bs',
            '波斯语': 'fa', '布尔语': 'af', '丹麦语': 'da',
            '菲律宾语': 'tl', '芬兰语': 'fi', '弗里西语': 'fy', '高棉语': 'km', '格鲁吉亚语': 'ka',
            '古吉拉特语': 'gu', '哈萨克语': 'kk', '海地克里奥尔语': 'ht',
            '豪萨语': 'ha', '荷兰语': 'nl', '吉尔吉斯语': 'ky', '加利西亚语': 'gl', '加泰罗尼亚语': 'ca',
            '捷克语': 'cs', '卡纳达语': 'kn', '科西嘉语': 'co', '克罗地亚语': 'hr',
            '库尔德语': 'ku', '拉丁语': 'la', '拉脱维亚语': 'lv', '老挝语': 'lo', '立陶宛语': 'lt',
            '卢森堡语': 'lb', '罗马尼亚语': 'ro', '马尔加什语': 'mg', '马耳他语': 'mt',
            '马拉地语': 'mr', '马拉雅拉姆语': 'mf', '马来语': 'ms', '马其顿语': 'mk',
            '毛利语': 'mi', '蒙古语': 'mn', '孟加拉语': 'bn', '缅甸语': 'my', '苗语': 'hmn', '南非克萨语': 'xh', '南非祖鲁语': 'zu',
            '尼泊尔语': 'ne', '挪威语': 'no', '旁遮普语': 'pa', '葡萄牙语': 'pt', '普什图语': 'ps',
            '齐切瓦语': 'ny', '日语': 'ja', '瑞典语': 'sv', '萨摩亚语': 'sm', '塞尔维亚语': 'sr',
            '赛所托语': 'st', '僧伽罗语': 'si', '世界语': 'eo', '斯洛伐克语': 'sk', '斯洛文尼亚语': 'sl',
            '斯瓦希里语': 'sw', '苏格兰盖尔语': 'gd', '宿务语': 'ceb', '索马里语': 'so', '塔吉克语': 'tg', '泰卢固语': 'te',
            '泰米尔语': 'ta', '泰语': 'th', '土耳其语': 'tr', '威尔士语': 'cy', '乌尔都语': 'ur',
            '乌克兰语': 'uk', '乌兹别克语': 'uz', '西班牙语': 'es', '希伯来语': 'rw', '希腊语': 'el',
            '夏威夷语': 'haw', '信德语': 'sd', '匈牙利语': 'hu', '修纳语': 'sn',
            '亚美尼亚语': 'hy', '伊博语': 'ig', '意大利语': 'it', '意第绪语': 'yi', '印地语': 'hi',
            '印尼巽他': 'su', '印尼语': 'id', '印尼爪哇语': 'jw', '约鲁巴语': 'yo', '越南语': 'vi'
            }
