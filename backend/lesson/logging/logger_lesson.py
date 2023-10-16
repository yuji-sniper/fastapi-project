import logging
import log_handler
import log_test


# 設定
logging.basicConfig(level=logging.INFO)


# 呼び出し
log_handler.do_something()
log_test.do_something()
