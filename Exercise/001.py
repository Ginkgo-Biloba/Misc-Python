# coding: utf_8
# 做为 Apple Store App 独立开发者，你要搞限时促销，为你的应用生成激活码（或者优惠券），使用 Python 如何生成 200 个激活码（或者优惠券）？

import string, random
ics = []
x = 0
ps = string.ascii_letters + string.digits + string.punctuation

# 200 个激活码 | 每个 24 位
while (x < 200):
    ic = ''
    for i in range(24):
        ic += random.choice(ps)
    if ic not in ics:
        ics.append(ic)
        x += 1

print('\n'.join(ics))
