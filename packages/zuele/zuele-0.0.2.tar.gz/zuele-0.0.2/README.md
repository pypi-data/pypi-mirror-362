# zuele
零配置、开箱即用的中文经济文本分词库。  
内置 1125 份年报提炼词典，支持带词性输出。

```python
import zuele
zuele.cut("2023年Q3营收3.2万亿元", with_pos=True)


3️⃣ 校验一次性脚本  
项目根目录执行：

```bash
python -m build        # 生成 dist/zuele-0.1.0.whl
twine check dist/*     # 检查元数据