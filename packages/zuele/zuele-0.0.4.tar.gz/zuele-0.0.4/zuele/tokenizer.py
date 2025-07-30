# zuele/tokenizer.py
import os
from typing import List, Tuple, Union

import re

ECON_REGEX = re.compile(
    r"\d{4}年"  # 年份
    r"|\d+(?:\.\d+)?(?:万亿|亿|万|千|百|十)?元\b"  # 金额
    r"|\d+(?:\.\d+)?%"  # 百分比
    r"|\d+(?:\.\d+)?bp\b"  # 基点
    r"|Q[1-4]|H[1-2]|FY\d{2,4}"  # 财报期
)


class Tokenizer:
    def __init__(self, dict_path: str = None) -> None:
        """
        dict_path 留空 → 使用包内默认 zuele_dict.txt
        """
        if dict_path is None:
            dict_path = os.path.join(
                os.path.dirname(__file__), "data", "zuele_dict.txt"
            )
        self._dict_path = dict_path
        self._lexicon: dict[str, Tuple[int, str]] = {}  # 实例私有
        self._load_lexicon()

    # -------- 私有 --------
    def _load_lexicon(self) -> None:
        if self._lexicon:  # 已加载直接返回
            return
        with open(self._dict_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                try:
                    word, freq, pos = line.split("\t")
                    self._lexicon[word] = (int(freq), pos)
                except ValueError:
                    continue

    # -------- 公开 --------
    def cut(self, text: str, *, with_pos: bool = False):
        res = []
        i = 0
        n = len(text)
        # 1. 先抓整块实体
        for m in ECON_REGEX.finditer(text):
            start, end = m.span()
            # 2. 实体前的剩余片段 → 最大匹配
            if start > i:
                res.extend(self._fmm(text[i:start], with_pos))
            # 3. 实体本身
            ent = text[start:end]
            res.append((ent, 'm') if with_pos else ent)
            i = end
        # 4. 尾部剩余
        if i < n:
            res.extend(self._fmm(text[i:], with_pos))
        return res

    # 把原最大匹配拆成私有方法，供复用
    def _fmm(self, text: str, with_pos: bool):
        words = self._lexicon.keys()
        res, i, n = [], 0, len(text)
        while i < n:
            for j in range(min(n, i + 15), i, -1):
                w = text[i:j]
                if w in words:
                    pos = self._lexicon[w][1]
                    res.append((w, pos) if with_pos else w)
                    i = j
                    break
            else:
                res.append((text[i], "x") if with_pos else text[i])
                i += 1
        return res