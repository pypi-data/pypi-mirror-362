import logging
import os

from markup_tg_logger import TelegramHandler, HtmlFormatter
from markup_tg_logger.defaults import HTML_PYTHON_TEMPLATE, HTML_BASH_TEMPLATE


BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = int(os.environ["CHAT_ID"])

formatter = HtmlFormatter(
    fmt = '<b>{levelname}</b>\n\n{message}',
    style = '{',
    exception_template = HTML_PYTHON_TEMPLATE,
    stack_info_template = HTML_BASH_TEMPLATE,
)

handler = TelegramHandler(
    bot_token = BOT_TOKEN,
    chat_id = CHAT_ID,
)
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)

logger = logging.getLogger('example')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

logger.info('Message with stack_info option in bash code block', stack_info=True)

try:
    raise Exception('Example exception in python code block')
except Exception as e:
    logger.exception(e)
