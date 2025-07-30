from collections.abc import Mapping
import html
from typing import override, Any

from ..defaults import DEFAULT_LEVEL_NAMES
from ..types import FormatStyle, EscapeFunc
from .escape import EscapeMarkupFormatter
    

class HtmlFormatter(EscapeMarkupFormatter):
    """A formatter for using HTML markup and flexible escaping settings.
    
    Equivalent to `EscapeMarkupFormatter` with `parse_mode` and `escape_func` parameters preset.

    Common use cases:

    1. HTML is used directly when calling the logger.
    For example, `logger.info('<u>example</u> text')`.

    In this case, it is necessary to disable message escaping. Control of special characters
    remains with the user. If stack and traceback output are used by default, it is recommended
    to leave their escaping enabled.

    ```python
    formatter = HtmlFormatter(
        fmt = '<b>{levelname}</b> {message}',
        style = '{',
        escape_message = False,
    )
    ```

    2. HTML is used in the `fmt` string and is not used within messages.

    In this case, the default escaping settings are sufficient, just adjust the `fmt` line.
    Optionally, you may want to wrap the stack and traceback output in a code block. To do this,
    either manually specify your preferred template, or import a ready-made template from the
    library defaults.

    ```python
    from markup_tg_logger.defaults import HTML_PYTHON_TEMPLATE

    formatter = HtmlFormatter(
        fmt = '<b>{levelname}</b> <i>{message}</i>',
        style = '{',
        stack_info_template = HTML_PYTHON_TEMPLATE,
        exception_template = HTML_PYTHON_TEMPLATE,
    )
    ``` 

    The `HTML_PYTHON_TEMPLATE` constant is a `<pre><code class="language-python">{text}</code></pre>`
    template for formatting text into a code block with python syntax highlighting. If you prefer
    bash highlighting, use the `HTML_BASH_TEMPLATE` constant or define your own template.

    3. Formatting the entire log output into a block with code and no markup inside that block.

    In this case, disable message, stack and traceback escaping and enable formatting result
    escaping. Also set the general template as described in point 2.

    ```python
    from markup_tg_logger.defaults import HTML_PYTHON_TEMPLATE

    formatter = HtmlFormatter(
        fmt = '{levelname} {message}',
        style = '{',
        escape_message = False,
        escape_stack_info = False,
        escape_exception = False,
        escape_result = True,
        result_template = HTML_PYTHON_TEMPLATE,
    )
    ``` 
    """

    @override
    def __init__(
        self,
        fmt: str | None = None,
        datefmt: str | None = None,
        style: FormatStyle = '%',
        validate: bool = True,
        *,
        defaults: Mapping[str, Any] | None = None,
        level_names: dict[int, str] = DEFAULT_LEVEL_NAMES,
        escape_func: EscapeFunc = lambda text: html.escape(text, quote=False),
        escape_message: bool = True,
        escape_stack_info: bool = True,
        escape_exception: bool = True,
        escape_result: bool = False,
        stack_info_template: str = '{text}',
        exception_template: str = '{text}',
        result_template: str = '{text}'
    ) -> None:
        """
        Args:
            fmt: A format string in the given style for the logged output as a whole. The possible
                mapping keys are drawn from the `LogRecord` object's `LogRecord` attributes. If not
                specified, `%(message)s` is used, which is just the logged message.
            datefmt: A format string in the given style for the date/time portion of the logged
                output. If not specified, the default described in `formatTime()` is used.
            style: Can be one of `%`, `{` or `$` and determines how the format string will be
                merged with its data: using one of printf-style String Formatting (%),
                `str.format()` ({) or string.Template ($). This only applies to fmt and datefmt
                (e.g. `%(message)s` versus `{message}`), not to the actual log messages passed
                to the logging methods. However, there are other ways to use {- and $-formatting
                for log messages.
            validate:  If `True` (the default), incorrect or mismatched `fmt` and `style` will
                raise a `ValueError`; for example, `HtmlFormatter('%(message)s', style='{')`.
            defaults:
                A dictionary with default values to use in custom fields. For example,
                `HtmlFormatter('%(ip)s %(message)s', defaults={"ip": None})`.
            level_names: Mapping between numeric logging level IDs and their names. For example,
                `{30: 'WARN'}` or `{logging.WARNING: 'WARN'}`. By default, names will be appended
                with colored emoji. The dictionary does not have to override all level names.
                To use the default names, use `level_names = {}`.
            escape_func: The function that will be used to escape special characters. By default,
                the `escape` function with `quote=False` from the `html` module of the standard
                library is used. 
            escape_message: If `True`(the default), escape the log message text.
            escape_stack_info: If `True` (the default), escape stack output.
            escape_exception: If `True` (the default), escape traceback exception output.
            escape_result: If `True`, escape the resulting message after all formatting. To enable
                this option, it is recommended to disable `escape_message`, `escape_stack_info`and
                `escape_exception` to avoid repeated escaping.
            stack_info_template: A template string with a single required parameter `{text}` for
                marking up stack info text. For example, `'<code>{text}</code>'`. By default, does
                not change the text.
            exception_template: A template string with a single required parameter `{text}` for
                marking up the traceback output. For example, `'<code>{text}</code>'`. By default,
                does not change the text.
            result_template: A template string with a single required parameter `{text}` for
                marking up the resulting message after all formatting. The `text` parameter
                includes the result of substitution into the `fmt` string, stack info and exception
                traceback. For example, `'<code>{text}</code>'`. By default, does not change the text.

        There is no separate `message_template` parameter in templates, since this functionality is
        implemented through the standard `fmt` string. For example, `fmt = '<code>{message}</code>'`.
        """

        super().__init__(
            fmt = fmt,
            datefmt = datefmt,
            style = style,
            validate = validate,
            defaults = defaults,
            level_names = level_names,
            parse_mode = 'HTML',
            escape_func = escape_func,
            escape_message = escape_message,
            escape_stack_info = escape_stack_info,
            escape_exception = escape_exception,
            escape_result = escape_result,
            stack_info_template = stack_info_template,
            exception_template = exception_template,
            result_template = result_template,
        )
