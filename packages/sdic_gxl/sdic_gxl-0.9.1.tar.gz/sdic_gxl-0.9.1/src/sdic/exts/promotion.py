from datetime import datetime

from sqlalchemy import func, and_
from sqlalchemy.orm import Session, aliased
from sdic.db.models import *
from sdic.constants import *
import pandas as pd


def get_promotion(session: Session,
                  begin_str: str,
                  end_str: str,
                  fund_name: str = '央企乡村投资基金'
                  ) -> dict:
    """
    获取基金的推进数据
    Args:
        session: 数据库会话
        begin_str: 开始时间,e.g. '2023-01-01'
        end_str: 结束时间.e.g. '2023-01-31'
        fund_name: 基金名称，默认为'央企乡村投资基金'
    Returns:
        dict: 推进数据字典
    """
    begin = datetime.strptime(begin_str, '%Y-%m-%d').date()
    end = datetime.strptime(end_str, '%Y-%m-%d').date()

    cash: FCTCashflowBase = aliased(FCTCashflowBase)
    vip: VInvestProject = aliased(VInvestProject)

    cash_data = session.query(
        cash.CAPITAL_TYPE,
        cash.FD_DATE,
        cash.FD_AMOUNT,
        vip.VC_FUND_NAME,
        vip.FD_SHOR_NAME
    ).outerjoin(
        vip,
        and_(
            cash.FD_PROJECT_ID == vip.FD_PROJECT_ID,
            cash.FD_FUND_ID == vip.FD_FUND_ID
        )
    ).filter(
        vip.FD_GSTYPE == '国投创益',
        vip.VC_FUND_NAME == fund_name,
        vip.FD_INVESTMENT_STATUS.in_(['0', '2']),
        cash.CAPITAL_TYPE.in_(ALL_LIST)
    )
    cash_info = pd.DataFrame(cash_data)
    cash_info_month = cash_info.query('FD_DATE <= @end and FD_DATE>=@begin')
    cash_info_acc = cash_info.query('FD_DATE <= @end')

    # 本月情况
    month_pay = {
        '本月拨付项目': len(
            cash_info_month.query('CAPITAL_TYPE in ["对外投资","投资保证金"]')['FD_SHOR_NAME'].unique()),
        '本月拨款': cash_info_month.query('CAPITAL_TYPE in ["对外投资","投资保证金"]')['FD_AMOUNT'].sum() / 10000,
    }
    # 本月回款
    month_income = {
        '本月回款项目个数': len(cash_info_month.query('CAPITAL_TYPE in @REVENUE_LIST')['FD_SHOR_NAME'].unique()),
        '本月回款金额': cash_info_month.query('CAPITAL_TYPE in @REVENUE_LIST')['FD_AMOUNT'].sum() / 10000,
        '本月回款本金': cash_info_month.query('CAPITAL_TYPE == "退回本金"')['FD_AMOUNT'].sum() / 10000,
        '本月收益': cash_info_month.query('CAPITAL_TYPE in @INCOME_LIST')['FD_AMOUNT'].sum() / 10000,
    }
    # 累计拨款
    acc_pay = {
        '累计拨款': cash_info_acc.query('CAPITAL_TYPE in @PAY_LIST')['FD_AMOUNT'].sum() / 10000,
        '累计回款': cash_info_acc.query('CAPITAL_TYPE in @REVENUE_LIST')['FD_AMOUNT'].sum() / 10000,
        '累计收益': cash_info_acc.query('CAPITAL_TYPE in @INCOME_LIST')['FD_AMOUNT'].sum() / 10000
    }

    rst = {
        '本月拨款项目': cash_info_month.query('CAPITAL_TYPE in ["对外投资","投资保证金"]')[
            'FD_SHOR_NAME'].unique().tolist(),
        '本月拨款': month_pay,
        '本月回款': month_income,
        '累计情况': acc_pay,
    }
    return rst
