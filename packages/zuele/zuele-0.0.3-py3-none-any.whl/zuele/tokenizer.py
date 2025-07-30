# zuele/tokenizer.py
import os
from typing import List, Tuple, Union


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
    def cut(
            self, text: str, *, with_pos: bool = False
    ) -> Union[List[str], List[Tuple[str, str]]]:
        """
        正向最大匹配
        """
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
