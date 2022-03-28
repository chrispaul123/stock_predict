import tushare as t1
from math import exp, log

t1.set_token('e49133a4f8a2b65703286d82a69d668935bce6b67515e8a34b13759a')
ts = t1.pro_api()

df = ts.daily(ts_code='600809.SH')
print(df['close'])
a1 = 235.49 / 234.74
a2 = 234.74 / 234.19
df1 = df[:5]

b1 = [0.897069, 0.252603]
b2 = [0.954485, 0.935146, 0.953759, 0.908799, 0.643431, 0.90386, 0.669584, 0.927401, 0.97777, 0.930162]



sum = 0
for b in b1:
    sum += (b - 0.7784)
c1 = sum / len(b1)
sum = 0
for b in b2:
    sum += (b - 0.7784)
c2 = sum / len(b2)
print(log(a2), log(a1))
print(c2, c1)
final = -0.0592 * log(a2) - 0.1415 * log(a1) + 0.00935 * c2 - 0.00905 * c1 - 0.00325
print(final)
# print(df['close'])
print(exp(final) * 235.49)
