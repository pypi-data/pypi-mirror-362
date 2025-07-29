import os
import locale
import gettext
from pathlib import Path
from typing import Optional
from typing import Callable


__all__ = [
    "translate",
]


def get_translate_language(
    domain: str = "messages",               # 默认为 'messages'，这是 .mo 文件的默认基名
    localedir: Optional[str] = None,        # 指定翻译文件目录，默认 None，稍后自动设置
)-> Callable[[str], str]:
    # 优先从环境变量中获取语言设置，适配 Linux/macOS 的常用变量
    lang = (
        os.getenv("LANG") or                # 常见格式如 "zh_CN.UTF-8"
        os.getenv("LC_ALL") or              # 全局语言优先级高于 LANG
        os.getenv("LANGUAGE")               # 某些系统使用 LANGUAGE 覆盖 LANG
    )

    if not lang:
        # 如果环境变量中没有定义语言，就使用 Python locale 模块检测系统默认语言
        lang, _ = locale.getdefaultlocale()  # 返回如 ("zh_CN", "UTF-8")

    # 去掉后缀（如 UTF-8），只保留语言代码部分（如 zh_CN）
    lang = (lang or "en_US").split('.')[0]

    if localedir is None:
        # 如果没有手动指定 locales 路径，就使用当前文件旁边的 "locales" 文件夹
        localedir = str(Path(__file__).resolve().parent / "locales")


    t = gettext.translation(
        domain=domain,                   # 如 messages.mo
        localedir=localedir,             # 语言目录路径
        languages=[lang],                # 语言列表，只取一个
        fallback=True                    # 若找不到翻译文件则返回原始字符串
    )
    
    return t.gettext  # 返回翻译函数
        
        
translate = get_translate_language()  # 默认加载 messages.mo
