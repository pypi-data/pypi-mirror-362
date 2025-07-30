from zuele import Tokenizer

tok = Tokenizer()

# 1. 基本分词
print("=== 基本分词 ===")
print(tok.cut("2023年营收3.2万亿元，同比增长10.3%，ROE 15.6bp"))

# 2. 带词性
print("\n=== 带词性 ===")
print(tok.cut("2023年营收3.2万亿元，同比增长10.3%，ROE 15.6bp", with_pos=True))

# 3. 边界检查：空串 / 无词典词
print("\n=== 边界 ===")
print(tok.cut(""))                  # []
print(tok.cut("xyz123"))            # ['x', 'y', 'z', '1', '2', '3']