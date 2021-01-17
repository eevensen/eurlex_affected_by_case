# Scrapy settings for eurlex_affected_by_case project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from datetime import datetime

BOT_NAME = 'eurlex_affected_by_case'

SPIDER_MODULES = ['eurlex_affected_by_case.spiders']
NEWSPIDER_MODULE = 'eurlex_affected_by_case.spiders'

timestamp = datetime.now().strftime("%Y-%m-%d--%H-%M-%S")

filepath_and_name = './export/' + str(timestamp) + '-' + BOT_NAME + '.csv'
FEEDS = {filepath_and_name: {'format': 'csv'}}

FEED_EXPORT_FIELDS = [
    'affected_acq_recno',
    'affected_celex_number',
    'affected_text',
    'affected_court_celex',
]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'eurlex_affected_by_case (+https://evensen.io)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 3

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 3
# CONCURRENT_REQUESTS_PER_IP = 3

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    ':authority: eur-lex.europa.eu': 'eur-lex.europa.eu',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'cache-control': 'max-age=0',
    'cookie': 'ELX_SESSIONID=5SoMvVCsIXLVOFLKqRdcsecR1h0RqoaXuLDY7i2Bm0DNCEzcDZqo!-643854698; ppms_privacy_0b5594a8-b9c8-4cd6-aa25-5c578dcf91df={%22consents%22:{%22analytics%22:{%22status%22:-1%2C%22updatedAt%22:%222021-01-16T19:47:53.415Z%22}}%2C%22domain%22:{%22normalized%22:%22eur-lex.europa.eu%22%2C%22isWildcard%22:false%2C%22pattern%22:%22eur-lex.europa.eu%22}}; _pk_ses.61.5596=*; _pk_ses.0b5594a8-b9c8-4cd6-aa25-5c578dcf91df.5596=*; _pk_id.61.5596=f4cc1f89bb152f41.1610826476.1.1610826573.1610826476.; WT_FPC=id=192.168.13.1-64399600.30862400:lv=1610801373601:ss=1610801277815; _pk_id.0b5594a8-b9c8-4cd6-aa25-5c578dcf91df.5596=32916e5ea3cb7cbb.1610826476.1.1610826574.1610826476.; AWSALB=skpn/9z2HNuBSnGrXxPeVSiYBZ12QF3HVAYleIqM+Z62yip/lemPJhT3oxLiaVeGO38rlUp1IhZ/z1gB7CNJP/7D9IZK4RQAgri7E9Ha7pYVLpk+EG6sqJHWvMN4',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
    'referrer': 'eur-lex.europa.eu'
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'eurlex_affected_by_case.middlewares.EurlexAffectedByCaseSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
    # 'eurlex_affected_by_case.middlewares.EurlexAffectedByCaseDownloaderMiddleware': 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'eurlex_affected_by_case.pipelines.EurlexAffectedByCasePipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = False
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = [404]
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'



# handle_httpstatus_list = [404]
RETRY_ENABLED = True
RETRY_TIMES = 5
RETRY_HTTP_CODES = [500, 503, 504, 400, 404, 408]
