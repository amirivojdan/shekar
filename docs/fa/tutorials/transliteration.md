# نویسه‌گردانی

ماژول نویسه‌گردانی تبدیل دوطرفه خط بین فارسی و تاجیکی را فراهم می‌کند. `FarsiToTajik` متن فارسی به خط عربی را به خط سیریلیک تاجیکی تبدیل می‌کند و `TajikToFarsi` تبدیل معکوس را انجام می‌دهد.

**نمونهٔ استفاده**

```python
from shekar import FarsiToTajik, TajikToFarsi

fa = FarsiToTajik()
print(fa("ایران مادر است!"))

tj = TajikToFarsi()
print(tj("Эрон модар аст!"))
```
