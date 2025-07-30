import pandas as pd
from sdic.utils import *
from sdic.constants import *


def get_return(target_df: pd.DataFrame) -> dict:
    
    """
    根据现金流获取对应的现金和收益等指标
    Args:
        target_df: 现金流DataFrame,其中需要包括的列
            CAPITAL_TYPE: 现金流类型
            FD_AMOUNT: 金额
            VC_FUND_NAME: 基金名称
            FD_SHOR_NAME: 项目名称
    """

    target_df.loc[:, 'adj_amount'] = target_df.apply(
        lambda x: -x["FD_AMOUNT"] if x['CAPITAL_TYPE'] in PAY_LIST else x['FD_AMOUNT'], axis=1)
    target_flows = [(t, cf) for t, cf in zip(target_df['FD_DATE'], target_df['adj_amount'])]

    # 拨款金额
    pay = target_df.query("CAPITAL_TYPE in @PAY_LIST")['FD_AMOUNT'].sum()
    # 项目个数
    count = target_df.query("CAPITAL_TYPE in @PAY_LIST").drop_duplicates(subset=['VC_FUND_NAME', 'FD_SHOR_NAME'],
                                                                         keep='first').shape[0]
    # 资金回收序列
    income_flow = target_df.query("CAPITAL_TYPE == '退回本金'").sort_values(by='FD_DATE', ascending=True)[
        'FD_DATE'].to_list()
    # 首次退出资金时间
    first_exit = income_flow[0] if len(income_flow) > 0 else ""
    # 回收本金
    capital_back = target_df.query("CAPITAL_TYPE == '退回本金'")['FD_AMOUNT'].sum()
    # 退出收益
    profit = target_df.query("CAPITAL_TYPE == '退出收益'")['FD_AMOUNT'].sum()
    # 利息收益
    interest = target_df.query("CAPITAL_TYPE == '利息收益'")['FD_AMOUNT'].sum()
    # 分红收益
    divide = target_df.query("CAPITAL_TYPE == '分红收益'")['FD_AMOUNT'].sum()
    # 对赌补偿
    gamble = target_df.query("CAPITAL_TYPE == '对赌补偿'")['FD_AMOUNT'].sum()
    # 在投金额
    on_invest = pay - capital_back
    # 估值
    evaluate = target_df.query("CAPITAL_TYPE == '估值'")['FD_AMOUNT'].sum()
    # 回收资金
    total_income = target_df.query("CAPITAL_TYPE in @TOTAL_INCOME_LIST")['FD_AMOUNT'].sum()

    # dpi 回收资金/拨付金额
    dpi = total_income / pay
    # moc 资产价值/拨付金额
    moc = (total_income + evaluate) / pay
    # 综合收益 tci
    tci = total_income + evaluate - pay
    # irr
    irr = xirr(target_flows)

    return {
        "拨款金额": pay,
        "拨付项目个数": count,
        "退回本金": capital_back,
        "退出收益": profit,
        "利息收益": interest,
        "分红收益": divide,
        "对赌补偿": gamble,
        "在投金额": on_invest,
        "估值": evaluate,
        "回款合计": total_income,
        "DPI": dpi,
        "MOC": moc,
        "综合收益": tci,
        "IRR": irr,
        "首次资金回收时间": first_exit,
    }
