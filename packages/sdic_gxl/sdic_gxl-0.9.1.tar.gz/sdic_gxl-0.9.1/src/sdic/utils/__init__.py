import pandas as pd
from scipy import optimize


# 计算现值
def xnpv(rate, cash_flow):
    return sum([cf / (1 + rate) ** ((t - cash_flow[0][0]).days / 365.0) for (t, cf) in cash_flow])


# 计算内部收益率（IRR）
def xirr(cash_flow,
         low=-0.9999,  # 1+r 不能 ≤0
         high=10,  # 1000% 的年化利率上限
         tol=1e-10):
    """
    计算内部收益率（IRR），使用 Brent 方法。
    cash_flow: [(时间, 现金流), ...]，时间必须是 datetime.date 或 datetime.datetime 对象。
    """
    # 1️⃣ 现金流整理
    cash_flow = sorted([(t, cf) for t, cf in cash_flow],
                       key=lambda x: x[0])

    # 2️⃣ 至少要有正有负
    if all(cf >= 0 for _, cf in cash_flow) or all(cf <= 0 for _, cf in cash_flow):
        return ""
    #         raise ValueError("现金流必须同时包含正、负值，IRR 才有意义")

    f_low, f_high = xnpv(low, cash_flow), xnpv(high, cash_flow)

    # 3️⃣ 如果两端同号，就把上限不断往上（或下）扩直到异号或超范围
    step = 2
    while f_low * f_high > 0 and high < 1e6:
        high *= step
        f_high = xnpv(high, cash_flow)

    if f_low * f_high > 0:
        return ""
    #         raise RuntimeError("在搜索范围内未找到 NPV 的符号变化，IRR 不存在")

    # 4️⃣ 用 Brent 法（对区间端点只要求异号，不用导数）
    return optimize.brentq(lambda r: xnpv(r, cash_flow), low, high, xtol=tol)


def obj_to_df(objs: list[object]) -> pd.DataFrame:
    """
    将sqlalchemy 返回的对象列表转换为 pandas DataFrame。
    :param objs:
    :return:
    """
    temp_dict = [{k: v for k, v in obj.__dict__.items() if not k.startswith('_')} for obj in objs]
    return pd.DataFrame(temp_dict)
