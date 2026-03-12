# واکاوی وابستگی دستوری

کلاس `DependencyParser` واکاوی وابستگی دستوری متن فارسی را با استفاده از یک مدل مبتنی بر Transformer (پیش‌فرض: **ALBERT**) انجام می‌دهد. این کلاس ساختار دستوری جمله را بررسی کرده و برای هر واژه، سرواژهٔ نحوی آن (با شماره‌گذاری از ۱، که ۰ به معنای ROOT است) و برچسب رابطهٔ وابستگی را براساس استاندارد **Universal Dependencies (UD)** برمی‌گرداند.

**ویژگی‌ها**

- **دقت بالا**
- **برچسب‌های درخت وابستگی** براساس استاندارد Universal Dependencies
- نمایش درخت وابستگی

**نمونهٔ استفاده**

```python
from shekar import DependencyParser

parser = DependencyParser()
text = "ما با آنچه می‌سازیم ایرانی هستیم."

result = parser(text)
for word, head, deprel in result:
    print(f"{word} ← (head: {head}, relation: {deprel})")
```

```shell
ما ← (head: 6, relation: nsubj)
با ← (head: 3, relation: case)
آنچه ← (head: 6, relation: obl)
می‌سازیم ← (head: 3, relation: acl)
ایرانی ← (head: 6, relation: xcomp)
هستیم ← (head: 0, relation: root)
. ← (head: 6, relation: punct)
```

## نمایش درختی

می‌توانید نتیجهٔ واکاوی را به صورت درخت با متد `print_tree()` نمایش دهید:

```python
parser.print_tree(result)
```

```shell
ROOT
└── [root] هستیم
    ├── [nsubj] ما
    ├── [obl] آنچه
    │   ├── [case] با
    │   └── [acl] می‌سازیم
    ├── [xcomp] ایرانی
    └── [punct] .
```
