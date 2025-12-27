# secp256k1 的模数 P
P_CURVE = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F

# 你列表中的第 0 个点 (x, y)
x0 = 55066263022277343669578718895168534326250603453777594175500187360389116729240
y0 = 32670510020758816978083085130507043184471273380659243275938904335757337482424

# 你列表中的第 1 个点 (x, y)
x1_target = 89565891926547004231252920425935692360644145829622209833684329913297188986597
y1_target = 12158399299693830322967808612713398636155367887041628176798871954788371653930


def point_double(x, y, p):
    # 斜率 s = (3*x^2) / (2*y) mod p
    # 注意 secp256k1 的 a = 0
    numerator = 3 * x * x
    denominator = 2 * y

    # 计算模逆
    inv = pow(denominator, -1, p)
    s = (numerator * inv) % p

    # x3 = s^2 - 2x
    x3 = (s * s - 2 * x) % p

    # y3 = s(x - x3) - y
    y3 = (s * (x - x3) - y) % p

    return x3, y3


# 计算 2 * P0
calc_x1, calc_y1 = point_double(x0, y0, P_CURVE)

print(f"Calculated X1: {calc_x1}")
print(f"Target X1:     {x1_target}")
print("-" * 20)
if calc_x1 == x1_target and calc_y1 == y1_target:
    print("【结论】验证成功：P1 是 P0 的两倍 (2*P0)。")
    print("这意味着这是一个标准的 ECDLP 问题（离散对数）。")
else:
    print("【结论】验证失败：P1 与 P0 无线性倍数关系。")
    print("这意味着这是一个 Subset Sum / Knapsack 问题（可用 LLL 攻击）。")