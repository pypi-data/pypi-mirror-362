# regex_patterns.py
import re
from typing import Pattern

ECON_PATTERN: Pattern[str] = re.compile(
    r"\d{4}年"  # 2024年
    r"|\d{4}年度"  # 2024年度
    r"|\d+(?:\.\d+)?(?:万亿|亿|万|千|百|十)?元\b"  # 金额：1.2万元 / 35亿元 / 100元
    r"|\d+(?:\.\d+)?%"  # 百分比：35.11%
    r"-\d+(?:\.\d+)?%"  # 负百分比：35.11%
    r"|Q[1-4]|H[1-2]|FY\d{2,4}"  # 季度/半年度/财年：Q1 H2 FY24
    r"|\b\d+(?:\.\d+)?\b"
    ,
    flags=re.U,
)
