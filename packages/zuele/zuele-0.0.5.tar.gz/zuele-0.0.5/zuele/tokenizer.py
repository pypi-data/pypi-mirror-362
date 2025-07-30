# zuele/tokenizer.py
import os
import re
from typing import List, Tuple, Union, Iterable, Iterator
from .regex_rules import ECON_PATTERN


class Tokenizer:
    # 1. 默认句子切分正则，可覆盖
    _SENT_RE = re.compile(
        r'[^。！？!?;；\n]+[。！？!?;；\n]?',
        flags=re.UNICODE
    )

    def __init__(self, dict_path: str = None) -> None:
        if dict_path is None:
            dict_path = os.path.join(
                os.path.dirname(__file__), "data", "zuele_dict.txt"
            )
        self._dict_path = dict_path
        self._regex = ECON_PATTERN
        self._lexicon: dict[str, Tuple[int, str]] = {}
        self._load_lexicon()

    # -------- 私有 --------
    def _load_lexicon(self) -> None:
        if self._lexicon:
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

    # 2. 句子切分器，可被继承/替换
    def _split_sentences(self, text: str) -> Iterable[str]:
        for m in self._SENT_RE.finditer(text):
            yield m.group()

    # 3. 单句分词（原 cut 的逻辑搬进来）
    def _cut_single(self, text: str, *, with_pos: bool) -> List[Union[str, Tuple[str, str]]]:
        res, i, n = [], 0, len(text)
        _STOP = {"的", "了", "，", "、", "与", "或"}
        while i < n:
            m = self._regex.match(text, i)
            if m:
                ent = m.group()
                res.append((ent, "m") if with_pos else ent)
                i = m.end()
                continue
            for j in range(min(n, i + 15), i, -1):
                w = text[i:j]
                if w in self._lexicon:
                    pos = self._lexicon[w][1]
                    res.append((w, pos) if with_pos else w)
                    i = j
                    break
            else:
                if with_pos and text[i] in _STOP:
                    res.append((text[i], "u"))
                    i += 1
                    continue
                res.append((text[i], "x") if with_pos else text[i])
                i += 1
        return res

    # 4. 公开接口：整篇文本 → 句子 → 词语（流式）
    def cut(self, text: str, *, with_pos: bool = False) -> Iterator[Union[str, Tuple[str, str]]]:
        for sent in self._split_sentences(text):
            for token in self._cut_single(sent, with_pos=with_pos):
                yield token
