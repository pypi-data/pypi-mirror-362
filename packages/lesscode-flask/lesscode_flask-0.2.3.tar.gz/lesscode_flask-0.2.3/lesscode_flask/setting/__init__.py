import os
import sys


class BaseConfig:
    # 应用id
    CLIENT_ID: str = ""
    # 应用名称-中文名称
    CLIENT_NAME: str = ""
    # 应用名称-英文名称
    CLIENT_EN_NAME: str = ""
    # 统一路由前缀
    ROUTE_PREFIX = ""
    # 项目端口号
    PORT = 5002

    # 数据源
    DATA_SOURCE = []
    # SQLALCHEMY数据库连接
    SQLALCHEMY_BINDS = {
        # 'users': 'mysqldb://localhost/users',
        # 'appmeta': 'sqlite:////path/to/appmeta.db'
    }

    ##**************日志存储相关*****************##
    # 日志级别
    LESSCODE_LOG_LEVEL = os.environ.get("LESSCODE_LOG_LEVEL", "INFO")
    # 日志格式
    LESSCODE_LOG_FORMAT = os.environ.get("LESSCODE_LOG_FORMAT",
                                         '[%(asctime)s] [%(levelname)s] [%(name)s:%(module)s:%(lineno)d] [%(message)s]')
    # 输出管道
    LESSCODE_LOG_STDOUT = os.environ.get("LESSCODE_LOG_STDOUT", True)
    # 日志文件备份数量
    LESSCODE_LOG_FILE_BACKUPCOUNT = os.environ.get("LESSCODE_LOG_FILE_BACKUPCOUNT", 7)
    # 日志文件分割周期
    LESSCODE_LOG_LOG_FILE_WHEN = os.environ.get("LESSCODE_LOG_LOG_FILE_WHEN", "D")
    # 日志文件存储路径
    LESSCODE_LOG_FILE_PATH = os.environ.get("LESSCODE_LOG_FILE_PATH", 'logs/lesscode.log')
    # 访问日志是否DB存储
    LESSCODE_ACCESS_LOG_DB = os.environ.get("LESSCODE_ACCESS_LOG_DB", 0)

    # 外网地址
    # swagger 的名称
    SWAGGER_NAME = "API"
    # swagger 的版本
    SWAGGER_VERSION = "1.0.0"
    # swagger 的描述
    SWAGGER_DESCRIPTION = "项目接口说明文档"

    SWAGGER_URL = '{}/swagger-ui'.format(ROUTE_PREFIX)

    OUTSIDE_SCREEN_IP: str = "http://127.0.0.1:{}".format("5004")
    # SWAGGER_URL = '{}/swagger-ui'.format(ROUTE_PREFIX)
    SWAGGER_API_URL = '{}/swagger'.format(ROUTE_PREFIX)

    # 无需包装的路由
    NOT_RESPONSE_RESULT = [SWAGGER_URL, SWAGGER_API_URL]
    # # 项目端口号
    # PORT: int = 8080
    #
    # 应用运行根路径
    # APPLICATION_PATH: str = f"{os.path.abspath(os.path.dirname(sys.argv[0]))}"
    # # 静态资源目录
    STATIC_PATH: str = os.path.join(f"{os.path.abspath(os.path.dirname(sys.argv[0]))}", "static")

    SECRET_KEY = "423ad5ef841bbd073b415e4ba4136d7c94cac3f5e9bfeec1a21da35cd9ea6b46"

    ##**************缓存相关*****************##
    # redis缓存开关
    CACHE_ENABLE: bool = False
    # 缓存库key
    REDIS_CACHE_KEY = "redis"
    # 权限缓存key
    REDIS_OAUTH_KEY = "oauth2_redis"

    ##**************权限控制相关*****************##
    # 是否启用权限验证
    AUTHORIZATION_ENABLE: bool = False
    # 是否启用网关获取用户
    GATEWAY_USER_ENABLE: bool = False
    # 禁用掉从cookie获取用户
    REMEMBER_COOKIE_NAME = "False"
    # 未配置权限的资源 默认权限  1：需要登录 0：游客'
    AUTH_DEFAULT_ACCESS = 0
    # 启用生成刷新token
    OAUTH2_REFRESH_TOKEN_GENERATOR = True
    #
    # # 外网地址
    # OUTSIDE_SCREEN_IP: str = ""
    # # 内网ip
    # INSTANCE_IP: str = ""
    #
    # 数据服务
    CAPABILITY_PLATFORM_SERVER: str = "http://127.0.0.1:8976"
    # # 权限服务地址
    # OAUTH_SERVER: str = ""
    # # 后端管理地址
    # UPMS_SERVER: str = ""
    # # 报告服务地址
    # REPORT_SERVER: str = ""
    #
    # # aes加密key
    # AES_KEY: str = 'haohaoxuexi'
    # ks3连接配置
    # host ks3的地址; access_key_id ks3的key; access_key_secret ks3的密钥 is_secure 是否使用https协议
    KS3_CONNECT_CONFIG: dict = {"bucket_name": "", "host": "", "access_key_id": "", "access_key_secret": "",
                                "is_secure": False}
    # request请求的参数
    CONNECT_CONFIG: dict = {
        # "pool_connections": 10,
        # "pool_maxsize": 100,
        # "max_retries": 1,
        # "pool_block": False
    }
    # 资源注册相关
    REGISTER_ENABLE = False
    REGISTER_SERVER = "http://127.0.0.1:8976"

    # 本地环境
    ENV = "local"
    # 是否代理能力平台的公共接口
    ICP_RESOURCE_PROXY = True
    ICP_RESOURCE_PROXY_SMS_TEMPLATE_CODE = "SMS_464780859"
    SMS_TEMPLATE = {}

    DATA_DOWNLOAD_UPLOAD_KS3 = False
