# zuele/__init__.py
from .tokenizer import Tokenizer

# 对外暴露“懒人函数”
cut = Tokenizer().cut
